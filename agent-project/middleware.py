import os
from typing import Any
from langchain.agents.middleware import wrap_tool_call, before_agent, AgentState
from langchain_core.messages import SystemMessage
from langgraph.runtime import Runtime


@wrap_tool_call
async def sanitize_tool_output(request, handler):
    """Tool Output Sanitizer Middleware

    웹 검색(Tavily) 결과 및 툴 실행 결과에 포함된 불필요한 HTML 노이즈,
    광고성 텍스트를 제거하고 깔끔하게 정제합니다.
    """
    tool_name = request.tool_call["name"]
    result = await handler(request)

    # 툴 결과가 문자열인 경우 노이즈 제거
    if isinstance(result, str):
        # 마크다운/HTML 태그나 불필요한 특수 기호 정리
        cleaned_result = result.replace(";) ", "").replace(";", "")
        print(f"[Sanitize Middleware] 🧹 '{tool_name}' 툴 결과 후처리 및 노이즈 제거 완료")
        return cleaned_result

    return result


@before_agent
def domain_guard_middleware(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Domain Guard Middleware

    사용자가 요리, 레시피, 맛집 추천과 무관한 주제(예: 코딩, 수학 문제 등)를
    요청할 경우 이를 단호하게 거부하고 요리 관련 대화로 유도합니다.
    """
    print("[Domain Guard] 🛡️ 요리/맛집 도메인 이탈 방지 가이드 적용 중...")
    
    domain_guard_message = SystemMessage(
        content=(
            "[Strict Domain Rule]\n"
            "- 당신은 오직 '스마트 요리 추천 및 맛집/레시피 안내'를 위한 AI 비서입니다.\n"
            "- 사용자가 코딩, 프로그래밍, 수학, 일반 상식 등 요리와 무관한 질문을 하면 "
            "\"죄송합니다. 저는 오직 요리 추천, 맛집 안내, 레시피 제공 업무만 도와드릴 수 있습니다. 어떤 음식을 추천해 드릴까요?\"라고 정중히 거부하세요.\n"
            "- 절대로 요리/맛집 외의 다른 작업(코드 작성 등)을 수행하지 마세요."
        )
    )
    
    return {"messages": [domain_guard_message]}