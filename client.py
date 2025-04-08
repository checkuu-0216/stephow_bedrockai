import boto3
import json
import os
from botocore.exceptions import ClientError
from typing import Optional

def get_anthropic_response(prompt: str) -> Optional[str]:
    """
    Anthropic Claude 모델을 통해 응답을 생성합니다.
    
    Args:
        prompt (str): 모델에 전달할 프롬프트
        
    Returns:
        Optional[str]: JSON 형식의 응답 또는 오류 발생 시 None
    """

#         # ai 연결하기전 작동 테스트를 위한 코드
#     print("💡 Mock AI 호출됨 (실제 Bedrock 호출 안함)")
    
#     # 프롬프트 일부 출력해보고 싶은 경우
#     print("프롬프트 일부:", prompt[:200], "...")

#     return """
# <response> {"title": "stephow.com에서 계정을 등록하는 방법"} </response>
# """

    try:
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS 자격 증명이 환경 변수에 설정되지 않았습니다.")

        client = boto3.client(
            "bedrock-runtime",
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )

        # 요청 본문 구성
        request_body = {
            "prompt": prompt,
            "max_tokens_to_sample": 1000,
            "temperature": 0.7,
            "top_p": 0.95,
        }

        response = client.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps(request_body),
            contentType="application/json"
        )
        
        response_body = json.loads(response['body'].read())
        return response_body.get('completion', '')

    except ValueError as e:
        print(f"설정 오류: {e}")
        return None
    except ClientError as e:
        print(f"AWS API 오류: {e.response['Error']['Message']}")
        return None
    except json.JSONDecodeError as e:
        print(f"응답 파싱 오류: {e}")
        return None
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        return None


