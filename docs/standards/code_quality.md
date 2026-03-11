# Workstation Code Quality Standards

## 1. Correctness & Robustness
- **Functional Integrity**: Code must fulfill the stated requirements of the relevant Constitutional Article.
- **Error Handling**: Graceful failure modes using custom exceptions and detailed logging.
- **Type Safety**: Mandatory type hints for all public functions/methods (Python 3.12+ style).

## 2. Security (Inspired by Microsoft SDL & OWASP)
- **Input Validation**: Strict validation of all external inputs (URLs, file paths, user data).
- **Secrets Management**: Absolute prohibition of hardcoded secrets; use `.env` and `SecretsManagerAgent`.
- **Least Privilege**: Components must operate with minimum necessary permissions.

## 3. Performance & Scalability (Inspired by NVIDIA & Tesla)
- **Asynchronous Execution**: High-latency operations (synthesis, ingestion) must be non-blocking.
- **Resource Efficiency**: Optimized data structures; minimal memory leaks.
- **Concurrency**: Flawless thread synchronization in the Meta-Pipeline.

## 4. Maintainability & Design (Inspired by Google & Apple)
- **Modularity**: Strict separation of concerns (Engines vs. Orchestrators vs. Interfaces).
- **Naming**: Descriptive, consistent, and semantically meaningful identifiers.
- **Documentation**: Google-style docstrings; up-to-date READMEs for every module.
- **DRY & SOLID**: Adherence to core engineering principles.

## 5. Purpose Alignment (The Conscious Entity Standard)
- **Dual Purpose Compliance**: Logic must not violate spiritual-ethical aspirations or operational mission.
- **PAS Integration**: Critical logic paths should be traceable to Purpose Alignment Scores.
