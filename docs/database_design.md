# Database Design (MongoDB Atlas)

## Overview

The Document Intelligence Platform is designed around the concept of a **Processing Job**.

Each incoming email, together with its attached documents, represents one independent processing request. The complete lifecycle of this request—including AI extraction, deterministic validation, workflow decision, and processing logs—is stored as a single MongoDB document.

This document-oriented approach closely matches the business workflow and eliminates the need for complex relational modeling.

---

# Why MongoDB?

This project is **document-centric** rather than **relationship-centric**.

Every email processing request is completely independent from other requests.

There are no business relationships between processing jobs, making MongoDB a natural choice.

Advantages include:

- Document-oriented storage
- Flexible schema
- High read performance
- Horizontal scalability
- No JOIN operations
- Natural mapping between application objects and database documents

---

# Why Not SQL?

A relational database was considered during the system design phase.
However, SQL databases are optimized for highly relational systems where entities frequently reference one another.
In this project, storing the same information in SQL would require multiple normalized tables.

Example:

```
emails
---------
id
subject
body
received_at

attachments
------------
id
email_id (FK)
filename
type
text

extractions
------------
id
attachment_id (FK)

validations
------------
id
extraction_id (FK)

workflow
----------
id
validation_id (FK)

logs
---------
id
email_id (FK)
stage
status
timestamp
```

This approach introduces:

- Multiple tables
- Primary Keys
- Foreign Keys
- Entity relationships
- Complex JOIN operations
- Additional mapping between database records and application models

Retrieving a complete processing job would require joining several tables.

Example:

```sql
SELECT *
FROM emails
JOIN attachments ...
JOIN extractions ...
JOIN validations ...
JOIN workflow ...
JOIN logs ...
```

This significantly increases implementation complexity for a workflow that naturally belongs to a single business object.

---

# MongoDB Design

Instead of splitting a processing request across multiple tables, MongoDB stores the entire processing job inside a single document.

```
MongoDB Atlas

└── processing_jobs

      │

      ├── metadata

      ├── email

      ├── attachments

      ├── extraction

      ├── validation

      ├── workflow

      └── logs
```

Each document completely represents one email processing request.

---

# Collection Design

The platform uses a single collection:

```
processing_jobs
```

Each document inside the collection represents one independent processing job.

This design simplifies querying while keeping all related information together.

---

# Processing Job Schema

```json
{
  "_id": ObjectId,

  "metadata": {
    "source_email": "customer@company.com",
    "received_at": "...",
    "processed_at": "...",
    "processing_time_ms": 2450,
    "status": "completed"
  },

  "email": {
    "subject": "...",
    "body": "..."
  },

  "attachments": [
    {
      "filename": "invoice.pdf",
      "type": "pdf",
      "text": "..."
    }
  ],

  "extraction": {},

  "validation": {},

  "workflow": {
    "action": "APPROVE",
    "reason": "Validation Passed"
  },

  "logs": []
}
```

---

# Metadata

Every production system stores processing metadata.

Metadata enables:

- Processing status tracking
- Performance monitoring
- Auditing
- Processing duration measurement
- Failure investigation

Example:

```json
{
    "status":"completed",
    "received_at":"...",
    "processed_at":"...",
    "processing_time_ms":2450,
    "source_email":"customer@company.com"
}
```

---

# Attachments

Attachments are stored inside the processing job to preserve traceability.

Every extracted field can always be traced back to its original source document.

Example:

```
invoice.pdf

↓

LLM Extraction

↓

Invoice Number

Vendor

Total

Tax
```

This greatly simplifies debugging and auditing.

---

# Workflow

The workflow section stores the final deterministic business decision.

Example:

```json
{
    "action":"APPROVE",
    "reason":"Validation Passed"
}
```

Only deterministic validation logic is allowed to generate workflow decisions.

---

# Processing Logs

Each stage records its execution status.

Example:

```json
[
    {
        "stage":"OCR",
        "status":"success"
    },
    {
        "stage":"LLM Extraction",
        "status":"success"
    },
    {
        "stage":"Validation",
        "status":"success"
    }
]
```

Logs provide complete observability of the processing pipeline.

---

# Schema Flexibility

MongoDB allows different documents within the same collection to contain different fields.

However, this platform intentionally maintains a consistent top-level schema.

```
metadata

email

attachments

extraction

validation

workflow

logs
```

Only the **extraction** section is flexible because different business documents naturally produce different structured outputs.

Example:

Invoice

```
invoice_number

vendor

tax

total
```

Purchase Order

```
po_number

supplier

delivery_date

items
```

This design combines schema consistency with MongoDB's flexible document model.

---

# Indexing Strategy

To improve query performance, the following indexes are recommended.

```
metadata.source_email

metadata.processed_at

metadata.status

workflow.action
```

These indexes optimize:

- Dashboard statistics
- Job history
- Workflow filtering
- Processing reports
- Administrative queries

---

# Design Rationale

The Processing Job follows the **Aggregate Pattern**.

All related information is stored together because it is always:

- Created together
- Updated together
- Retrieved together

No relationships exist between processing jobs.

Therefore:

- No Foreign Keys
- No JOIN operations
- No relationship tables

The document model directly represents the business workflow.

---

# SQL vs MongoDB

| SQL Database | MongoDB |
|--------------|----------|
| Multiple Tables | Single Collection |
| Primary / Foreign Keys | Embedded Documents |
| JOIN Operations | Single Document Retrieval |
| Fixed Schema | Flexible Schema |
| Relationship-Oriented | Document-Oriented |
| Better for relational systems | Better for document processing systems |

---

# Conclusion

MongoDB is the preferred database for this project because each email processing request is an independent business object.

The entire processing lifecycle—including metadata, email content, attachments, AI extraction, deterministic validation, workflow decision, and processing logs—is stored as a single document.

This approach reduces implementation complexity, improves maintainability, eliminates unnecessary relational modeling, and aligns naturally with the business workflow.