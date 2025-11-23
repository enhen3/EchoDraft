# Repository Guidelines

This document defines how to organize code and collaborate in this repository.

## Project Structure & Module Organization

- Place implementation code in `src/`, grouped by feature or domain.
- Mirror `src/` in `tests/` (e.g., `src/auth/` ↔ `tests/auth/`).
- Use `scripts/` for automation (tooling, data tasks, release helpers).
- Keep documentation in `docs/` and static assets in `assets/`.

## Build, Test, and Development Commands

Prefer a small set of standard entry points, ideally via `Makefile`:

- `make install` – install all project dependencies.
- `make dev` – run the local development server or main CLI.
- `make test` – execute the entire test suite.
- `make lint` – run formatters and linters.

When adding language-specific commands (e.g., `npm test`, `pytest`), wire them into these targets.

## Coding Style & Naming Conventions

- Use 2-space indentation unless language tooling enforces otherwise.
- Favor clear, descriptive names (`UserSessionService`, `draft_to_markdown`) over abbreviations.
- Keep functions small and single-purpose; extract shared logic into utility modules.
- Configure and rely on language-idiomatic formatters/linters (e.g., Prettier, ESLint, Black).

## Testing Guidelines

- Co-locate tests in `tests/` following the `src/` structure.
- Name test files after the unit under test (e.g., `draft_parser_test.*`).
- Add or update tests with every behavior change; aim for high coverage on core modules.
- Ensure `make test` passes before opening a pull request.

## Commit & Pull Request Guidelines

- Use concise, imperative commit messages, ideally `type(scope): summary` (e.g., `feat(editor): support live preview`).
- Group related changes into a single PR; avoid mixing refactors with feature work.
- PR descriptions should include motivation, summary of changes, testing notes, and any relevant screenshots or logs.
- Reference issues using standard GitHub syntax (e.g., `Closes #42`).

## Agent-Specific Instructions

- Prefer minimal, focused diffs and keep changes consistent with existing style.
- Do not modify `AGENTS.md` unless explicitly requested.
- Update documentation and tests when changing user-visible behavior or APIs.

