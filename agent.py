from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

@tool
def read_note_from_file(file: str) -> str:
    """Read the contents of a text file and return it as a string."""
    try:
        with open(file) as f:
            content = f.read()
            return f"Contents of {file}: {content}"
    except FileNotFoundError:
        return f"Error: File '{file}' not found"
    except PermissionError:
        return f"Error: Permission denied"
    except Exception as ex:
        return f"Error: {str(ex)}"

@tool
def write_note_to_file(file: str, content: str):
    """Write the given content to a file."""
    try:
        with open(file, "w") as f:
            f.write(content)
            return f"Successfully wrote {len(content)} characters to '{file}'"
    except FileNotFoundError:
        return f"Error: File '{file}' not found"
    except Exception as ex:
        return f"Error writing to {file}: {str(ex)}"


system_prompts="""you are an note-taking assistant.
                  you can read and write text files to help user manage their notes.
                  Be cautious and precise
                """

TOOLS=[read_note_from_file, write_note_to_file]
model=ChatOpenAI(model="gpt-4", temperature=0)
agent=create_agent(model,tools=TOOLS,system_prompt=system_prompts)

def run_agents(user_input:str)->str:
    try:
        result= agent.invoke({"message": [{"role": "user", "content": user_input}]})
        return result["messages"][-1].content

    except Exception as ex:
        return f"Error: {str(ex)}"


print(run_agents("I have a scheduled appointment at Feb 5 morning to doctor. make a note for it"))


