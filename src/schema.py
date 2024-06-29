
from pydantic import BaseModel, Field
from typing import List


class ModelSuggestion(BaseModel):
    """Data model for a call summary."""

    task: str = Field(
        description="The suggested task for the child."
    )
    type: str = Field(
        description="The type of the children suggestion should be one of ."
    )
    steps: List[str] = Field(description="Steps to complete the task")