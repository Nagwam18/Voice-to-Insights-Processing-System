from pydantic_ai import Agent
from pydantic_ai.models.huggingface import HuggingFaceModel
from app.models.schemas import Insights
from app.core.prompts import PROMPT

agent = Agent(
    model=HuggingFaceModel("Qwen/Qwen2.5-7B-Instruct"),
    output_type=Insights,
    system_prompt=PROMPT
)

async def analyze_text(text: str) -> dict:
    result = await agent.run(text)
    insight: Insights = result.output
    return insight.model_dump()
