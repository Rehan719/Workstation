# Workstation Documentation Style Guide (v137.1)

This document codifies the standards for all documentation within the Workstation ecosystem. Adherence to these rules ensures consistency, professional credibility, and usability for all participants in the Sentient Civilization Epoch.

## 1. Heading Hierarchy
- Use **ATX headings** (e.g., `# Heading 1`, `## Heading 2`).
- Always include a single space after the `#` symbols.
- Use Sentence case for headings (e.g., `## Technical compliance matrix`, not `## TECHNICAL COMPLIANCE MATRIX`).

## 2. Terminology and Brand Voice
- **VSB AI CEO**: Always refer to the VSB AI CEO as "VSB AI CEO" or "Jules" (in an executive context). Avoid "VSB AI CEO" in isolation.
- **Biomimetic OS**: Always capitalize.
- **Quad Engine Reactor**: Always capitalize.
- **Sovereign Intelligence**: Capitalize when referring to the state of the system.
- **Build-to-Order (BTO)**: Use this format for product line references.
- **Centers of Excellence (CoEs)**: Use this format for department references.

## 3. Versioning
- The current version is **v137.1** (or **v137.1.0** for semantic technical references).
- Use the format `vX.Y.Z` for specific releases.
- When introducing a new feature, explicitly note it: `*Introduced in v137.1*`.

## 4. Formatting Conventions
- **UI Elements**: Use **Bold** for buttons, menus, and screen names (e.g., "Click **Submit** on the **Dashboard**").
- **Code & Commands**: Use `inline backticks` for variables, file paths, and short commands. Use triple backtick blocks for code examples.
- **Notes & Warnings**: Use blockquotes for emphasis.
  > **Note:** Important supplementary information.
  > **Warning:** Critical safety or system stability information.

## 5. Visuals and Diagrams
- **Mermaid**: Use Mermaid for all architecture and flow diagrams to ensure they are searchable and editable.
- **Images**: Store images in `docs/assets/` and use relative paths. Always include descriptive Alt text.

## 6. Links
- **Internal**: Use relative paths (e.g., `[User Guide](USER_GUIDE.md)`).
- **External**: Verify all external links before committing. Use `markdown-link-check` if available.
- **Anchors**: Prefer standard GitHub-style anchors (lowercase-with-hyphens).

## 7. Documentation Layout
Every major guide should follow this structure:
1. Title (H1)
2. Executive Summary / Overview
3. Prerequisites (if applicable)
4. Main Content (H2/H3)
5. Troubleshooting / FAQs
6. Related Links

---
*Codified via Grand Synthesis Engine. Consistency is the foundation of civilization.*
