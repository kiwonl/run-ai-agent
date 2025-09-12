# -*- coding: utf-8 -*-
import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

import google.auth
import google.auth.transport.requests
import google.oauth2.id_token

# --- Setup Logging and Environment ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

# 모델 이름 환경 변수에서 가져오기
model_name = os.getenv("MODEL")


# Greet user and save their prompt
def add_prompt_to_state(tool_context: ToolContext, prompt: str) -> dict[str, str]:
    """Saves the user's initial prompt to the state."""
    tool_context.state["PROMPT"] = prompt
    logging.info(f"[상태 업데이트] 프롬프트에 추가됨: {prompt}")
    return {"status": "success"}


# Configuring the MCP Tool to connect to the Zoo MCP server

mcp_server_url = os.getenv("MCP_SERVER_URL")
if not mcp_server_url:
    raise ValueError("MCP_SERVER_URL 환경 변수가 설정되지 않았습니다.")


def get_id_token():
    """Get an ID token to authenticate with the MCP server."""
    target_url = os.getenv("MCP_SERVER_URL")
    audience = target_url.split("/mcp/")[0]
    request = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(request, audience)
    return id_token


"""
# Use this code if you are using the public MCP Server and comment out the code below defining mcp_tools
mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=mcp_server_url
    )
)
"""

mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=mcp_server_url,
        headers={
            "Authorization": f"Bearer {get_id_token()}",
        },
    ),
)

# Configuring the Wikipedia Tool
wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

# 1. Researcher Agent
comprehensive_researcher = Agent(
    name="comprehensive_researcher",
    model=model_name,
    description="동물원 내부 데이터와 위키피디아의 외부 지식에 모두 접근할 수 있는 기본 연구원입니다.",
    instruction="""
    당신은 도움이 되는 연구 조수입니다. 당신의 목표는 사용자의 프롬프트에 완전히 답변하는 것입니다.
    두 가지 도구에 액세스할 수 있습니다:
    1. 우리 동물원의 동물(이름, 나이, 위치)에 대한 특정 데이터를 가져오는 도구.
    2. 일반적인 지식(사실, 수명, 식단, 서식지)을 위해 위키피디아를 검색하는 도구.

    먼저 사용자의 프롬프트를 분석합니다.
    - 프롬프트가 하나의 도구로만 답변될 수 있는 경우 해당 도구를 사용합니다.
    - 프롬프트가 복잡하여 동물원 데이터베이스와 위키피디아 모두의 정보가 필요한 경우,
      필요한 모든 정보를 수집하기 위해 두 도구를 모두 사용해야 합니다.
    - 사용하는 도구의 결과를 예비 데이터 출력으로 종합합니다.

    프롬프트:
    {{ PROMPT }}
    """,
    tools=[mcp_tools, wikipedia_tool],
    output_key="research_data",  # 결합된 결과를 저장하는 키
)

# 2. Response Formatter Agent
response_formatter = Agent(
    name="response_formatter",
    model=model_name,
    description="모든 정보를 친절하고 읽기 쉬운 응답으로 종합합니다.",
    instruction="""
    당신은 동물원 투어 가이드의 친절한 목소리입니다. 당신의 임무는
    RESEARCH_DATA를 가져와 사용자에게 완전하고 도움이 되는 답변으로 제공하는 것입니다.

    - 먼저 동물원의 특정 정보(이름, 나이, 찾는 위치 등)를 제시합니다.
    - 그런 다음 연구에서 얻은 흥미로운 일반적인 사실을 추가합니다.
    - 일부 정보가 누락된 경우 가지고 있는 정보만 제시합니다.
    - 대화적이고 매력적으로 이야기합니다.

    RESEARCH_DATA:
    {{ research_data }}
    """,
)

tour_guide_workflow = SequentialAgent(
    name="tour_guide_workflow",
    description="동물에 대한 사용자 요청을 처리하기 위한 기본 워크플로우입니다.",
    sub_agents=[
        comprehensive_researcher,  # 1단계: 모든 데이터 수집
        response_formatter,  # 2단계: 최종 응답 포맷 지정
    ],
)

root_agent = Agent(
    name="greeter",
    model=model_name,
    description="동물원 투어 가이드의 기본 진입점입니다.",
    instruction="""
    - 동물원에 있는 동물에 대해 배우는 데 도움을 줄 것이라고 사용자에게 알립니다.
    - 사용자가 응답하면 'add_prompt_to_state' 도구를 사용하여 응답을 저장합니다.
    도구를 사용한 후 'tour_guide_workflow' 에이전트로 제어를 이전합니다.
    """,
    tools=[add_prompt_to_state],
    sub_agents=[tour_guide_workflow],
)
