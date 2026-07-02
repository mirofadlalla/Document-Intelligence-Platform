# Processing Pipeline Use Cases

## UC-01 — Standard Document Processing

### Primary Actor
External Vendor

### Goal
Automatically process a valid business email with supporting documents.

### Preconditions
- A valid email is received.
- Supported attachments (PDF, DOCX, or Image) are included.

### Main Flow
1. Receive the incoming email.
2. Extract the email body.
3. Parse all supported attachments.
4. Perform OCR when required.
5. Extract structured information using the AI extraction service.
6. Cross-reference information across all documents.
7. Execute deterministic validation rules.
8. Determine the workflow decision.
9. Store the processing result.
10. Return the standardized JSON response.

### Postconditions
- Processing results are stored.
- Workflow status is assigned.

### Expected Workflow
APPROVE


---

## UC-02 — Cross-Document Conflict

### Primary Actor
External Vendor

### Goal
Detect inconsistencies between multiple business documents.

### Preconditions
- Multiple related documents are available.

### Main Flow
1. Extract invoice data.
2. Extract delivery slip data.
3. Compare quantities and line items.
4. Detect mismatched information.
5. Flag validation errors.
6. Route the request for manual review.

### Postconditions
- Validation errors are recorded.
- Human review is required.

### Expected Workflow
ROUTE_TO_HUMAN_REVIEW


---

## UC-03 — Failed Business Validation

### Primary Actor
System

### Goal
Reject documents that violate deterministic business rules.

### Preconditions
- Structured data has been extracted successfully.

### Main Flow
1. Calculate totals.
2. Validate taxes.
3. Validate discounts.
4. Validate invoice format.
5. Detect invalid business rules.
6. Reject the request.

### Postconditions
- Validation report is generated.
- Workflow is rejected.

### Expected Workflow
REJECT


---

## UC-04 — Corrupted Document

### Primary Actor
External Vendor

### Goal
Handle unreadable or corrupted documents gracefully.

### Preconditions
- One or more attachments cannot be parsed.

### Main Flow
1. Attempt to parse the attachment.
2. Detect parsing failure.
3. Record the error.
4. Continue processing remaining documents.
5. Route for manual review if required.

### Postconditions
- Error is logged.
- Remaining documents continue processing.

### Expected Workflow
ROUTE_TO_HUMAN_REVIEW


---

## UC-05 — Unsupported File Type

### Primary Actor
External Vendor

### Goal
Reject unsupported document formats.

### Preconditions
- Uploaded attachment has an unsupported extension.

### Main Flow
1. Receive uploaded file.
2. Validate file type.
3. Reject unsupported format.
4. Return validation error.

### Postconditions
- File is rejected.
- Processing is terminated.

### Expected Workflow
REJECT


---

# Use Case Summary

| Use Case | Description | Workflow |
|----------|-------------|----------|
| UC-01 | Standard document processing | APPROVE |
| UC-02 | Cross-document mismatch | ROUTE_TO_HUMAN_REVIEW |
| UC-03 | Failed deterministic validation | REJECT |
| UC-04 | Corrupted document | ROUTE_TO_HUMAN_REVIEW |
| UC-05 | Unsupported file type | REJECT |