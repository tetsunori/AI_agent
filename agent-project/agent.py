import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# 환경 변수 로드
load_dotenv()

# 도구 및 미들웨어 임포트
from tools import search_recipe_from_10000recipe, search_nearby_restaurants
from middleware import domain_guard_middleware

# 1. 사용할 LLM 모델 설정
model = ChatOpenAI(model="gpt-4o", temperature=0.7)

# 2. 커스텀 툴 목록
tools = [
    search_recipe_from_10000recipe,
    search_nearby_restaurants,
]

# 3. 시스템 프롬프트 (엄격한 도메인 고정 및 체계적인 문답 유도)
system_prompt = (
    "당신은 스마트 요리 추천 및 맛집/레시피 안내 AI 비서입니다.\n"
    "사용자가 원하는 메뉴를 체계적인 문답(대분류 ➔ 메뉴 선정 ➔ 배달 vs 조리 선택)을 통해 유도해주세요.\n\n"
    "[Strict Domain Rule]\n"
    "- 당신은 오직 요리 추천, 맛집 안내, 레시피 제공 업무만 수행합니다.\n"
    "- 코딩, 프로그래밍, 수학, 일반 상식 등 요리와 무관한 질문이 들어오면 "
    "\"죄송합니다. 저는 오직 요리 추천, 맛집 안내, 레시피 제공 업무만 도와드릴 수 있습니다. 어떤 음식을 추천해 드릴까요?\"라고 정중히 거부하세요.\n"
    "- 절대로 요리/맛집 외의 다른 작업(코드 작성 등)을 수행하지 마세요."
)

# 4. ReAct 에이전트 생성
agent = create_react_agent(
    model=model,
    tools=tools,
    prompt=system_prompt,
)

if __name__ == "__main__":
    print("[Agent Setup] 🚀 도메인 보호 및 후처리 기능이 결합된 에이전트가 로드되었습니다.")