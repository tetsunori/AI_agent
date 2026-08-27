import os
from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
from middleware import sanitize_tool_output

load_dotenv()
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))


@tool
def search_recipe_from_10000recipe(query: str) -> str:
    """만개의레시피 사이트에서 특정 메뉴의 필수 재료 및 단계별 조리 순서를 검색합니다."""
    try:
        search_query = f"{query} 레시피 만드는 법"
        response = tavily.search(
            query=search_query,
            search_depth="advanced",
            include_domains=["10000recipe.com"],
            max_results=5,
        )
        # 함수 내부에서 직접 후처리 함수 호출
        raw_result = str(response)
        cleaned_result = raw_result.replace(";) ", "").replace(";", "")
        print(f"[Sanitize Middleware] 🧹 'search_recipe_from_10000recipe' 결과 노이즈 제거 완료")
        return cleaned_result
    except Exception as e:
        return f"레시피 검색 중 오류가 발생했습니다: {str(e)}"


@tool
def search_nearby_restaurants(address: str, menu: str) -> str:
    """사용자의 위치(주소)와 메뉴를 바탕으로 근처 맛집 목록과 특징을 검색합니다."""
    try:
        search_query = f"{address} {menu} 맛집 추천"
        response = tavily.search(
            query=search_query,
            search_depth="advanced",
            max_results=5,
        )
        # 함수 내부에서 직접 후처리 함수 호출
        raw_result = str(response)
        cleaned_result = raw_result.replace(";) ", "").replace(";", "")
        print(f"[Sanitize Middleware] 🧹 'search_nearby_restaurants' 결과 노이즈 제거 완료")
        return cleaned_result
    except Exception as e:
        return f"맛집 검색 중 오류가 발생했습니다: {str(e)}"