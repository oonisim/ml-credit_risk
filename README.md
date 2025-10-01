# FEAST Tutorial (Local Quickstart)

This tutorial guides you through using [FEAST](https://feast.dev), an open‑source
feature store for machine learning. See FEAST Documentation: https://docs.feast.dev for more details.

You will: 
1. Set up local infrastructure
2. Create features and materialize them to the offline store.
3. Register features to the registry database.
4. Consume features for model training.


---

## What is FEAST

FEAST is a feature store that lets you define features once and use them for training and inference.

Key concepts :
- Offline store: Where batch feature data lives (using PostgreSQL in this tutorial).
- Feature View: A group of features from an offline feature table that are served together.
- Registry Database: Metadata store tracking all FEAST objects.

---

# Repository Layout

```text
.
├── deploy.sh
├── destroy.sh
├── deployment
│   ├── infra                          <--- Tutorial environment setup scripts
│   │   └── sh
│   │       ├── os/   (os-specific setup script directory)
│   │       ├── _config.sh
│   │       ├── deploy.sh
│   │       ├── destroy.sh
│   │       ├── start_postgresql_container.sh
│   │       ├── stop_postgresql_container.sh
│   │       ├── create_registry_database.sh
│   │       └── create_offline_store_database.sh
│   ├── feast                          <---- FEAST SDK and feature repository
│   │   └── feature_repository
│   │       ├── data/                       <--- FEAST artefacts (e.g., online store)
│   │       ├── deploy.sh
│   │       ├── destroy.sh
│   │       ├── features.py                 <--- Feature definitions 
│   │       └── feature_store.yaml.template <--- FEAST config (registry, offline store, online store)
│   └── test
├── python                             <--- Python package installation
│   ├── requirements.txt
│   └── install_python_packages.sh
├── notebook                           <--- FEAST tutorial notebooks
│   ├── eda.py                              <--- EDA code
│   ├── feature_engineering.py              <--- Feature engineering code
│   ├── evaluation.py                       <--- Model evaluation code
│   ├── 01-credit-risk-model-feature-engineering.ipynb
│   ├── 02-credit-risk-model-feature-registration.ipynb
│   └── 03-credit-risk-model-feature-consumption.ipynb
├── data
│   └── raw
│       └── german_credit_data.csv          <--- Credit risk dataset
└── README.md
```

---
# Deploy Tutorial Environment

## Prerequisites

- MacOS or Linux with:
  - Git
  - Python 3.10+ (tested with 3.11)
  - pip (or conda) and virtual environments
  - Docker (for local PostgreSQL container)
- Package Manager: Homebrew for MacOS, apt for Ubuntu, yum or dff for RHEL/CentOS/Amazon Linux.

## 1) Clone and enter the project

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

## 2) Deploy local infrastructure

Brings up local infrastructure (e.g., PostgreSQL Docker conainer for offline and registry databases).
The script will prompt for a PostgreSQL admin password (or set `POSTGRES_PASSWORD` environment variable first).

```bash
# Option A: let the script prompt for a password
chmod u+x ./deploy.sh
./deploy.sh

# Option B: set the env var up front
export POSTGRES_PASSWORD='<your-strong-password>'
chmod u+x ./deploy.sh
./deploy.sh
```

## 3) Create and activate a Python virtual environment

Using pip venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Using conda:
```bash
conda create -n feast-tutorial python=3.11 -y
conda activate feast-tutorial
```

## 4) Install Python dependencies

```bash
chmod u+x ./python/install_python_packages.sh
./python/install_python_packages.sh
```

## 7) Run Tutorial

Start Jupyter:
```bash
python -m notebook
```

Open the notebooks in the `notebook/` directory to explore:
- 01: feature engineering
- 02: feature registration with FEAST
- 03: feature consumption online

PDF versions are included for quick reference.

## 8) Tear down

```bash
./destroy.sh
```

This stops and removes local infra and FEAST artifacts created by the deployment scripts.

---

## Troubleshooting

- psycopg2 installation build errors on macOS:
  ```bash
  brew install openssl && brew link openssl
  ```
  Then re‑run:
  ```bash
  pip install -r python/requirements.txt
  ```
- Ensure Docker is available before `./deploy.sh`.
- If `POSTGRES_PASSWORD` was exported for the session, you can unset it:
  ```bash
  unset POSTGRES_PASSWORD
  ```

---

## Learn more

- Website: https://feast.dev
- Docs: https://docs.feast.dev
- GitHub: https://github.com/feast-dev/feast
