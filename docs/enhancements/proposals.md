# v138.1 Enhancement Proposals

## Proposal 001: Visual Fidelity & CSS Normalization
- **Objective**: Ensure the "Sophisticated & Professional" brand identity renders consistently across all environments.
- **Approach**: Normalize `postcss.config.js`, update Tailwind content paths to include `packages/ui`, and refine glassmorphism utility classes.
- **Impact**: High (Aesthetic alignment and brand trust).

## Proposal 002: Dynamic BTO Configuration Engine
- **Objective**: Evolve the BTO Catalog from a static view to an interactive "Build-to-Order" experience.
- **Approach**: Create a `BTOConfigurator` component that maps `btoProducts.json` options to a dynamic form. Implement order state management in the backend.
- **Impact**: High (Commercialization & User Empowerment).

## Proposal 003: Mobile Native Handshake
- **Objective**: Provide a premium native experience on iOS/Android.
- **Approach**: Integrate `expo-local-authentication` for Biometric Login and `expo-notifications` for system alerts.
- **Impact**: Medium (Mobile UX & Security).

## Proposal 004: UI Component Centralization
- **Objective**: Reduce technical debt and enable recursive development.
- **Approach**: Migrate reusable layout and UI components (Buttons, Cards, Modals) from `apps/web` to `packages/ui`.
- **Impact**: High (Maintainability & Scalability).
