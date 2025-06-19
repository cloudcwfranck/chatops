# chatops

Chat for Operations teams

## CLI Usage

The CLI is built with [Typer](https://typer.tiangolo.com/). After installing the dependencies you can run the application with:

```bash
python -m chatops
```

### Suggest a CLI Command

The package exposes a helper function `suggest_command` that uses OpenAI
embeddings to map a natural language request to the most relevant ChatOps
CLI command:

```python
from chatops import suggest_command

cmd = suggest_command("restart app on prod")
print(cmd)  # -> "deploy deploy APP ENV" or similar
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
│   └── security.py
└── README.md
```
