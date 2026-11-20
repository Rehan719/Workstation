#!/bin/bash
# FU-603's drills (W1137), on a machine with Docker: nothing is deployed and no account is touched.
# Usage: deploy/drill.sh CURRENT_IMAGE PREVIOUS_IMAGE   (two images built from this tree's Dockerfile, at two commits)
#   RESTORE: the records written by the current release are copied off their volume, restored onto a fresh one,
#            and the current release started on the copy reads them back.
#   ROLLBACK: on the restored volume, the previous release is started in place of the current one, reads the same
#            records, and the current release is started again over the same records.
#   WHERE THE RECORDS ARE: after real writes, `docker diff` lists what the container changed outside its volume.
# Each container runs with the flags deploy/gcp/startup.sh gives the release machine, plus the free-tier memory.
# Prints one KEY=VALUE line per measurement.
set -u
CUR=${1:?current release image}; PREV=${2:?previous release image}
D=$(mktemp -d); PORT=18081; N=ws-drill-$$
VA=ws-drill-a-$$; VB=ws-drill-b-$$
cleanup() { docker rm -f $N >/dev/null 2>&1; docker volume rm -f $VA $VB >/dev/null 2>&1; rm -rf "$D"; }
trap cleanup EXIT

start() {   # start IMAGE on VOLUME; print the seconds to a healthy answer
  docker rm -f $N >/dev/null 2>&1
  local t0; t0=$(date +%s.%N)
  docker run -d --name $N --publish=127.0.0.1:$PORT:8000 --volume="$2":/app/data \
    --log-opt max-size=10m --log-opt max-file=3 --memory=1g --memory-swap=1g -e AI_DISABLE_LOCAL=1 "$1" >/dev/null || return 1
  for _ in $(seq 1 120); do
    curl -fsS -o /dev/null --noproxy '*' "http://127.0.0.1:$PORT/health" 2>/dev/null && {
      python3 -c "import time; print(round(time.time() - $t0, 1))"; return 0; }
    sleep 1
  done
  docker logs --tail 30 $N; return 1
}
api() { curl -sS --noproxy '*' "$@"; }
census() {  # every file on a volume, with its digest, in order
  docker run --rm --user 0 -v "$1":/data:ro --entrypoint sh "$CUR" -c 'cd /data && find . -type f -exec sha256sum {} + | sort -k2'
}

docker volume create $VA >/dev/null && docker volume create $VB >/dev/null
echo "CURRENT_IMAGE=$CUR"; echo "PREVIOUS_IMAGE=$PREV"

# 1. the current release writes records
s=$(start "$CUR" $VA) || { echo "CURRENT_START_FAILED"; exit 1; }; echo "CURRENT_TO_HEALTH_SECONDS=$s"
pid=$(api -X POST "http://127.0.0.1:$PORT/api/v1/projects/" -H 'Content-Type: application/json' \
      -d '{"title": "Drill project W1137", "description": "made up for the restore and rollback drills"}' \
      | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])") || { echo "WRITE_FAILED"; exit 1; }
echo "PROJECT_WRITTEN=$pid"
api "http://127.0.0.1:$PORT/api/v1/plan" -o /dev/null; api "http://127.0.0.1:$PORT/api/v1/projects/" -o /dev/null
echo "CHANGED_OUTSIDE_THE_VOLUME=$(docker diff $N | awk '{print $2}' | grep -v -E '^/app/data(/|$)' | grep -v -E '^/tmp(/|$)' | tr '\n' ' ')"
echo "CHANGED_IN_TMP=$(docker diff $N | awk '{print $2}' | grep -c -E '^/tmp/')"
docker stop -t 10 $N >/dev/null

# 2. backup: the volume's records copied off it whole; restore: onto a fresh volume
t0=$(date +%s.%N)
docker run --rm --user 0 -v $VA:/data:ro -v "$D":/backup --entrypoint tar "$CUR" czf /backup/records.tgz -C /data . || { echo "BACKUP_FAILED"; exit 1; }
docker run --rm --user 0 -v $VB:/data -v "$D":/backup --entrypoint tar "$CUR" xzpf /backup/records.tgz -C /data || { echo "RESTORE_FAILED"; exit 1; }
echo "BACKUP_AND_RESTORE_SECONDS=$(python3 -c "import time; print(round(time.time() - $t0, 1))")"
echo "BACKUP_BYTES=$(stat -c %s "$D/records.tgz")"
a=$(census $VA); b=$(census $VB)
echo "FILES_ON_ORIGINAL=$(echo "$a" | grep -c .) FILES_ON_RESTORED=$(echo "$b" | grep -c .) IDENTICAL=$([ "$a" = "$b" ] && echo yes || echo no)"
echo "OWNER_ON_RESTORED=$(docker run --rm --user 0 -v $VB:/data --entrypoint stat "$CUR" -c '%u:%g' /data)"

# 3. the current release on the restored copy reads the record back
s=$(start "$CUR" $VB) || { echo "RESTORED_START_FAILED"; exit 1; }; echo "RESTORED_TO_HEALTH_SECONDS=$s"
echo "RESTORED_READS_PROJECT=$(api -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/api/v1/projects/$pid")"

# 4. rollback: the previous release on the same records, then forward again
s=$(start "$PREV" $VB) || { echo "ROLLBACK_START_FAILED"; exit 1; }; echo "ROLLBACK_TO_HEALTH_SECONDS=$s"
echo "ROLLBACK_READS_PROJECT=$(api -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/api/v1/projects/$pid")"
echo "ROLLBACK_LISTS_PROJECT=$(api "http://127.0.0.1:$PORT/api/v1/projects/" | python3 -c "import json,sys; print(any(p['id']=='$pid' for p in json.load(sys.stdin)))")"
s=$(start "$CUR" $VB) || { echo "FORWARD_START_FAILED"; exit 1; }; echo "FORWARD_TO_HEALTH_SECONDS=$s"
echo "FORWARD_READS_PROJECT=$(api -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT/api/v1/projects/$pid")"
echo "DRILL_DONE=yes"
