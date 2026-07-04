---
title: Document Intelligence Platform
emoji: 🧾
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Document Intelligence Platform

[![CI Status](https://github.com/<YOUR_GITHUB_USERNAME>/Document-Intelligence-Platform/actions/workflows/ci.yml/badge.svg)](https://github.com/<YOUR_GITHUB_USERNAME>/Document-Intelligence-Platform/actions/workflows/ci.yml)

Production-grade AI-powered document intelligence platform that extracts structured data from emails and multi-format documents using LLMs, validates extracted information through deterministic business rules, performs cross-document verification, and automates business workflow decisions.

## CI/CD Pipeline & Deployment

This repository includes automated CI/CD workflows using GitHub Actions:

- **CI (`ci.yml`)**: Runs automatically on every push and pull request. It checks out the code, installs Python dependencies, runs the test suite (`pytest`), and verifies that the Docker image builds successfully.
- **CD (`deploy.yml`)**: Runs automatically when code is pushed to the `main` branch. It pushes the codebase to Hugging Face Spaces using Git.

### Required GitHub Configuration

To enable the deployment to Hugging Face Spaces, configure the following in your GitHub repository settings:

**Repository Secrets** (Settings > Secrets and variables > Actions > Secrets):
- `HF_TOKEN`: Your Hugging Face access token with Write permissions.
- `MONGODB_URI`: MongoDB connection string (needed for tests if not mocked).
- `GROQ_API_KEY`: Groq API key (needed for tests if not mocked).

**Repository Variables** (Settings > Secrets and variables > Actions > Variables):
- `HF_USERNAME`: Your Hugging Face username (e.g., `omary`).

*Note: You also need to create a Space on Hugging Face named `document-intelligence-platform` before deploying.*


```text
                                    +----------------------+
                                    |     React Web UI     |
                                    +----------+-----------+
                                               |
                                               | HTTP
                                               |
                                    +----------v-----------+
                                    |   FastAPI Backend    |
                                    +----------+-----------+
                                               |
                                       POST /process-email
                                               |
                                    +----------v-----------+
                                    | Document Processing  |
                                    |    Orchestrator      |
                                    +----------+-----------+
                                               |
        ------------------------------------------------------------------------
        |                      |                      |                         |
        |                      |                      |                         |
+-------v------+      +--------v--------+   +---------v---------+   +----------v---------+
| Email Parser |      | Document Parser |   | OCR Engine        |   | Document Extractor |
| (.eml/.msg)  |      | File Detection  |   | PaddleOCR         |   | PDF / DOCX / TXT   |
+-------+------+      +--------+--------+   +---------+---------+   +----------+---------+
        |                      |                        |                        |
        ------------------------                        --------------------------
                     |                                             |
                     +-------------------+-------------------------+
                                         |
                                         v
                              Normalized Plain Text
                                         |
                                         |
                            +------------v-------------+
                            |    LLM Extraction Layer  |
                            |    GPT OSS 20B (JSON)    |
                            +------------+-------------+
                                         |
                              Structured Pydantic Models
                                         |
                                         |
                            +------------v-------------+
                            | Cross-Document Matching  |
                            | Invoice ↔ Delivery Note  |
                            +------------+-------------+
                                         |
                                         |
                            +------------v-------------+
                            | Deterministic Validation |
                            | Totals • Tax • Regex     |
                            | Business Rules           |
                            +------------+-------------+
                                         |
                                         |
                            +------------v-------------+
                            | Workflow Decision Engine |
                            | Approve / Review / Reject|
                            +------------+-------------+
                                         |
                       ------------------|------------------
                       |                                     |
             +---------v---------+              +------------v------------+
             |  MongoDB Atlas    |              |   JSON API Response     |
             +-------------------+              +-------------------------+
```# Document-Intelligence-Platform
# Document-Intelligence-Platform
