from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage

RECENT_TASKS_TEMPLATE = """
1. **Cleaning the Room:** A child organized their toys, books, and clothes, making the room neat and tidy.
2. **Taking Out the Trash:** A child took the household trash out to the curb for pickup.
3. **Reading a Book:** A child read a chapter book for 30 minutes.
4. **Completing Homework:** A child finished their math homework and submitted it on time.
5. **Assisting with Groceries:** A child helped carry grocery bags from the car to the kitchen.

"""

BASIC_INFO_TEMPLATE = """
- **Name:** {name}
- **Age:** {age}
- **Gender:** {gender}
"""

SUGGEST_SYSTEM_PROMPT = """
You are a task recommender system designed 
to suggest enjoyable and productive activities 
for children based on their chat message history and recently completed tasks.
Make suggestions based on children interest, age, gender, and recent activities.

Generate a valid JSON following the given schema below:
{json_schema}
"""

SUGGEST_USER_PROMPT = """
### Basic Info about the Child
{basic_info}

### Chat Message with the Child
{chat_message}

### Recent Tasks Completed by Children in 5 Categories
{recent_tasks}

Now make 10 suggestions for the child based on the information provided.
Categorized the problem into 5 categories:
- Chores
- Learning
- Helping
- Sport
- Communication

For each task, break it down into smaller steps for children to complete, 
and ensure the task is age-appropriate and engaging.

You should return in JSON format, 10 suggestions

### Answer

"""

SUGGESTION_PROMPT_TEMPLATE = ChatPromptTemplate(
    message_templates=[
        ChatMessage(
            role="system",
            content=SUGGEST_SYSTEM_PROMPT
        ),
        ChatMessage(
            role="user",
            content=SUGGEST_USER_PROMPT,
        ),
    ]
)