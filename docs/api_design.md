# API Design

## Overview

The Document Intelligence Platform exposes a simple RESTful API for processing business emails and document attachments.

The API follows a resource-oriented design, uses JSON responses, and is versioned from the beginning to support future evolution without breaking existing clients.

Base URL

```
/api/v1
```

---

# Endpoints

## Process Documents

Processes an incoming email together with its attached business documents.

```
POST /api/v1/process
```

### Request

**Content-Type**

```
multipart/form-data
```

| Field | Type | Required |
|------|------|----------|
| email_subject | string | ✅ |
| email_body | string | ✅ |
| attachments | File[] | ✅ |

### Response

```json
{
  "metadata": {},
  "extraction": {},
  "validation": {},
  "workflow": {
    "action": "APPROVE"
  }
}
```

---

## Get Processing Job

Returns a previously processed job.

```
GET /api/v1/jobs/{job_id}
```

### Response

```json
{
  "metadata": {},
  "email": {},
  "attachments": [],
  "extraction": {},
  "validation": {},
  "workflow": {},
  "logs": []
}
```

---

## List Processing Jobs

Returns the latest processing jobs.

```
GET /api/v1/jobs
```

### Response

```json
[
  {},
  {},
  {}
]
```

---

## Health Check

Returns the application health status.

```
GET /health
```

### Response

```json
{
  "status": "healthy"
}
```

---

# HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Processing completed successfully |
| 400 | Invalid request |
| 422 | Validation failed |
| 500 | Internal server error |

---

# Error Response Format

All API errors follow a consistent response format.

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Invoice total mismatch."
  }
}
```

---

# API Versioning

The API is versioned using the URL path.

```
/api/v1/
```

This allows future API versions (e.g., `/api/v2`) to be introduced without breaking existing clients.

---

# Request Flow

```
React Client

      │

      ▼

POST /api/v1/process

      │

      ▼

FastAPI Backend

      │

      ▼

Processing Pipeline

      │

      ▼

MongoDB Atlas

      │

      ▼

JSON Response
```

---

# Design Considerations

- RESTful API design.
- Versioned endpoints.
- Consistent JSON responses.
- Standard HTTP status codes.
- Uniform error handling.
- Health check endpoint for deployment environments.
- Stateless request processing.
- Multipart upload support for multiple document attachments.