import json

def build_prompt_from_steps(steps, domain="stephow.com", language="ko"):
    """
    Generate a structured prompt from OCR-based step data.
    """
    input_data = {
        "steps": [],
        "domain": domain,
        "language": language
    }

    for step in steps:
        # 기본 제목 설정 (title > header > "Untitled")
        title = step.get("title") or step.get("header") or "Untitled"
        desc = step.get("description", "").strip()
        header = step.get("header", "").strip()
        callout = step.get("callout", "").strip()

        text = title.strip()

        # Step 타이틀에 설명이 있을 경우
        if desc:
            text += f" - {desc}"

        # 헤더가 있을 경우 추가
        if header:
            text += f" [{header}]"

        # 콜아웃이 있을 경우 추가
        if callout:
            text += f" ({callout})"

        # 단계 추가
        input_data["steps"].append(text)

    # 프롬프트 구성
    prompt = f"""
<input_data>
{json.dumps(input_data, indent=2, ensure_ascii=False)}
</input_data>

[System Setting] 
You are an AI assistant specialized in generating concise, clear, and action-oriented manual titles based on user workflows. 
Your primary goal is to create user-centric titles that clearly describe the end goal of a process.

[Analysis Requirements]
Workflow Analysis:
- Identify the final goal of the process.
- Identify key operational steps.
- Confirm the result of user actions.

Title Creation Criteria:
- Use action verbs to clearly convey the purpose.
- Focus on the end goal and user action.
- Start the title with one of the following phrases:
  - "How to ..."
  - "Guide to ..."
  - "Learn to ..."
- Include the domain name if relevant (e.g., "on {domain}").
- Limit the title to 10 words for readability.
- Use official technical terms to maintain accuracy.
- Prioritize a single comprehensive phrase that summarizes the entire process rather than breaking it into smaller tasks.

[Output Format]
- Return the title as a JSON object within <response> tags:
  <response> {{"title": "Generated title here"}} </response>
- Output the title only in the specified language.

[Language Support]
- Respond only in the specified language.
- Consider grammar, idioms, and context of the target language.
- Create titles that match the context and style of the language.

[Avoid]
- Generic or vague terms like "workflow", "task", "process".
- Redundant or unnecessary words.
- Passive voice that makes the title less actionable.

[Additional Context]
- Domain: {domain}
- Note: If displayed as 'Untitled', analyze additional context using domain and metadata information.
- If the steps represent a larger workflow, create a title that reflects the overall process, not just individual actions.

[Examples]
Language: ENGLISH
Input: ["Click 'Login'", "Enter credentials", "Submit form"]
→ <response> {{"title": "How to Log In to Your Account on domain"}} </response>

Language: KOREAN
Input: ["로그인 버튼 클릭", "아이디와 비밀번호 입력", "제출 버튼 클릭"]
→ <response> {{"title": "domain에서 계정에 로그인하기"}} </response>
"""

    return prompt
