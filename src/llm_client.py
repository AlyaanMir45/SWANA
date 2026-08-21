import json
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


def generate_command(user_request: str, columns: list[str]) -> dict:
    """
    Convert a user's natural language request into a SWANA command.
    """

    column_list = ", ".join(columns)

    prompt = f"""
You convert user requests into JSON commands for a data analysis application.

Available columns:
{column_list}

Supported analysis operations:

average
sum
count

Supported cleaning actions:

remove_duplicates
remove_missing_rows
fill_missing_values
remove_empty_columns
standardize_column_names

Rules:
- Return only valid JSON.
- Do not include explanations.
- Use exact column names from the available columns.
- For average or sum, include the column.
- For count, no column is required.

Examples:

User request:
What is the average annual salary?

Response:
{{
    "operation": "average",
    "column": "Annual Salary"
}}

User request:
Remove duplicate rows

Response:
{{
    "action": "remove_duplicates",
    "parameters": {{}}
}}

User request:
{user_request}
"""

    response = client.responses.create(
        model="openai/gpt-oss-20b",
        input=prompt,
    )

    command_text = response.output_text.strip()

    return json.loads(command_text)