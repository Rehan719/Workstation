# Archived frontend pages

These React pages were moved out of `apps/workstation-superapp/src/pages/` during the **frontend
convergence to the IDBO Whole Vision** (W86). They were **not wired to any backend** — aspirational /
Phase-4 clusters (cosmic federation, orbital/interstellar, genome lab, DAO/sanctum governance, QEP
product portals, council/scholar/learner realms, etc.) — and were collapsed out so the product reads as
the eight vision sections.

**Nothing is deleted.** Files are preserved here with full git history. The live app keeps every
**backend-wired** page; only not-wired pages were archived.

## Restore a page
```bash
git mv _archive/frontend/pages/<sub>/<Name>.tsx apps/workstation-superapp/src/pages/<sub>/<Name>.tsx
```
Then re-add its `import` + `<Route>` in `apps/workstation-superapp/src/App.tsx` (and a Sidebar entry in
`src/components/layout/Sidebar.tsx` if it should appear in nav).

> Two pages (`synthesis/PresentationPlayer.tsx`, `synthesis/BusinessModelDashboard.tsx`) were initially
> moved then restored — they are imported by the kept `SynthesisStudio` page.

## Orphaned components (W88)
`_archive/frontend/components/` holds components that became **unreachable** after the page archive — a
reachability graph from `src/main.tsx` found them imported by no kept file (only by archived pages, or by
each other). Verified by `tsc && vite build` staying green after removal. Includes the unused `ui/*`
shadcn primitives (badge/button/card/input/progress/scroll-area/textarea — zero importers anywhere), the
QEP student-portal cluster (`QEPStudentPortal` + `HifzProgress` + `TajweedMeter`), several
`organism/*` visualisers, and others. Restore the same way (git mv back) and re-add the importer.

