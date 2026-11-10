# playwright-framework

## Local setup (Windows)

Use Python 3.13 or newer. From the repository root, create and activate a virtual
environment, then install the project and its requirements:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e . -r requirements.txt
python -m playwright install chrome
```

Set `LOGIN_URL`, `LOGIN_USERNAME`, and `LOGIN_PASSWORD` in `config/.env.qa` (or
override them in `config/.env.qa.local`). Keep real credentials in the local
override file and do not commit them. The UI tests use the configured login site.

Run the test suite from the repository root:

```powershell
python -m pytest
```

To select another configured environment, pass `--env stage` or `--env prod`.
