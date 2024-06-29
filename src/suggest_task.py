from src.prompts import SUGGESTION_PROMPT_TEMPLATE, BASIC_INFO_TEMPLATE, RECENT_TASKS_TEMPLATE
from src.schema import ModelSuggestion
from src.model import load_model

def get_children_info():
    # TODO: Fetch from the backend database
    return {
        "name": "Andy",
        "age": 10,
        "gender": "Male"
    }
    
import re
import json

def extract_json_from_string(text):
    # Regex pattern to match content between ```json and ```
    pattern = r'```json\s*(.*?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        json_content = match.group(1)
        try:
            data = json.loads(json_content)
            return data
        except json.JSONDecodeError:
            print("Invalid JSON content")
            return None
    else:
        print("No JSON content found")
        return None



async def get_suggestions(message_history, retries=3, delay=2):
    llm = load_model("groq", "llama3-8b-8192")
    
    messages = SUGGESTION_PROMPT_TEMPLATE.format_messages(
        json_schema=ModelSuggestion.schema_json(), 
        basic_info=BASIC_INFO_TEMPLATE.format(**get_children_info()),
        chat_message=" ".join([m["role"] + ": " + m["content"] for m in message_history]),
        recent_tasks=RECENT_TASKS_TEMPLATE,         
    )

    for attempt in range(retries):
        try:
            output = await llm.achat(messages)
            json_output = extract_json_from_string(output.message.content)
            return json_output
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                json_output = {"error": "Error occurred while generating suggestions"}
                return json_output