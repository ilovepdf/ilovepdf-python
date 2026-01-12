# Live Samples (`samples/live/`)

This folder contains **live/manual test scripts** for the iLovePDF Python library. These scripts are designed to execute real workflows against the actual iLovePDF API using real credentials and files.

---

## Purpose

- **Manual validation:** Run real end-to-end flows to verify the library's integration with the iLovePDF API.
- **Debugging:** Quickly reproduce and debug issues that may not appear in unit or integration tests.
- **Demonstration:** Show real usage scenarios with actual API responses and files.

---

## Important Notes & Warnings

- **Not for automated testing:** These scripts are **not** intended for CI/CD or automated test pipelines.
- **Requires real credentials:** You must provide valid API keys and real sample files.
- **Never commit secrets:** Do **not** hardcode or commit sensitive credentials or data in these scripts.
- **May incur API usage:** Running these scripts will consume API quota and may generate real documents or trigger billing, depending on your iLovePDF account.

---

## How to Use

1. **Set up your environment:**
   - Ensure your API credentials are set via environment variables or a `.env` file.
   - Place any required sample files in the appropriate locations (see script comments).
   - **Create the `output_live` folder in the project root if it does not exist.** Many live samples will attempt to download their results to this folder. You can create it with:
     ```
     mkdir output_live
     ```

2. **Install dependencies:**
   - From the project root, run:
     ```
     pip install -r ../requirements.txt
     ```

3. **Run a live sample:**
   - From the project root, execute:
     ```
     python samples/live/<script_name>.py
     ```

4. **Review results:**
   - Output files will be saved as specified in each script.
   - Check the script output and any generated files for results.

---

## Folder Policy

- Scripts here should be kept up-to-date with the main library API.
- Do **not** include confidential or customer data.
- Document any special requirements or setup in the script or here.

---

## When to Use Live Samples

- When you need to verify the library with the real iLovePDF API.
- For advanced debugging or troubleshooting.
- To demonstrate real-world flows to collaborators or stakeholders.

---

For standard usage examples, see the parent [`samples/`](../) folder. For automated tests, see [`tests/`](../../tests/).

---