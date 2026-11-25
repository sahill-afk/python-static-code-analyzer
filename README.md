# Python Static Code Analyzer

A focused Streamlit code review tool for identifying Python syntax, quality, security, and complexity concerns. The Streamlit interface runs in a browser on desktop and mobile. Analysis is static: submitted source is parsed and inspected, never executed, and is not intentionally persisted by this application.

## Features

- Paste Python code or upload a `.py` file (maximum 1 MB).
- Syntax diagnostics, unused and undefined names, naming and maintainability checks.
- Bandit security findings and explicit checks for dynamic code execution patterns.
- Radon cyclomatic complexity by function and method.
- Severity counts, a documented quality score, and detailed explanations and suggestions.
- Downloadable PDF and CSV reports.
- Responsive Streamlit interface with the existing focused code analyzer design.
- Native Tkinter desktop launcher is also retained as `desktop_app.py`.

## Objectives

- Help students and developers review Python code with understandable findings.
- Demonstrate modular static analysis using Python AST and established analysis libraries.
- Produce readable, exportable reports without executing submitted source.

## Technologies

- Python 3.10+
- Streamlit for the browser interface
- Python `ast`, Pyflakes, Bandit, and Radon for analysis
- ReportLab for PDF reports and the standard `csv` module for CSV reports
- Tkinter for the optional native desktop interface

## Run locally

Create and activate a virtual environment, then install dependencies:

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Start the Streamlit app:

```bash
python -m streamlit run app.py
```

To launch the optional native desktop version instead:

```bash
python desktop_app.py
```

## Use the analyzer

1. Open **Code Analyzer** from the home screen or select **Start Code Analysis**.
2. Paste Python source or upload a UTF-8 `.py` file up to 1 MB.
3. Select **Analyze Code** and review the summary and detailed findings.
4. Download PDF or CSV reports after a completed analysis. Use **Clear Code** to reset the editor and current results.

Invalid syntax is reported with its parser line and message; syntax-dependent checks are skipped when parsing fails. Empty source and invalid uploads receive a clear validation message.

### Quality score

The score starts at 100 and deducts a fixed amount per finding: Critical 25, High 15, Medium 8, Low 3, Info 0. It is clamped to 0–100. Invalid syntax receives 0 because the remaining checks cannot reliably analyze an invalid program. This score is an educational review aid, not a security certification.

## Project structure

```text
.
├── .github/workflows/ci.yml     # Automated tests and static checks
├── .gitignore
├── .streamlit/config.toml       # Streamlit theme and upload size
├── LICENSE                      # MIT License
├── README.md
├── app.py                       # Streamlit Community Cloud entry point
├── desktop_app.py               # Optional native desktop launcher
├── requirements.txt
├── src/
│   ├── analyzer/                # Analysis orchestration, quality, security
│   ├── reports/                 # PDF and CSV report generation
│   ├── ui/                      # Streamlit components and desktop interface
│   └── utils/                   # Input validation and result models
└── tests/                       # Analyzer and report tests
```

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py desktop_app.py src tests
python -m pyflakes app.py desktop_app.py src tests
```

## Limitations and privacy

- Static checks can produce false positives and cannot prove code safe or correct.
- Undefined-name analysis cannot resolve every dynamic import, runtime monkey-patch, or project-wide relationship.
- The analyzer handles individual files up to 1 MB; it does not scan folders, perform type checking, or autofix code.
- Submitted code is never executed. Analysis runs in memory; no user code is intentionally written to disk or sent to a third-party analysis service.
- Community Cloud hosts the app publicly. Do not submit confidential or sensitive source code to a public demo.
- Bandit and other rules are best-effort checks and are not a replacement for a full security review.

## Publish on GitHub

1. Create an empty GitHub repository (do not initialize it with a second README or license).
2. In this project folder, inspect the files before staging and push the project:

   ```bash
   git status --short
   git add .
   git status
   git commit -m "Prepare Python Static Code Analyzer for deployment"
   git remote add origin https://github.com/YOUR_USERNAME/python-static-code-analyzer.git
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` and the repository name. This workspace already has a local Git repository on `main`. If you are uploading a downloaded source archive without `.git`, initialize it with `git init -b main` first. Review the staged list; never commit `.env`, Streamlit secrets, credentials, virtual environments, or private source files.

## Deploy on Streamlit Community Cloud

1. Push the project to GitHub as above and make the repository public if you want anyone to inspect the source. Community Cloud also supports private repositories when authorized.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and grant access to the repository.
3. Choose **Create app**, select the repository and `main` branch, and set the entrypoint to `app.py`.
4. Optionally choose a memorable custom subdomain, then select **Deploy**.
5. Wait for the build to complete, open the resulting `*.streamlit.app` address, and test it on mobile and desktop. Share that URL once it loads successfully.

The root `requirements.txt` and `.streamlit/config.toml` are included for the cloud build. Streamlit Community Cloud monitors the GitHub repo and redeploys when you push changes. Deployment is not complete until you perform these account-based steps and verify the resulting public URL.

For the current deployment workflow, see the [Streamlit Community Cloud deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## License

Distributed under the MIT License. See [LICENSE](LICENSE).
