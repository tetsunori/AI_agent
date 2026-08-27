from typing import Any
from langchain.agents.middleware import AgentMiddleware


class CookingAgentMiddleware(AgentMiddleware):
    """최신 LangChain create_agent와 완벽히 호환되는 동/비동기 통합 미들웨어"""

    def before_agent(self, state: dict[str, Any], runtime: Any) -> dict[str, Any] | None:
        print("[Domain Guard] 🛡️ 요리/맛집 도메인 가이드 미들웨어 작동 중...")
        return None

    def wrap_tool_call(self, request: Any, handler: Any) -> Any:
        result = handler(request)
        if isinstance(result, str):
            cleaned_result = result.replace(";) ", "").replace(";", "")
            print(f"[Sanitize Middleware] 🧹 툴 결과 노이즈 제거 완료 (Sync)")
            return cleaned_result
        return result

    async def awrap_tool_call(self, request: Any, handler: Any) -> Any:
        """LangGraph Studio의 비동기 실행 환경을 지원하기 위한 비동기 툴 후처리 메서드"""
        result = await handler(request)
        if isinstance(result, str):
            cleaned_result = result.replace(";) ", "").replace(";", "")
            print(f"[Sanitize Middleware] 🧹 툴 결과 노이즈 제거 완료 (Async)")
            return cleaned_result
        return result