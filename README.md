# ResumeForge

ResumeForge is a downloadable portfolio project for tailoring a resume from one person's master profile and a target job description. Run the Streamlit app locally for review and Word export, or use the Markdown agent kit in an assistant you already use.

[Download the source ZIP](https://github.com/sujilearnsdatascience/job-hunt-kit/archive/refs/heads/main.zip) · [Watch or download the fictional-data demo](docs/demo/resumeforge-offline.mp4?raw=true)

## Markdown agent kit

### Create your agent once

1. In **ChatGPT**, create a custom GPT named **ResumeForge** and open its **Instructions** field. In **Claude**, create a Project named **ResumeForge** and open **Set project instructions**. In other assistants, look for a custom agent or workspace with persistent instructions. Feature availability depends on your account.
2. Copy the [ResumeForge agent instructions](agent-kit/INSTRUCTIONS.md) into that field and save the agent for private use. If the builder supports conversation starters, add `Tailor my resume to this job description.`
3. Fill in the [blank master profile template](agent-kit/profile-template.md) with verified facts and remove unused placeholders. Keep it locally and attach it per run, or upload it once to the agent’s private knowledge if you are comfortable storing it with that provider. Keep only one person’s profile in an agent. Review sharing and data settings before uploading personal information.

### Use it for each job description

Open your saved ResumeForge GPT, or start a new chat inside your ResumeForge Project. Use a fresh conversation for each role. Send the message below and paste the full job description. Attach your master profile if you did not save it with the agent.

```text
Tailor my resume to this job description.

Job description:
[Paste the full job description here.]
```

Review the Markdown draft and the evidence gaps before using it. Test the setup with the [fictional master profile](examples/profile.md) and [fictional job description](examples/job-description.txt). The fictional applicant’s unsupported PMP and Kubernetes qualifications should appear only in the gap review. If your assistant lacks persistent instructions, paste the agent instructions into a new chat with the profile and JD. The kit itself requires no API key.

## Install and run locally

Download and extract the source ZIP, or clone `https://github.com/sujilearnsdatascience/job-hunt-kit.git`. Open a terminal in the project directory. Python 3.12 is recommended.

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1
```

**macOS or Linux**

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py --server.address 127.0.0.1
```

Open the address printed by Streamlit. Stop the app with Ctrl+C.

## Workflow

1. Keep the fictional profile and JD for a first run, or upload a UTF-8 Markdown profile and paste your target JD. Use `# Full name`, `## Career Evidence`, and `### Employer | Dates`, with `**Official role:**` and accomplishment bullets. The [template](agent-kit/profile-template.md) includes the supported optional sections.
2. Select **Offline demo** and click **Build evidence-based draft**. Offline selection uses word overlap and requires no account or API key.
3. Review **Evidence & gaps**, then edit the draft as needed in **Resume editor**. The audit table traces the original selection. Review any edits separately. Changes to the profile, JD, mode, or model discard the existing draft.
4. Approve the reviewed draft and select **Download Word resume** or **Download Markdown**. Edits reset download approval. **Clear session** clears the active inputs and draft. Keep or delete downloaded files separately.

### Optional OpenAI mode

Select **AI evidence selection** and enter your own OpenAI API key in the password field. You can alternatively set `RESUME_API_KEY` in the local server process. The model defaults to `gpt-4.1-mini` and can be changed in the sidebar or via `RESUME_MODEL`. API usage requires an API account, model access, billing, and connectivity to `api.openai.com`. ChatGPT subscriptions and API billing are separate.

The model selects source fact IDs. The app validates the IDs against the current profile and renders the original wording in source order. Both modes preserve source wording. Bullet rewriting is outside the current scope.

## Architecture and tech stack

Streamlit handles the local interface and session state in `app.py`. The Python module `resume_builder.py` parses supported Markdown sections, assigns fact IDs, selects evidence, validates the selection, and renders the draft. The OpenAI Python SDK handles optional model calls. `python-docx` creates the single-column Word export with selectable text. Markdown downloads use the reviewed editor text. Pytest covers the core workflow and a mocked OpenAI response. Playwright and Chromium exercise the running app. See [architecture](docs/architecture.md) for the data flow.

## Privacy and limitations

Offline selection runs locally. The app keeps uploads and drafts in session state and generates exports when requested. OpenAI mode sends career evidence and the JD to OpenAI. The request omits parsed contact fields, though evidence and the JD can still contain identifying text. The Markdown kit shares whatever you submit with the assistant provider. Keep real profiles, resumes, and API keys out of version control. Use fictional data for public screenshots and demos.

ResumeForge is intended for private local use. It has no login or durable profile store. The parser trusts the facts supplied by the user and cannot resolve conflicting claims. Offline word overlap and the evidence table can miss relevant experience or surface irrelevant matches. Manual edits require a factual review. Word formatting uses standard headings and a single column, and ATS behavior varies by employer. The app makes no ranking or interview guarantees.

## Tests

From the project directory, use your virtual environment's Python (`.venv/bin/python` on macOS/Linux or `.\.venv\Scripts\python.exe` on Windows):

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

With the app running on port 8501, the Linux browser smoke test uses Chromium at `/usr/bin/chromium`:

```bash
.venv/bin/python tests/browser_smoke.py
```

The automated suite uses mocked AI responses. The browser test and recorded demo use fictional data in offline mode. These checks do not establish live API access, model availability, or billed request behavior.
