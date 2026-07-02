# Document Intelligence Platform

Production-grade AI-powered document intelligence platform that extracts structured data from emails and multi-format documents using LLMs, validates extracted information through deterministic business rules, performs cross-document verification, and automates business workflow decisions.

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
