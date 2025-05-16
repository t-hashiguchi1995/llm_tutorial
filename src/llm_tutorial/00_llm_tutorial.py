import os
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

def generate_text(prompt: str) -> str:
    """OpenAIのLLMを使用してテキストを生成する関数

    Args:
        prompt (str): プロンプト

    Returns:
        str: 生成されたテキスト
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def main() -> None:
    prompt = "こんにちは、自己紹介をしてください。"
    response = generate_text(prompt)
    print(response)

if __name__ == "__main__":
    main()
