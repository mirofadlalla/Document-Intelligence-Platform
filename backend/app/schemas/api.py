

from pydantic import BaseModel

from .workflow import WorkflowAction

class ProcessRequest(BaseModel):

    subject: str

    body: str


class ProcessResponse(BaseModel):

    metadata: ...

    extraction: ...

    validation: ...

    workflow_action: WorkflowAction