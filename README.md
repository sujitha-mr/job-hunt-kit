# Evidence Resume Builder

A working prototype of a resume builder based on the supplied Microsoft 365 Copilot agent design: select one person's master profile, paste a job description, select relevant evidence, review, and download an ATS-friendly Word document.

## Run on Windows

Python 3.12 is recommended. From this repository in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

On Linux/macOS use `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`, and `.venv/bin/python -m streamlit run app.py`.

Open the local address printed by Streamlit. Start with the fictional profile and JD. Upload a UTF-8 Markdown profile to replace the example. Profiles must use `# Person Name`, `## Career Evidence`, `### Employer | Dates`, an optional `**Official role:**` line, and accomplishment bullets. Also supported: `## Experience`, `## Skills and Tools`, `## Skills`, `## Education`, and `## Certifications`. Other sections, including instructions and guardrails, are excluded from resume evidence. Reconcile contradictory facts before upload: the parser does not independently verify claims or resolve conflicts.

## Optional AI mode

Offline mode uses word overlap; it does not call an AI model. AI mode calls OpenAI to select source fact IDs. Both modes retain the exact evidence wording and career order; free-form AI rewriting is intentionally deferred. Invalid IDs fail validation. The application generates documents from the current profile only.

Set `RESUME_API_KEY` securely in the server process and optionally set `RESUME_MODEL` (default `gpt-4.1-mini`). Never commit keys or paste them into profile files. In hosted environments, use their secure variable settings. The API endpoint `api.openai.com` must be permitted by network policy. API billing is separate from ChatGPT/Codex subscriptions.

AI generation transmits career evidence and the job description to OpenAI. Contact lines are excluded from that request, but evidence may still contain identifying or sensitive information. The app does not write uploads or drafts to disk, but this is not a production privacy guarantee. Use a private local instance; no user authentication, durable profile storage, or multi-user authorization is implemented.

## What is validated

Evidence IDs and original wording are checked deterministically. A Word export uses one column, standard headings, selectable text, and no tables. Manual edits reset download approval and require factual review. Word extraction tests check content preservation. The evidence table is an audit aid, and JD word overlap is explicitly labelled as lexical matching; neither establishes semantic entailment. ATS parsing varies, and no ranking or interview outcome is guaranteed. No misleading numerical ATS score is displayed.

Changes to profile, JD, model or mode discard the previous draft from the interface. Multiple browser sessions are isolated by Streamlit session state; this is not a substitute for production account security. Clearing a session removes its active inputs and draft; files explicitly downloaded by the user remain on their machine.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Tests cover exclusion of unsupported qualifications, invalid evidence IDs, profile isolation, intake errors, the AI adapter with a mocked response, DOCX text preservation, and the interface review/export/reset flow. No real profile or credential is included in tests.

## Next increments

Structured evidence extraction and conflict handling; grounded paraphrasing with claim-level evaluation; semantic requirement mapping; visual resume/PDF exports; and profile management. Referral notes and the agent's scoring rubrics are not implemented in this first release.

See [architecture](docs/architecture.md) for implementation decisions.
