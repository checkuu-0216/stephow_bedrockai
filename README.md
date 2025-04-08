# 🧠 AI 기반 메뉴얼 제목 자동 생성기

이 프로젝트는 OCR로 추출된 메뉴얼 단계(step) 데이터를 기반으로, Amazon Bedrock의 Claude 모델을 활용하여 자동으로 **자연스럽고 목적 중심적인 제목(title)** 을 생성해주는 도구입니다.

<br>

## 📌 프로젝트 목적

- 메뉴얼 작성 시, 사람이 직접 제목을 붙이지 않아도 **AI가 자동으로 적절한 제목**을 제안해주는 기능 제공
- 사용자의 최종 목적과 흐름을 분석하여 **자연스러운 문장으로 제목을 자동 생성**
- 반복 작업을 줄이고, 설명서 품질을 일관되게 유지

<br>

## ⚙️ 기술 스택

| 구분        | 기술 |
|-------------|------|
| Backend     | Python 3.x |
| AI 모델     | Amazon Bedrock - Claude v2 |
| 데이터 연동 | REST API (OCR 결과 가져오기) |
| 기타        | boto3, requests, json, os 등 |

<br>

## 🧭 전체 흐름 설명

OCR 데이터 기반으로 제목을 생성하는 전체 프로세스는 다음과 같습니다:

```text
main.py 실행
  └─ load_steps_from_api(): 
        - OCR API에서 step 데이터 불러오기
  └─ build_prompt_from_steps(): 
        - 가져온 step 정보를 기반으로 프롬프트 구성
        - 제목 후보가 될 주요 내용을 정제하고 AI에 전달할 input_data 생성
  └─ get_anthropic_response(): 
        - Claude 모델에 프롬프트 전달
        - 생성된 제목 응답 받기
  └─ 결과 출력 및 title_generation_count 증가
        - 최대 3회까지만 생성 가능

- `steps`: 각 메뉴얼 단계를 표현하는 JSON 데이터 배열
- `prompt`: AI가 이해할 수 있도록 설계된 문장 + 구조화된 input_data
- `title_generation_count`: 제목 생성 가능 횟수 (최대 3회)
```

<br>

## 📄 주요 파일 설명

| 파일명 | 설명 |
|--------|------|
| `main.py` | 전체 프로그램 실행 진입점. API 호출, 프롬프트 생성, AI 호출 등 전체 흐름을 제어 |
| `client.py` | Amazon Bedrock (Claude) 호출 관련 함수 정의 |
| `prompt_builder.py` | step 데이터로부터 AI에 전달할 프롬프트를 구성하는 로직 포함 |
| `README.md` | 프로젝트 설명 파일 (현재 문서) |

💬 AI 프롬프트 내용 (한글 해석)
<details> <summary>👉 Claude 모델에 전달되는 프롬프트 전체 보기 (한글 해석)</summary> <br>

```text
<input_data>
{input_data를 구조화한 JSON}
</input_data>

[시스템 설정]
당신은 사용자 워크플로우를 바탕으로 간결하고 명확하며 목적 중심적인 메뉴얼 제목을 생성하는 데 특화된 AI 도우미입니다.  
주요 목표는 사용자의 최종 목적을 명확히 설명하는 사용자 중심의 제목을 만드는 것입니다.

[분석 요구사항]
워크플로우 분석:
- 프로세스의 최종 목표를 식별합니다.
- 핵심 작업 단계를 파악합니다.
- 사용자의 행동 결과를 확인합니다.

제목 생성 기준:
- 목적을 명확히 전달하기 위해 **동사**를 사용합니다.
- 최종 목표와 사용자 행동에 집중합니다.
- 제목은 아래 문구 중 하나로 시작해야 합니다:
  - "How to ..."
  - "Guide to ..."
  - "Learn to ..."
- 가능하다면 **도메인명(domain)** 을 포함합니다. (예: "on {domain}")
- **가독성을 위해 10단어 이내**로 제한합니다.
- 정확성을 위해 공식 기술 용어를 사용합니다.
- 여러 작업보다 **전체 프로세스를 포괄**하는 하나의 문장으로 작성합니다.

[출력 형식]
- 결과는 **<response> 태그로 감싸진 JSON 객체**로 반환되어야 합니다:
  <response> {"title": "여기에 생성된 제목"} </response>
- 결과는 반드시 **지정된 언어로만 출력**해야 합니다.

[언어 설정]
- 지정된 언어로만 응답합니다.
- 문법, 관용구, 문맥을 고려해 제목을 생성합니다.
- 언어 스타일과 일관되도록 구성합니다.

[피해야 할 표현]
- "workflow", "task", "process" 같은 **모호한 단어**는 지양합니다.
- **중복되거나 불필요한 단어**는 제거합니다.
- **수동태 표현**은 피하고 능동형으로 표현합니다.

[추가 정보]
- 도메인: {domain}
- 참고: 'Untitled'로 보일 경우, 도메인과 메타데이터를 통해 추가적인 맥락을 분석합니다.
- 이 step들이 더 큰 워크플로우의 일부라면, **전체 과정**을 반영하는 제목을 생성합니다.

[예시]
Language: ENGLISH  
Input: ["Click 'Login'", "Enter credentials", "Submit form"]  
→ <response> {"title": "How to Log In to Your Account on domain"} </response>

Language: KOREAN  
Input: ["로그인 버튼 클릭", "아이디와 비밀번호 입력", "제출 버튼 클릭"]  
→ <response> {"title": "domain에서 계정에 로그인하기"} </response>
```
</details>

<br>

## 🧪 테스트 및 디버깅 모드

AWS 키 없이도 내부 로직이 잘 작동하는지 확인할 수 있도록 **모의 AI 응답(Mocking)** 기능이 포함되어 있습니다.  
`get_anthropic_response()` 함수 내부에서 실제 Bedrock API를 호출하지 않고, 프롬프트 생성 및 흐름 테스트가 가능합니다.

예시:

```python
def get_anthropic_response(prompt: str) -> Optional[str]:
    print("💡 Mock AI 호출됨 (실제 Bedrock 호출 안함)")
    print("프롬프트 일부:", prompt[:200], "...")
    return """
    <response> {"title": "stephow.com에서 계정을 등록하는 방법"} </response>
    """
```

## 🔐 AWS 연동 전 확인 사항
.env 파일 또는 환경 변수에 다음 정보가 필요합니다:

AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=us-east-1

실제 Claude API 호출 시, 위 정보가 없으면 다음과 같은 에러 발생:

AWS 자격 증명이 환경 변수에 설정되지 않았습니다.

## 🔁 제목 생성 횟수 제한
한 번의 메뉴얼 세션에서 제목은 최대 3회까지 생성 가능합니다.

title_generation_count 변수를 통해 횟수를 관리하며, 초과 시 메시지 출력 후 중단됩니다.

제목 자동 생성기는 최대 3회까지 가능합니다.

## 📌 실행 방법

### 1. 환경 변수 설정
AWS_ACCESS_KEY_ID=... <br>
AWS_SECRET_ACCESS_KEY=...

### 2. 메인 파일 실행
python main.py