import json
from client import get_anthropic_response
from prompt import build_prompt_from_steps
import requests

title_generation_count = 0  # 각 메뉴얼 생성 세션마다 제목 생성 횟수를 초기화

def load_steps_from_api(api_url):
    """메뉴얼 데이터를 API로부터 불러오기"""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("steps", [])
    except Exception as e:
        print(f"Error loading steps from API: {e}")
        return []

def main():    
    global title_generation_count  # 전역 변수 사용 선언

    # 최대 3회 제한
    if title_generation_count > 3:
        print("제목 자동 생성기는 추가 3회까지 가능합니다.")
        return
    
     # 메뉴얼 데이터를 불러올 API 주소 
    api_url = "https://example.com/api/ocr-data"  # 실제 API 주소로 변경

    # API로부터 step 정보 불러오기
    steps = load_steps_from_api(api_url)

    # 프롬프트 구성
    formatted_prompt = build_prompt_from_steps(steps, domain="stephow.com", language="ko")

    # Anthropic 모델 호출
    result = get_anthropic_response(formatted_prompt)

    if result:
        title_generation_count += 1
        print(f"Generated Title: {result}")
    else:
        print("타이틀 생성을 실패했습니다.")

if __name__ == "__main__":
    main()
