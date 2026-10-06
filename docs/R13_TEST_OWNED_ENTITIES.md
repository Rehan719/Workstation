# R13 — the test-owned entities, listed for the Owner to approve

Owner ruling 2026-10-05b, R13: **the prune is approved AS A LIST, NOT AS A CONCEPT.** This is that
list. Nothing has been deleted, and the script that produced it has no delete path.

- entities on disk: **219**
- owner_id exactly one of ['pytest']: **162**
- other owners: **57**
- of the test-owned, **50** carry a LEDGER, a REPO or a roster entry — economic
  events were posted, or a body was shipped to disk, so these are not stray fixtures.
- a further **112** are referenced ONLY by an auto-seeded business plan, which is
  created for every entity and therefore says nothing about whether anything happened to it.

Matching is an EXACT owner_id comparison, never a substring: a real owner whose name contains
"pytest" would otherwise be swept in, which is the bare-word mistake this round hit twice.

| # | vsb_id | name | status | created | also on disk as |
|---|--------|------|--------|---------|-----------------|
| 1 | `vsb-000b75b0c4` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 2 | `vsb-0340e1ab07` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 3 | `vsb-04ea154b67` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 4 | `vsb-0573e3e2a1` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 5 | `vsb-05809c02e8` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 6 | `vsb-067f5a3868` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 7 | `vsb-06a576445f` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 8 | `vsb-070343695f` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 9 | `vsb-0882e81280` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 10 | `vsb-0a3d1f2585` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 11 | `vsb-0c108d05f1` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 12 | `vsb-0f9990d928` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 13 | `vsb-114fb493a8` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 14 | `vsb-12d937d05e` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 15 | `vsb-15f4ca6d5f` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 16 | `vsb-1685a08a2d` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 17 | `vsb-170650a2a4` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 18 | `vsb-18778ead15` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 19 | `vsb-18b5202a4f` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 20 | `vsb-18c1a044c5` | VSB — per-vsb deliverable | operational | 2026-06-30 | business plan |
| 21 | `vsb-1aabf0d821` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 22 | `vsb-1f1b5f42b0` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 23 | `vsb-225512f64e` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 24 | `vsb-236448d224` | VSB — avatar grounding test | operational | 2026-06-30 | business plan |
| 25 | `vsb-23ba76ce60` | VSB — ledger lock-in | operational | 2026-06-30 | business plan |
| 26 | `vsb-242be7f086` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 27 | `vsb-267c8f2f47` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 28 | `vsb-2682149ff1` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 29 | `vsb-26b30162f9` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 30 | `vsb-28cb9cd857` | VSB — list-flags test | operational | 2026-06-30 | business plan |
| 31 | `vsb-2c9c01adf1` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 32 | `vsb-2d69e838b4` | VSB — pytest VSB business-plan seed check | operational | 2026-06-30 | business plan |
| 33 | `vsb-2dac0a963a` | VSB — pytest VSB business-plan seed check | operational | 2026-06-30 | business plan |
| 34 | `vsb-2ed7fe7b43` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 35 | `vsb-323fa06bd2` | VSB — pytest per-vsb swarm | operational | 2026-06-30 | business plan |
| 36 | `vsb-33c1d624df` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 37 | `vsb-342610d248` | VSB — avatar grounding test | operational | 2026-06-30 | business plan |
| 38 | `vsb-34d57722d1` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 39 | `vsb-36189f1765` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 40 | `vsb-362bf547c4` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 41 | `vsb-370b59a53f` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 42 | `vsb-38deea4ff9` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 43 | `vsb-38defe6b80` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 44 | `vsb-39a81d2d58` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 45 | `vsb-3b3c25e172` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 46 | `vsb-3b5a7fa09a` | VSB — per-vsb deliverable | operational | 2026-06-30 | business plan |
| 47 | `vsb-3d9e97d76b` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 48 | `vsb-3f09f40ed2` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 49 | `vsb-3f660dbd3c` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 50 | `vsb-3fe6729eee` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 51 | `vsb-44f69adb47` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 52 | `vsb-454ff83c0f` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 53 | `vsb-464e5c3709` | VSB — ledger lock-in | operational | 2026-06-30 | business plan |
| 54 | `vsb-49a52ce858` | VSB — list-flags test | operational | 2026-06-30 | business plan |
| 55 | `vsb-4a2bc0802f` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 56 | `vsb-4c6bcbd65d` | VSB — pytest VSB business-plan seed check | operational | 2026-06-30 | business plan |
| 57 | `vsb-4d2f938da9` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 58 | `vsb-4d9bb368c3` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 59 | `vsb-547b62d743` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 60 | `vsb-554c6676f9` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 61 | `vsb-5558582314` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 62 | `vsb-5624a730fa` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 63 | `vsb-5aac6b830e` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 64 | `vsb-5b6251a209` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 65 | `vsb-5e1e053912` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 66 | `vsb-644452646c` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 67 | `vsb-673a7465df` | VSB — list-flags test | operational | 2026-06-30 | business plan |
| 68 | `vsb-6b19b04add` | VSB — ledger lock-in | operational | 2026-06-30 | business plan |
| 69 | `vsb-6bd5354c2d` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 70 | `vsb-6c80fdd503` | VSB — ledger lock-in | operational | 2026-06-30 | business plan |
| 71 | `vsb-6cb7bc5db4` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 72 | `vsb-6cbf407c81` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 73 | `vsb-6cc08b3d00` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 74 | `vsb-6d6dad5ee3` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 75 | `vsb-71f2e069f5` | VSB — avatar grounding test | operational | 2026-06-30 | business plan |
| 76 | `vsb-77da2e63bf` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 77 | `vsb-7c4c07a1da` | VSB — pytest VSB business-plan seed check | operational | 2026-06-30 | business plan |
| 78 | `vsb-86e5d0dae1` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 79 | `vsb-86fbfa31d5` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 80 | `vsb-87f6c799d4` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 81 | `vsb-88dfc70a61` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 82 | `vsb-8963da3558` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 83 | `vsb-8a80bb39ea` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 84 | `vsb-8a951e2113` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 85 | `vsb-8dc9c84b33` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 86 | `vsb-8e36c8066a` | VSB — pytest per-vsb swarm | operational | 2026-06-30 | business plan |
| 87 | `vsb-8eab78223c` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 88 | `vsb-8ffcefb274` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 89 | `vsb-939933c66c` | VSB — avatar grounding test | operational | 2026-06-30 | business plan |
| 90 | `vsb-93d06bf891` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 91 | `vsb-96b10e7590` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 92 | `vsb-979b096264` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 93 | `vsb-9ac18c8c14` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 94 | `vsb-9b5e39caa9` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 95 | `vsb-9ff6f84d91` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 96 | `vsb-a01b2af1d6` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 97 | `vsb-a1e2f8ac72` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 98 | `vsb-a466d5e838` | VSB — pytest per-vsb swarm | operational | 2026-06-30 | business plan |
| 99 | `vsb-aa71c26445` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 100 | `vsb-abd0f0edbd` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 101 | `vsb-abe1419767` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 102 | `vsb-ac0f5c4133` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 103 | `vsb-ac9fd0210d` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 104 | `vsb-acb1c8ac15` | VSB — per-vsb deliverable | operational | 2026-06-30 | business plan |
| 105 | `vsb-ad2d6c0e38` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 106 | `vsb-ada946bdd6` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 107 | `vsb-af62f4353d` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 108 | `vsb-b04a7e42cf` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 109 | `vsb-b2f21b2876` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 110 | `vsb-b317579762` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 111 | `vsb-b36090baba` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 112 | `vsb-b37bd4eee7` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 113 | `vsb-b54d2b98c8` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 114 | `vsb-b85c184f3d` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 115 | `vsb-b896126d29` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 116 | `vsb-bf6fcb188d` | VSB — per-vsb deliverable | operational | 2026-06-30 | business plan |
| 117 | `vsb-c0f227c0fb` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 118 | `vsb-c29660aaa3` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 119 | `vsb-c3e5d72165` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 120 | `vsb-c5ccc6d2a9` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 121 | `vsb-c755564e6e` | VSB — pytest per-vsb swarm | operational | 2026-06-30 | business plan |
| 122 | `vsb-c8498ba01a` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 123 | `vsb-c8a3d027f1` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 124 | `vsb-c8f6f6bbd7` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 125 | `vsb-ca084cb019` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 126 | `vsb-ce97065195` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 127 | `vsb-cf8aad58a7` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 128 | `vsb-cfa9a93d33` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 129 | `vsb-cfc6e7e41d` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 130 | `vsb-d00573f5bc` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 131 | `vsb-d0caf0dc80` | VSB — pytest VSB business-plan seed check | operational | 2026-06-29 | business plan |
| 132 | `vsb-d0cec0bc4c` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 133 | `vsb-d3e1f340b1` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 134 | `vsb-d4f4217a8c` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 135 | `vsb-d5fda298c8` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 136 | `vsb-d63577cebb` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 137 | `vsb-d6fef75254` | VSB — avatar grounding test | operational | 2026-06-29 | business plan |
| 138 | `vsb-d865433b57` | VSB — list-flags test | operational | 2026-06-30 | business plan |
| 139 | `vsb-d8da3f4dbd` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 140 | `vsb-da887e8800` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 141 | `vsb-dc5e467a11` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 142 | `vsb-dfb81ba1c2` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 143 | `vsb-e087d4ffb8` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 144 | `vsb-e332a6f82c` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 145 | `vsb-e463d5542f` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 146 | `vsb-e758d229e2` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 147 | `vsb-e7c9b5048c` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 148 | `vsb-e820cb0a7f` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 149 | `vsb-e89e46128d` | VSB — pytest per-vsb swarm | operational | 2026-06-29 | business plan |
| 150 | `vsb-f01f2ce6c3` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 151 | `vsb-f0ef43fd4d` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 152 | `vsb-f3706686de` | VSB — ledger lock-in | operational | 2026-06-29 | business plan |
| 153 | `vsb-f6500f01e0` | VSB — a halal community meal service | operational | 2026-06-30 | business plan |
| 154 | `vsb-f67d7e0e67` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 155 | `vsb-f6f859baa2` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |
| 156 | `vsb-f9097b4f1c` | VSB — a halal community meal service | operational | 2026-06-29 | business plan |
| 157 | `vsb-fa3a355fc6` | VSB — list-flags test | operational | 2026-06-29 | business plan |
| 158 | `vsb-fa4bb6bffc` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 159 | `vsb-fe3b5403a3` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 160 | `vsb-fefa202668` | VSB — a halal community meal service | operational | 2026-06-29 | repo, business plan |
| 161 | `vsb-ff5e8006a4` | VSB — per-vsb deliverable | operational | 2026-06-29 | business plan |
| 162 | `vsb-ffaaa9c19b` | VSB — a halal community meal service | operational | 2026-06-30 | repo, business plan |

## What a later round may do with this

Delete ONLY the ids the Owner approves from the table above, after taking a copy of
`data/vsb_entities/` first, and re-measure the entity counts the platform reports about itself
afterwards — those counts are what the prune is for.

_Generated 2026-10-05 23:40Z. Deletes nothing._
