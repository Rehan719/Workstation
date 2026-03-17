# DESIGN.md – Workstation v138.0 Unified App

## 1. Brand Identity
The Workstation application is the primary interface to a multi-agentic, biomimetic AI ecosystem. The design must reflect:
- **Sophistication**: Professional-grade interface for high-stakes decision-making.
- **Biomimetic Elegance**: Use of organic, fluid motions and patterns that hint at the "Living Ecosystem Core".
- **Sovereign Authority**: A layout that empowers the user as the "Conscious Entity Guardian".

## 2. Color Palette
- **Primary (Sovereign Blue)**: `#020617` (Deepest Navy / Slate 950)
- **Accent (Aura Cyan)**: `#38bdf8` (Sky 400)
- **Highlight (Amber Gold)**: `#fbbf24` (Amber 400)
- **Status (Vital Green)**: `#10b981` (Emerald 500)
- **Text (Luminous White)**: `#f8fafc` (Slate 50)
- **Subtext (Faded Slate)**: `#64748b` (Slate 500)

## 3. Typography
- **Primary**: `Inter` or `Geist` (Sans-serif)
- **Headings**: `Inter` Black (900) with tight tracking (`-0.02em`)
- **Monospace**: `JetBrains Mono` or `Fira Code` (for logs, metrics, and terminal views)

## 4. Design Patterns
- **Glassmorphism**: Use of `backdrop-blur-xl` and semi-transparent backgrounds (`bg-slate-900/80`) to create depth.
- **Micro-interactions**: Subtle `framer-motion` animations for page transitions and card hovers.
- **Role-Based Layouts**:
  - **VSB AI CEO**: Central command hub, high-level summaries.
  - **C-Suite**: Departmental metrics, deep-dive data tables.
  - **CoEs**: Content-rich knowledge base, search-centric.
  - **BTO**: Product configuration wizards, 3D/visual previews.

## 5. Mobile Interface
- **First-class Experience**: Not just a responsive web app, but a native-feel Expo application.
- **Bottom Navigation**: Persistent access to Dashboard, Reactors, Knowledge, and Profile.
- **Biometrics**: Integration with FaceID/Fingerprint for the "Sovereign Handshake".
