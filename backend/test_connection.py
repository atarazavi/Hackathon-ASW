"""Quick script to verify Azure OpenAI connection"""
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

try:
    completion = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[{"role": "user", "content": "Say 'connection successful'"}],
        max_tokens=10,
    )
    print("SUCCESS:", completion.choices[0].message.content)
except Exception as e:
    print("FAILED:", str(e))
