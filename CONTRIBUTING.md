## Engineering Standard: Git Workflow & Commit Convention

To ensure **Code Integrity**, **Traceability**, and alignment with **Industry Best Practices**, the following protocol is mandatory for all contributors to the repository. This system is designed to facilitate seamless collaboration and professional-grade version control.

---

### 1. Branch Naming Strategy
Branches must follow a strict prefix-based naming convention to categorize the intent of the changes. Avoid generic names; be descriptive.

* **feat/**: New functional requirements or features. (e.g., feat/auth-integration)
* **fix/**: Resolutions for bugs or technical glitches. (e.g., fix/header-overflow)
* **refactor/**: Code changes that neither fix a bug nor add a feature (e.g., improving performance).
* **docs/**: Changes to documentation only.
* **chore/**: Maintenance tasks, updating dependencies, or configuration changes.
* **research/**: Experimental work or data science notebooks/explorations.

---

### 2. Commit Message Structure
We adhere to the **Conventional Commits** specification. Every commit message must be structured as follows:

`type(scope): description`

#### Standard Types:
* **feat**: A new feature.
* **fix**: A bug fix.
* **docs**: Documentation changes.
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc).
* **refactor**: A code change that neither fixes a bug nor adds a feature.
* **perf**: A code change that improves performance.
* **test**: Adding missing tests or correcting existing tests.

#### Examples:
* feat(api): implement fastapi router for sensor telemetry
* fix(ui): correct color mapping for critical alert status
* refactor(ds): optimize preprocessing pipeline for real-time inference
* chore(deps): upgrade pydantic to version 2.0

---

### 3. Integration Workflow (Pull Request Protocol)
To maintain a stable codebase, the following workflow is strictly enforced:

1. **Isolation**: All work must be performed in a dedicated branch branched off develop.
2. **No Direct Commits**: Direct commits to main or develop are prohibited.
3. **Mandatory Peer Review**: Every Pull Request (PR) requires at least one approval from a team lead or peer before merging.
4. **Atomic Commits**: Commits should be granular and represent a single logical change. This simplifies the rollback process if a regression occurs.
5. **Conflict Resolution**: It is the contributor's responsibility to rebase or merge the latest develop into their feature branch and resolve conflicts before requesting a review.

---

### 4. Rationale
Implementation of this standard serves three primary objectives:
1. **Automated Versioning**: Enables the use of automated tools to generate changelogs and manage semantic versioning.
2. **Scalability**: Ensures the repository remains manageable as the team and codebase grow.
3. **Professionalism**: Demonstrates a high level of technical discipline to external stakeholders and recruiters.