# 🐄 Dairy Hub API

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.4-009688.svg)
![uv](https://img.shields.io/badge/uv-fast-magenta.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Overview

Dairy Hub is a production-ready milk collection and billing system API. Designed for small to medium dairy cooperatives, it offers a robust backend for managing milk collection, offline-first environments, and simple deployment.

## Features

- **Zero-config Deployment**: Uses SQLite for extreme portability and offline readiness.
- **RESTful API**: Fast and modern API built with FastAPI.
- **Multiple Clients**: Supports web portals and standalone desktop clients.
- **Data Validation**: Strict schema enforcement using Pydantic.
- **Extensible**: Built with SQLAlchemy to easily scale to PostgreSQL in the future if needed.

## Architecture Overview

The system follows a classic three-tier architecture:
1. **Client Layer**: Communicates via HTTP/JSON.
2. **API Layer**: FastAPI handles routing, validation, and authentication.
3. **Data Layer**: SQLAlchemy ORM manages interactions with the SQLite database.

## Technology Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Database**: SQLite (default)

## Project Structure

```text
├── application-source/
│   ├── app/            # FastAPI application logic
│   ├── scripts/        # Database initialization & utilities
│   ├── tests/          # Pytest suite
│   ├── pyproject.toml  # Project dependencies and config
│   └── uv.lock         # Locked dependencies
├── codebuild/          # Deployment and infrastructure scripts
├── .github/workflows/  # CI/CD pipelines
└── README.md
```

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed globally (e.g., `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Using `uv`

This project uses `uv` for lightning-fast Python package management and virtual environment creation. It replaces traditional tools like `pip`, `venv`, and `poetry` with a single binary.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_ORG/python-dairy-hub-api.git
   cd python-dairy-hub-api/application-source
   ```

2. **Sync dependencies:**
   ```bash
   uv sync
   ```
   *This automatically creates a `.venv` directory and installs all dependencies specified in `uv.lock`.*

## Environment Variables

Copy `.env.example` to `.env` (if provided) and adjust as necessary. By default, the application is pre-configured to run out of the box using SQLite.

## Database Initialization

To initialize the SQLite database and run migrations, execute:
```bash
uv run init-db
```
*(Optional)* To seed the database with sample data:
```bash
uv run seed-db
```

## Running Locally

To start the local development server with hot-reloading:
```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Access the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Development Workflow

### Formatting
Code formatting is strictly enforced using `ruff`. To format the codebase:
```bash
uv run ruff format .
```

### Linting
To check for code quality and style issues:
```bash
uv run ruff check .
```

### Testing
Run the test suite using `pytest`:
```bash
uv run pytest
```

## Running the Application

For a production-like environment on your local machine, run Uvicorn with multiple workers:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Deployment

Deployment is automated via GitHub Actions (`.github/workflows/deploy.yml`). 
Upon merging to `main`, the deployment workflow executes `codebuild/create_app.sh` on the target server, pulling the latest code, syncing dependencies with `uv`, and automatically restarting the `systemd` service.

## Troubleshooting

- **`uv` command not found**: Ensure `uv` is installed and added to your system's `PATH`.
- **Database Locked Errors**: Ensure multiple processes aren't attempting to write to the SQLite file simultaneously.
- **VS Code Interpreter**: Open the `application-source` directory, and VS Code should automatically detect the `uv` virtual environment at `application-source/.venv`.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Ensure all linting and tests pass (`uv run ruff check .` and `uv run pytest`).
5. Push to the branch (`git push origin feature/amazing-feature`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
