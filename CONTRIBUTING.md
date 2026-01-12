# Contributing to iLovePDF Python Library

Thank you for your interest in contributing to the iLovePDF Python library!
We welcome contributions from the community to improve features, documentation, tests, and overall quality.

---

## How to Contribute

1. **Fork the repository**
   Click the "Fork" button at the top right of the GitHub page to create your own copy.

2. **Clone your fork**
   ```
   git clone https://github.com/<your-username>/ilovepdf-python.git
   cd ilovepdf-python
   ```

3. **Create a new branch**
   ```
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   - Follow the project structure and coding conventions.
   - Add or update tests as needed.
   - Update documentation if your change affects usage or APIs.

5. **Test your changes**
   Run unit and integration tests:
   ```
   pytest tests/unit
   pytest tests/integration
   ```

6. **Commit your changes**
   - Use clear and concise commit messages.
   - Follow the commit message guidelines in `AGENT.md`.

7. **Push to your fork and open a Pull Request**
   - Go to your fork on GitHub and click "Compare & pull request".
   - Fill in the PR template and describe your changes.

---

## Guidelines

- **Code Style:**
  - Use PEP8 formatting.
  - Type annotations are required for public methods.
  - Use English for code comments and documentation.

- **Tests:**
  - All new features and bug fixes must include relevant unit and/or integration tests.
  - Test files should be placed in `tests/unit/` or `tests/integration/` as appropriate.

- **Documentation:**
  - Update or add docstrings for new modules, classes, and functions.
  - Update the relevant README files if your changes affect usage or coverage.

- **Samples:**
  - If you add a new Task module, provide at least one sample script in `samples/` and document it in `samples/README.md`.

- **Environment:**
  - Ensure your code works with Python >= 3.9.
  - Use Docker for development and testing if possible (see `.docker/README.md`).

---

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub.
Include as much detail as possible, including steps to reproduce, expected behavior, and environment information.

---

## Code of Conduct

Please review and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming and respectful environment for all contributors.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make iLovePDF Python better!
