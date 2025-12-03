# 📡 DMS URL Health Monitor

![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![CI](https://github.com/pgworksonline/dms-url-health-monitor/actions/workflows/ci.yml/badge.svg)
![Code Style](https://img.shields.io/badge/code%20style-flake8-blue)
---
A DevOps-focused Python tool for automated website health monitoring, uptime validation, content verification, latency measurement, and CI-driven reliability testing.
This project demonstrates real-world DevOps, automation, observability, and Python engineering skills.
## 🛠️ Features
- Multi-page URL monitoring
- Response-time measurement
- Expected-text validation
- Structured logging (INFO / WARNING / ERROR)
- GitHub Actions CI workflow
- Clean, config-driven architecture
- Optional cron-based automation
## 📁 Project Structure
```
.
├── monitor.py
├── urls.json
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```
## 🧩 Configuration (urls.json)
[
  {
    "name": "Home Page",
    "url": "https://designersmovingservice.com",
    "expected_text": "For a seamless and stress-free move"
  }
]
---

## 📐 Architecture Diagram
```
                   ┌────────────────────────┐
                   │       urls.json         │
                   │ (List of URLs + text)   │
                   └─────────────┬──────────┘
                                 │
                                 ▼
                     ┌───────────────────┐
                     │     monitor.py     │
                     │     main()         │
                     └──────────┬─────────┘
                                │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
   ┌─────────────────┐  ┌───────────────┐  ┌─────────────────┐
   │  check_url()     │  │ requests.get() │  │ logging module  │
   │ - HTTP status     │  │ - fetch page  │  │ - INFO/WARN/ERR │
   │ - expected text   │  │ - timeout     │  │ - logs output   │
   │ - latency (ms)    │  └───────────────┘  └─────────────────┘
   └─────────────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Summary evaluation   │
                     │  All good? Yes/No    │
                     └──────────┬───────────┘
                                │
                         ┌──────┴───────┐
                         ▼              ▼
           ┌───────────────────┐   ┌────────────────────┐
           │ logging.info()    │   │ logging.warning()  │
           │ Healthy ✔️         │   │ Issues found ⚠️     │
           └───────────────────┘   └────────────────────┘
```
---
## 🚀 GitHub Actions CI Workflow
```yaml
name: CI

on:
  push:
    branches: [ "main", "dev" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repo
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 monitor.py || true

    - name: Run basic syntax check
      run: |
        python -m py_compile monitor.py
```
---
## 🎯 Skills Demonstrated
DevOps / SRE
- Service health monitoring
- Log-based observability
- CI pipeline integration
- Cron automation
- Failure detection & reporting

Python Engineering
- Exception handling
- Modular function design
- HTTP requests & timeouts
- Logging
- JSON configuration
---

## 📬 Contact
Feel free to open an issue or submit a PR.
