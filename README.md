# chatops

Chat for Operations teams

## CLI Usage

The CLI is built with [Typer](https://typer.tiangolo.com/). After installing the dependencies you can run the application with:

```bash
python -m chatops
```

### Rollback Deployments

To rollback to the last successful deployment for an app and environment:

```bash
python -m chatops deploy rollback APP ENV
```

### Folder Structure

```
chatops/
├── chatops/            # Python package
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── cost.py
│   ├── deploy.py
│   ├── incident.py
│   ├── logs.py
│   ├── security.py
│   └── cve.py
└── README.md
```

### Latest CVEs

To display recent high or critical vulnerabilities published in the last week:

```bash
python -m chatops cve latest
```
