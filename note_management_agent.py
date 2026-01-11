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
    """Appends content to a file only if it doesn't already exist."""
    try:
        clean_note = content.strip()

        # Open in r+ (Read + Write).
        # Note: This requires the file to exist, so we use 'a' first just to ensure it exists.
        open(file, 'a').close()

        with open(file, "r+") as f:
            existing_content = f.read()

            # Check if the note is already there
            if clean_note.lower() in existing_content.lower():
                return f"Note already exists in '{file}'."


            separator = "\n" if existing_content and not existing_content.endswith("\n") else ""
            f.write(f"{separator}{clean_note}")

            return f"Successfully added the note to '{file}'."

    except Exception as ex:
        return f"Error: {str(ex)}"


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


def run_agent(user_input: str) -> str:
    try:
        # Use "messages" (plural) for the standard LangChain agent input
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        return result["messages"][-1].content
    except Exception as ex:
        return f"Error: {str(ex)}"




if __name__ == "__main__":

  print(run_agent("hi, how are you?"))

  while True:
        prompt=input("Ask AI Assistant (q to quit): ")
        if prompt=="q":
            quit()
        print(run_agent(prompt))
        print(".........................................\n")