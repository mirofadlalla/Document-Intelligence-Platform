
from pydantic import BaseModel

class ProcessingJob(BaseModel):

    metadata: ...

    email: ...

    attachments: ...

    extraction: ...

    validation: ...

    workflow: ...

# class ProcessingStatus(Enum):

#     RECEIVED

#     PARSING

#     EXTRACTING

#     VALIDATING

#     COMPLETED

#     FAILED