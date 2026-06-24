#!/bin/bash
# End-to-end verification for the Employment Application Studio feature.
# Exercises: per-category upload, category filtering, full multi-output generation,
# single-output generation, empty-input generation, invalid output type, deletion,
# autonomous miscellaneous-upload categorization, the live job search engine (explicit
# query / instructions-derived / upload-derived / zero-signal fallback), and wiring a
# found listing back in as the Target Job Ad input, and the distinct Job Description
# input category (separate from Target Job Ad) including its classifier disambiguation.
set -uo pipefail
BASE="http://localhost:8000/api/v1"
FAIL=0

check() {
  local desc="$1" cond="$2"
  if [ "$cond" = "1" ]; then
    echo "PASS: $desc"
  else
    echo "FAIL: $desc"
    FAIL=1
  fi
}

WORKDIR=$(mktemp -d)
CATEGORIES=(cv_history past_applications star_examples job_ad job_description person_spec application_guidance interview_prep_materials)
declare -A FILE_IDS

echo "=== 1. Upload one file per input category ==="
for cat in "${CATEGORIES[@]}"; do
  echo "Sample content for $cat" > "$WORKDIR/$cat.txt"
  RESP=$(curl -s -X POST "$BASE/ingest/" -F "file=@$WORKDIR/$cat.txt" -F "category=$cat")
  FID=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin).get('file_id',''))" 2>/dev/null)
  RETURNED_CAT=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin).get('category',''))" 2>/dev/null)
  FILE_IDS[$cat]=$FID
  check "upload($cat) returns file_id" "$([ -n "$FID" ] && echo 1 || echo 0)"
  check "upload($cat) tags correct category" "$([ "$RETURNED_CAT" = "$cat" ] && echo 1 || echo 0)"
done

echo "=== 2. Category filtering on /ingest/list ==="
for cat in "${CATEGORIES[@]}"; do
  COUNT=$(curl -s "$BASE/ingest/list?category=$cat" | python -c "import sys,json; print(len(json.load(sys.stdin)))")
  check "list?category=$cat returns exactly 1 (got $COUNT)" "$([ "$COUNT" = "1" ] && echo 1 || echo 0)"
done

UNFILTERED_COUNT=$(curl -s "$BASE/ingest/list" | python -c "import sys,json; print(len(json.load(sys.stdin)))")
check "unfiltered list count >= ${#CATEGORIES[@]} (got $UNFILTERED_COUNT)" "$([ "$UNFILTERED_COUNT" -ge "${#CATEGORIES[@]}" ] && echo 1 || echo 0)"

echo "=== 3. Generate with ALL 8 output types together ==="
ALL_FILE_IDS=$(python -c "import json; print(json.dumps(list('${FILE_IDS[cv_history]}|${FILE_IDS[past_applications]}|${FILE_IDS[star_examples]}|${FILE_IDS[job_ad]}|${FILE_IDS[job_description]}|${FILE_IDS[person_spec]}|${FILE_IDS[application_guidance]}|${FILE_IDS[interview_prep_materials]}'.split('|'))))")
PAYLOAD=$(python -c "
import json
file_ids = $ALL_FILE_IDS
payload = {
    'file_ids': file_ids,
    'company_website': 'https://example.com',
    'linkedin_url': 'https://linkedin.com/in/test-user',
    'instructions': 'Senior Backend Engineer role at a fintech scaleup',
    'output_types': ['cv','cover_letter','supporting_statement','application_form','interview_prep','new_job_prep','in_job_support','linkedin_profile']
}
print(json.dumps(payload))
")
RESP=$(curl -s -X POST "$BASE/career/generate" -H "Content-Type: application/json" -d "$PAYLOAD")
RESULT_COUNT=$(echo "$RESP" | python -c "import sys,json; print(len(json.load(sys.stdin)['results']))")
check "generate(all 8 outputs) returns 8 results (got $RESULT_COUNT)" "$([ "$RESULT_COUNT" = "8" ] && echo 1 || echo 0)"

NONEMPTY=$(echo "$RESP" | python -c "
import sys,json
r = json.load(sys.stdin)['results']
print(1 if all(len(d['content']) > 100 and d['title'] and d['output_id'] for d in r) else 0)
")
check "all 8 results have non-trivial content/title/output_id" "$NONEMPTY"

UNIQUE_CONTENT=$(echo "$RESP" | python -c "
import sys,json
r = json.load(sys.stdin)['results']
print(1 if len(set(d['content'] for d in r)) == len(r) else 0)
")
check "all 8 results have distinct content (not templated stubs)" "$UNIQUE_CONTENT"

CONTEXT_REFLECTED=$(echo "$RESP" | python -c "
import sys,json
r = json.load(sys.stdin)['results']
cv = next(d for d in r if d['output_type']=='cv')
print(1 if 'example.com' in cv['content'] and 'linkedin.com/in/test-user' in cv['content'] else 0)
")
check "generated content reflects company_website + linkedin_url context" "$CONTEXT_REFLECTED"

JOB_DESCRIPTION_REFLECTED=$(echo "$RESP" | python -c "
import sys,json
r = json.load(sys.stdin)['results']
cv = next(d for d in r if d['output_type']=='cv')
print(1 if 'job description document' in cv['content'] else 0)
")
check "generated content reflects uploaded job_description context" "$JOB_DESCRIPTION_REFLECTED"

echo "=== 4. Generate with a single output type ==="
SINGLE=$(curl -s -X POST "$BASE/career/generate" -H "Content-Type: application/json" -d '{"file_ids": [], "output_types": ["linkedin_profile"], "instructions": "Test"}')
SINGLE_COUNT=$(echo "$SINGLE" | python -c "import sys,json; print(len(json.load(sys.stdin)['results']))")
check "generate(linkedin_profile only) returns 1 result" "$([ "$SINGLE_COUNT" = "1" ] && echo 1 || echo 0)"

echo "=== 5. Generate with empty inputs and empty output_types ==="
EMPTY=$(curl -s -X POST "$BASE/career/generate" -H "Content-Type: application/json" -d '{"file_ids": [], "output_types": []}')
EMPTY_COUNT=$(echo "$EMPTY" | python -c "import sys,json; print(len(json.load(sys.stdin)['results']))")
check "generate(no outputs) returns 0 results, no error" "$([ "$EMPTY_COUNT" = "0" ] && echo 1 || echo 0)"

NO_CONTEXT_FALLBACK=$(curl -s -X POST "$BASE/career/generate" -H "Content-Type: application/json" -d '{"file_ids": [], "output_types": ["cv"]}' | python -c "
import sys,json
r = json.load(sys.stdin)['results'][0]
print(1 if 'No supporting materials supplied' in r['content'] else 0)
")
check "generate with zero context falls back to default context message" "$NO_CONTEXT_FALLBACK"

echo "=== 6. Invalid output type handled gracefully ==="
INVALID=$(curl -s -X POST "$BASE/career/generate" -H "Content-Type: application/json" -d '{"file_ids": [], "output_types": ["not_a_real_type"]}')
INVALID_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/career/generate" -H "Content-Type: application/json" -d '{"file_ids": [], "output_types": ["not_a_real_type"]}')
check "invalid output_type does not 500 (got HTTP $INVALID_STATUS)" "$([ "$INVALID_STATUS" = "200" ] && echo 1 || echo 0)"

echo "=== 7. Deletion ==="
DEL_ID=${FILE_IDS[cv_history]}
DEL_RESP=$(curl -s -X DELETE "$BASE/ingest/$DEL_ID")
DEL_STATUS=$(echo "$DEL_RESP" | python -c "import sys,json; print(json.load(sys.stdin).get('status',''))")
check "delete($DEL_ID) returns DELETED" "$([ "$DEL_STATUS" = "DELETED" ] && echo 1 || echo 0)"

POST_DELETE_COUNT=$(curl -s "$BASE/ingest/list?category=cv_history" | python -c "import sys,json; print(len(json.load(sys.stdin)))")
check "cv_history category empty after delete (got $POST_DELETE_COUNT)" "$([ "$POST_DELETE_COUNT" = "0" ] && echo 1 || echo 0)"

DOUBLE_DELETE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE/ingest/$DEL_ID")
check "double-delete returns 404 (got $DOUBLE_DELETE_STATUS)" "$([ "$DOUBLE_DELETE_STATUS" = "404" ] && echo 1 || echo 0)"

echo "=== 8. Autonomous categorization (Miscellaneous slot) ==="
declare -A MISC_IDS

classify_sample() {
  local label="$1" content="$2" expected="$3"
  echo "$content" > "$WORKDIR/misc_${expected}.txt"
  RESP=$(curl -s -X POST "$BASE/career/uploads/auto" -F "file=@$WORKDIR/misc_${expected}.txt")
  FID=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin).get('file_id',''))" 2>/dev/null)
  GOT_CAT=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin)['classification']['category'])" 2>/dev/null)
  STORED_CAT=$(echo "$RESP" | python -c "import sys,json; print(json.load(sys.stdin)['category'])" 2>/dev/null)
  MISC_IDS[$expected]=$FID
  check "classify($label) -> expected '$expected', got '$GOT_CAT'" "$([ "$GOT_CAT" = "$expected" ] && echo 1 || echo 0)"
  check "classify($label) persists category on registry entry (got '$STORED_CAT')" "$([ "$STORED_CAT" = "$expected" ] && echo 1 || echo 0)"
}

classify_sample "CV-like text" "CURRICULUM VITAE. Professional Summary. Work Experience: 10 years in engineering. Career history attached." "cv_history"
classify_sample "Past application text" "This is your application reference 12345. Previously applied on 2025-01-01 via the submitted application portal." "past_applications"
classify_sample "STAR example text" "Situation: tight deadline. Task: deliver feature. Action: coordinated team. Result: shipped on time. STAR method used throughout." "star_examples"
classify_sample "Job ad text" "We are looking for a Senior Engineer to join our team. Competitive salary. Job Title: Senior Engineer. Apply now." "job_ad"
classify_sample "Job description text" "Job Description. Job Purpose: lead the engineering function. Key Responsibilities: oversee delivery and mentor staff. Reports to: Head of Engineering. Job Summary attached." "job_description"
classify_sample "Person spec text" "Person Specification. Essential criteria: 5 years experience. Desirable criteria: leadership. Selection criteria applied." "person_spec"
classify_sample "Application guidance text" "How to apply: submit your application before the closing date. Application guidance and submission instructions enclosed." "application_guidance"
classify_sample "Interview prep text" "Interview panel will ask competency based interview questions at the assessment centre." "interview_prep_materials"

echo "--- Unclassifiable content falls back to 'uncategorized' ---"
echo "asdf qwer zxcv random unrelated gibberish text with no domain signal" > "$WORKDIR/misc_none.txt"
NONE_RESP=$(curl -s -X POST "$BASE/career/uploads/auto" -F "file=@$WORKDIR/misc_none.txt")
NONE_FID=$(echo "$NONE_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['file_id'])")
NONE_CAT=$(echo "$NONE_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['classification']['category'])")
NONE_CONF=$(echo "$NONE_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['classification']['confidence'])")
check "unclassifiable content falls back to 'uncategorized' (got '$NONE_CAT')" "$([ "$NONE_CAT" = "uncategorized" ] && echo 1 || echo 0)"
check "unclassifiable content has 0.0 confidence (got '$NONE_CONF')" "$([ "$NONE_CONF" = "0.0" ] && echo 1 || echo 0)"

UNCATEGORIZED_LIST_COUNT=$(curl -s "$BASE/ingest/list?category=uncategorized" | python -c "import sys,json; print(len(json.load(sys.stdin)))")
check "uncategorized item discoverable via /ingest/list?category=uncategorized" "$([ "$UNCATEGORIZED_LIST_COUNT" -ge "1" ] && echo 1 || echo 0)"

echo "--- Cleanup auto-categorized test files ---"
for k in "${!MISC_IDS[@]}"; do
  curl -s -X DELETE "$BASE/ingest/${MISC_IDS[$k]}" > /dev/null
done
curl -s -X DELETE "$BASE/ingest/$NONE_FID" > /dev/null

echo "=== 9. Cleanup remaining test uploads ==="
for cat in past_applications star_examples job_ad job_description person_spec application_guidance interview_prep_materials; do
  curl -s -X DELETE "$BASE/ingest/${FILE_IDS[$cat]}" > /dev/null
done
CLEANUP_COUNT=$(curl -s "$BASE/ingest/list" | python -c "
import sys,json
data = json.load(sys.stdin)
ids = set('${FILE_IDS[past_applications]} ${FILE_IDS[star_examples]} ${FILE_IDS[job_ad]} ${FILE_IDS[job_description]} ${FILE_IDS[person_spec]} ${FILE_IDS[application_guidance]} ${FILE_IDS[interview_prep_materials]}'.split())
print(sum(1 for d in data if d['file_id'] in ids))
")
check "all test uploads cleaned up (remaining: $CLEANUP_COUNT)" "$([ "$CLEANUP_COUNT" = "0" ] && echo 1 || echo 0)"

rm -rf "$WORKDIR"

echo "=== 10. Live job search engine ==="
WORKDIR2=$(mktemp -d)

EXPLICIT=$(curl -s -m 20 -X POST "$BASE/career/job-search" -H "Content-Type: application/json" -d '{"file_ids": [], "instructions": "", "query": "python developer", "limit": 5}')
EXPLICIT_QUERY=$(echo "$EXPLICIT" | python -c "import sys,json; print(json.load(sys.stdin)['query'])")
EXPLICIT_COUNT=$(echo "$EXPLICIT" | python -c "import sys,json; print(json.load(sys.stdin)['count'])")
EXPLICIT_SOURCES=$(echo "$EXPLICIT" | python -c "import sys,json; print(len(json.load(sys.stdin)['sources_used']))")
check "job-search(explicit query) echoes query (got '$EXPLICIT_QUERY')" "$([ "$EXPLICIT_QUERY" = "python developer" ] && echo 1 || echo 0)"
check "job-search(explicit query) returns live results (got $EXPLICIT_COUNT)" "$([ "$EXPLICIT_COUNT" -gt "0" ] && echo 1 || echo 0)"
check "job-search(explicit query) used >=1 live source (got $EXPLICIT_SOURCES)" "$([ "$EXPLICIT_SOURCES" -ge "1" ] && echo 1 || echo 0)"

RESULT_SHAPE_OK=$(echo "$EXPLICIT" | python -c "
import sys,json
r = json.load(sys.stdin)['results']
ok = len(r) > 0 and all(d.get('title') and d.get('url') and d.get('source') for d in r)
print(1 if ok else 0)
")
check "job-search results have title/url/source populated" "$RESULT_SHAPE_OK"

INSTR_RESP=$(curl -s -m 20 -X POST "$BASE/career/job-search" -H "Content-Type: application/json" -d '{"file_ids": [], "instructions": "remote customer support", "query": "", "limit": 5}')
INSTR_QUERY=$(echo "$INSTR_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['query'])")
check "job-search(no query) derives query from instructions (got '$INSTR_QUERY')" "$([ "$INSTR_QUERY" = "remote customer support" ] && echo 1 || echo 0)"

echo "Frontend Engineer at a Series B startup" > "$WORKDIR2/job_ad_for_search.txt"
JOBAD_RESP=$(curl -s -X POST "$BASE/ingest/" -F "file=@$WORKDIR2/job_ad_for_search.txt" -F "category=job_ad")
JOBAD_FID=$(echo "$JOBAD_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['file_id'])")
DERIVED_RESP=$(curl -s -m 20 -X POST "$BASE/career/job-search" -H "Content-Type: application/json" -d "{\"file_ids\": [\"$JOBAD_FID\"], \"instructions\": \"\", \"query\": \"\", \"limit\": 5}")
DERIVED_QUERY=$(echo "$DERIVED_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['query'])")
check "job-search(no query/instructions) derives from uploaded job_ad (got '$DERIVED_QUERY')" "$([ "$DERIVED_QUERY" = "Frontend Engineer at a Series B startup" ] && echo 1 || echo 0)"

NO_SIGNAL_RESP=$(curl -s -m 20 -X POST "$BASE/career/job-search" -H "Content-Type: application/json" -d '{"file_ids": [], "instructions": "", "query": "", "limit": 5}')
NO_SIGNAL_QUERY=$(echo "$NO_SIGNAL_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['query'])")
check "job-search(zero signal) falls back to 'remote' (got '$NO_SIGNAL_QUERY')" "$([ "$NO_SIGNAL_QUERY" = "remote" ] && echo 1 || echo 0)"

curl -s -X DELETE "$BASE/ingest/$JOBAD_FID" > /dev/null
rm -rf "$WORKDIR2"

echo "=== 11. 'Use as Target Job Ad' wiring from a found listing ==="
USE_RESP=$(curl -s -X POST "$BASE/career/job-search/use" -H "Content-Type: application/json" -d '{
  "title": "Senior Backend Engineer",
  "company": "Acme Corp",
  "location": "Remote",
  "url": "https://example.com/jobs/123",
  "description": "Build and scale backend systems.",
  "source": "Remotive"
}')
USE_FID=$(echo "$USE_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['file_id'])")
USE_CAT=$(echo "$USE_RESP" | python -c "import sys,json; print(json.load(sys.stdin)['category'])")
check "job-search/use tags listing as 'job_ad' category (got '$USE_CAT')" "$([ "$USE_CAT" = "job_ad" ] && echo 1 || echo 0)"

USE_LISTED=$(curl -s "$BASE/ingest/list?category=job_ad" | python -c "
import sys,json
data = json.load(sys.stdin)
print(1 if any(d['file_id']=='$USE_FID' for d in data) else 0)
")
check "used listing discoverable via /ingest/list?category=job_ad" "$USE_LISTED"

USE_TEXT_OK=$(curl -s "$BASE/ingest/list?category=job_ad" | python -c "
import sys,json
data = json.load(sys.stdin)
entry = next(d for d in data if d['file_id']=='$USE_FID')
text = entry['extracted_text']
print(1 if 'Senior Backend Engineer' in text and 'Acme Corp' in text and 'example.com/jobs/123' in text else 0)
")
check "used listing's extracted_text carries title/company/url" "$USE_TEXT_OK"

curl -s -X DELETE "$BASE/ingest/$USE_FID" > /dev/null

echo ""
if [ "$FAIL" = "0" ]; then
  echo "ALL CHECKS PASSED"
else
  echo "SOME CHECKS FAILED"
fi
exit $FAIL
