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

### Fetch AWS Logs

Retrieve recent log events from AWS CloudWatch:

```bash
python -m chatops logs aws SERVICE --log-group LOG_GROUP --log-stream LOG_STREAM
```

If the log group or stream are not provided, the CLI will prompt for them interactively.

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
└── README.md
```

### Latest CVEs

To display recent high or critical vulnerabilities published in the last week:

```bash
python -m chatops cve latest
```
