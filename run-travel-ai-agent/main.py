import os
import logging
import asyncio
import google.cloud.logging
from dotenv import load_dotenv

from adk.agent import Agent
from adk.embedding import EmbeddingModel
from adk.llm import LLM
from adk.prompt import PromptGenerator

from tools.travel_agent import add_prompt_to_state, plan_trip

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()
model_name = os.getenv("MODEL")


def create_agent():
    """Creates and configures the travel agent."""
    llm = LLM(model_name)
    embedding_model = EmbeddingModel()
    prompt_generator = PromptGenerator(llm=llm)

    agent = Agent(
        llm=llm,
        embedding_model=embedding_model,
        prompt_generator=prompt_generator,
        tools=[add_prompt_to_state, plan_trip],
    )
    return agent


if __name__ == "__main__":
    agent = create_agent()
    logging.info("Travel agent initialized.")

    async def run_agent():
        while True:
            prompt = input("You: ")
            if prompt.lower() in ["exit", "quit"]:
                break
            response = await agent.process(prompt)
            print(f"Agent: {response}")

    try:
        asyncio.run(run_agent())
    except (KeyboardInterrupt, EOFError):
        pass