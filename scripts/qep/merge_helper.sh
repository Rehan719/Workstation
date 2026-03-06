#!/bin/bash
echo "--- QEP Merge Conflict Helper (Article 95/120) ---"
echo "Identifying conflicts..."
git status | grep "both modified"
echo ""
echo "Resolution strategy: Prioritizing v99.0 Transcendent Baselines."
echo "Use 'git checkout --ours <file>' for v99 baseline or 'git checkout --theirs <file>' for local features."
