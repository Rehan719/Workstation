// W579 (FU-352) — the frontend test runner's setup.
//
// Until now every page guard in the Python suite was a TEXT SCAN: 81 tests read a .tsx file and assert
// by substring, and 295 `data-testid` attributes existed for a renderer that did not exist. A substring
// scan is not worthless — one caught the `{false && …}` class in W577, where a render was switched off
// while its field name survived in the source — but it cannot tell whether a component actually renders
// anything, and P2.18's clause (b) is that an instrument says what it is.
//
// This file is the minimum that makes a render real: jest-dom's matchers, and cleanup between tests so
// one test's DOM cannot satisfy the next one's assertion.
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
