from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


# --- 1. Refined Tools ---
# Clear docstrings are critical because the agent uses them as instructions.
@tool
def read_note_from_file(file_path: str) -> str:
    """
    Read the contents of a text file.
    Use this when the user asks to see, read, or check a specific note.
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
            return f"Contents of {file_path}:\n{content}"
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as ex:
        return f"Error: {str(ex)}"


@tool
def write_note_to_file(file_path: str, content: str) -> str:
    """
    Write content to a text file.
    Use this when the user wants to save information or create a new note.
    """
    try:
        with open(file_path, "w") as f:
            f.write(content)
            return f"Successfully saved to '{file_path}'."
    except Exception as ex:
        return f"Error writing to {file_path}: {str(ex)}"


# --- 2. Agent Configuration ---
# System prompts in v1.0 should be descriptive and goal-oriented.
system_prompts = """You are a precise note-taking assistant. 
1. Use 'write_note_to_file' to save information. 
2. Use 'read_note_from_file' to retrieve information.
3. If the user doesn't specify a filename, ask them for one before taking action.
4. Be concise and confirm your actions once complete."""

TOOLS = [read_note_from_file, write_note_to_file]
# gpt-4o is recommended for more reliable tool-calling precision
model = ChatOpenAI(model="gpt-4o", temperature=0)

# This creates a Graph-based agent loop automatically
agent = create_agent(model, tools=TOOLS, system_prompt=system_prompts)


def run_agents(user_input: str) -> str:
    try:
        # NOTE: The standard input key for the new create_agent is "messages" (plural)
        result = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })

        # The result state contains the full conversation; we want the last assistant message
        return result["messages"][-1].content

    except Exception as ex:
        return f"Error: {str(ex)}"


# --- Testing ---
if __name__ == "__main__":
    print("AI:", run_agents("Save a note called 'reminders.txt' with the text 'Buy groceries'"))
    print("AI:", run_agents("What is in my 'reminders.txt' file?"))