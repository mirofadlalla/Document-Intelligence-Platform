from enum import Enum

from pydantic import BaseModel


class WorkflowAction(str, Enum):

    APPROVE = "APPROVE"

    REVIEW = "ROUTE_TO_HUMAN_REVIEW"

    REJECT = "REJECT"


class WorkflowResult(BaseModel):

    action: WorkflowAction

    reason: str