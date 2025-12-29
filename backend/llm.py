import os

try:
    from openai import OpenAI
except ImportError as exc:
    raise ImportError(
        "Missing dependency 'openai'. Install it with:\n"
        "  python -m pip install --upgrade openai\n"
        "Then restart VS Code and select the correct Python interpreter "
        "(Ctrl+Shift+P -> Python: Select Interpreter)."
    ) from exc


# Read Databricks token from environment variable
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")


if not DATABRICKS_TOKEN:
    raise RuntimeError(
        "DATABRICKS_TOKEN environment variable is not set.\n"
        "On Windows PowerShell run:\n"
        "  setx DATABRICKS_TOKEN \"<your-token>\"\n"
        "Then CLOSE and reopen the terminal."
    )


# Create OpenAI-compatible client for Databricks
client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url="https://dbc-0f132665-c7e7.cloud.databricks.com/serving-endpoints"
)


def get_ai_reply(user_message: str) -> str:
    response = client.chat.completions.create(
        model="databricks-qwen3-next-80b-a3b-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Explain answers clearly in a friendly, warm, and well-structured way. "
                    "Use short paragraphs, examples, and natural flow. "
                    "Do not stop mid-answer."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_tokens=1200,   #  Increased
        temperature=0.7
    )
    return response.choices[0].message.content
