import os
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


@tool
def read_note_from_file(file: str) -> str:
    """Use this when a user asks to see, check, or retrieve a note."""
    try:
        with open(file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File '{file}' not found"
    except Exception as ex:
        return f"Error: {str(ex)}"


@tool
def write_note_to_file(file: str, content: str):
    """
    Appends content to a file. 
    It checks if the note already exists to avoid duplicates.
    """
    try:
        # Step 1: Check if file exists and read content to prevent duplicates
        if os.path.exists(file):
            with open(file, "r") as f:
                existing_content = f.read().splitlines()

            # If the exact note is already a line in the file, stop here
            if content.strip() in existing_content:
                return f"Note already exists in '{file}'. No changes made."

        # Step 2: Append the note in a new line
        with open(file, "a") as f:
            # Ensure we start on a new line if the file isn't empty
            f.write(f"\n{content.strip()}")
            return f"Successfully added the note to '{file}'."

    except Exception as ex:
        return f"Error updating {file}: {str(ex)}"


system_prompts = """You are a precise note-taking assistant.
1. When asked to make a note, use 'write_note_to_file' immediately.
2. If the user doesn't provide a filename, default to 'notes.txt'.
3. Do not explain what you are going to do; just do it and confirm the result.
4. If you need to read a note, use 'read_note_from_file'.
5. Do not overwrite; the tool will handle appending and duplicate checks.
"""

TOOLS = [read_note_from_file, write_note_to_file]
model = ChatOpenAI(model="gpt-4", temperature=0)
agent = create_agent(model, tools=TOOLS, system_prompt=system_prompts)


def run_agents(user_input: str) -> str:
    try:
        # Use "messages" (plural) for the standard LangChain agent input
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        return result["messages"][-1].content
    except Exception as ex:
        return f"Error: {str(ex)}"


# Testing
print(run_agents("read all the notes i have previously listed"))