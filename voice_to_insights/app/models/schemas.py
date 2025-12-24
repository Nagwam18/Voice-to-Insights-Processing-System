from pydantic import BaseModel, Field
from typing import List

class Insights(BaseModel):
    summary: str = Field(description="Concise summary in 2–3 sentences")
    entities: List[str] = Field(description="Important names or objects")
    actions: List[str] = Field(description="Actions or next steps")
