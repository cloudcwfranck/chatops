# chatops

Chat for Operations teams

## CLI Usage

The CLI is built with [Typer](https://typer.tiangolo.com/). After installing the dependencies you can run the application with:

```bash
python -m chatops
```

### IAM Checks

To list IAM users and highlight those with admin-level permissions:

```bash
python -m chatops iam check
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
│   ├── iam.py
│   └── security.py
└── README.md
```
