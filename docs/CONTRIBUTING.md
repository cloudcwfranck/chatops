# Contributing to ChatOps

Thank you for helping improve this project! This document describes the workflow for new contributors.

## Getting Started

1. Fork the repository on GitHub and clone your fork.
2. Create a virtual environment and install dependencies in editable mode:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
3. Install any additional development tools you might need (e.g. `black` or `flake8`).

## Branch Workflow

- Work from the `main` branch and create a feature branch for your change:

  ```bash
  git checkout -b my-feature
  ```
- Keep your branch focused on a single set of related changes.
- Format your code with `black` and follow PEP 8 conventions.
- Write or update tests under `tests/` and make sure they pass with `./test.sh`.

## Commit Messages

- Use clear, present‑tense messages (e.g. "Add deploy command tests").
- Reference GitHub issues when applicable, e.g. `Fixes #42`.
- Squash small fixups locally before opening a pull request.

## Pull Requests

1. Push your branch to your fork and open a pull request against `main`.
2. Verify that GitHub Actions runs succeed.
3. Fill out the pull request template checklist.
4. Be responsive to review feedback and update your branch as needed.

## Opening Issues

If you encounter a bug or have a feature request, open an issue describing:

- A clear title and summary
- Steps to reproduce or motivation for the feature
- Expected versus actual behavior

## Code of Conduct

All contributors are expected to follow the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Be respectful and inclusive in all interactions.

---
Happy hacking!
