# Quran Education Platform (QEP) Mobile Architecture Pattern
## Domain: RELIGION::QEP::DEVELOPER

### 1. Overview
The QEP Mobile App is designed as a React Native application, leveraging the same design principles as the Workstation Sovereign Ecosystem. It provides students with access to the curriculum, progress tracking, and the Ijazah database on the go.

### 2. Core Components
- **LessonCard.tsx**: Reusable component for displaying lesson information and progress.
- **ProgressRing.tsx**: Specialized SVG-based ring for visualizing Hifz and Tajweed metrics.
- **AppNavigator.tsx**: Tab-based navigation system for switching between Curriculum, Hifz, and Profile.

### 3. Integration Points
- **API Connector**: Communicates with the `LMSIntegration` API defined in v8.0.
- **Authentication**: Uses the VSB-compatible JWT authentication flow.
- **Local Cache**: Caches lesson content for offline recitation practice.

### 4. Extension Guide
To add a new screen:
1. Create the screen component in `screens/`.
2. Register the screen in `navigation/AppNavigator.tsx`.
3. Define the data fetching logic in `hooks/useQEPData.ts`.

---
**Status:** Pattern Definition | **Last Updated:** 2026-04-01
