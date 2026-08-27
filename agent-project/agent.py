import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# 환경 변수 로드
load_dotenv()

# 도구 및 미들웨어 클래스 임포트
from tools import search_recipe_from_10000recipe, search_nearby_restaurants
from middleware import CookingAgentMiddleware

# 1. 모델 설정
model = ChatOpenAI(model="gpt-4o", temperature=0.7)

# 2. 툴 목록
tools = [
    search_recipe_from_10000recipe,
    search_nearby_restaurants,
]

# 3. 시스템 프롬프트
system_prompt = (
    "당신은 스마트 요리 추천 및 맛집/레시피 안내 AI 비서입니다.\n"
    "사용자가 원하는 메뉴를 체계적인 문답(대분류 ➔ 메뉴 선정 ➔ 배달 vs 조리 선택)을 통해 유도해주세요.\n"
    "조리를 선택한 경우, **반드시 툴(검색 결과)을 사용하여 얻은 재료 목록과 상세한 조리 순서, 팁을 사용자에게 빠짐없이 친절하게 설명해 주세요.**\n\n"
    "[Strict Domain Rule]\n"
    "- 당신은 오직 요리 추천, 맛집 안내, 레시피 제공 업무만 수행합니다.\n"
    "- 코딩, 프로그래밍, 수학 등 요리와 무관한 질문이 들어오면 "
    "\"죄송합니다. 저는 오직 요리 추천, 맛집 안내, 레시피 제공 업무만 도와드릴 수 있습니다. 어떤 음식을 추천해 드릴까요?\"라고 정중히 거부하세요."
)

# 4. create_agent에 미들웨어 클래스 인스턴스([CookingAgentMiddleware()]) 전달
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    middleware=[CookingAgentMiddleware()],
)

if __name__ == "__main__":
    print("[Agent Setup] 🚀 미들웨어가 정상 탑재된 에이전트가 로드되었습니다.")