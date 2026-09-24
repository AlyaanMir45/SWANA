
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
minimum
maximum
median

Supported grouped analysis operations:

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
- Do not include explanations or Markdown.
- Use exact column names from the available columns.
- Never invent column names.
- Use only the supported operations and cleaning actions.
- For all analysis operations except count, include the column.
- For count, no column is required.
- For grouped analysis, include "group_by".
- The "group_by" value must be an exact available column name.
- Only average, sum and count support grouped analysis.
- For grouped count, include "group_by" but do not include "column".
- Do not include "group_by" for ordinary analysis.
- Interpret "mean" as average.
- Interpret "total" as sum when referring to a numeric column.
- Interpret "lowest", "smallest" and "min" as minimum.
- Interpret "highest", "largest" and "max" as maximum.
- Interpret "median" as median.
- Interpret phrases such as "by department", "per department",
  and "for each department" as requests for grouped analysis
  when department is an available column.
- If the request cannot be understood, return an empty JSON object.

Examples:

User request:
What is the average annual salary?

Response:
{{
    "operation": "average",
    "column": "annual_salary"
}}

User request:
What is the total annual salary?

Response:
{{
    "operation": "sum",
    "column": "annual_salary"
}}

User request:
Count the rows

Response:
{{
    "operation": "count"
}}

User request:
What is the lowest annual salary?

Response:
{{
    "operation": "minimum",
    "column": "annual_salary"
}}

User request:
What is the highest annual salary?

Response:
{{
    "operation": "maximum",
    "column": "annual_salary"
}}

User request:
What is the median annual salary?

Response:
{{
    "operation": "median",
    "column": "annual_salary"
}}

User request:
What is the average annual salary by department?

Response:
{{
    "operation": "average",
    "column": "annual_salary",
    "group_by": "department"
}}

User request:
What is the total annual salary by department?

Response:
{{
    "operation": "sum",
    "column": "annual_salary",
    "group_by": "department"
}}

User request:
How many employees are in each department?

Response:
{{
    "operation": "count",
    "group_by": "department"
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