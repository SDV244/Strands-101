#%%
from strands import Agent
from strands_tools import calculator, current_time, speak

#%%
agent = Agent(tools=[calculator, current_time])
#%%
message = "If I was born in 1945 what is my age in days?"
agent(message)
# %%
from strands.models import BedrockModel
from strands_tools import file_read, file_write,speak

model_id = BedrockModel(
    model_id= "anthropic.claude-3-5-sonnet-20240620-v1:0",
)

system_prompt = """

You are a helpful personal assistant capable of performing local file actions and simple tasks

your key capabilities:
1 read, understand, and sumarie files
2 create and write to files
3 List directory contents and provde information on the files
4 sumarize text content


you can use the following tools to perform these actions:
-file_read: read a file and return the content
-file_write: write to a file
-'speak': Speak a message to the user
"""

agent = Agent(
    model = model_id,
    system_prompt = system_prompt,
    tools= [
        file_read,
        file_write,
        speak,
    ],
)
agent("What is the content of the file 'chapter10.txt' located in the 'docs' directory and summary the document in les than 20 words, save ir into docs folder also read it outloud")
# %%
from strands.models import BedrockModel
# Assuming 'Agent' is imported from your library, e.g., 'from strands import Agent'
from strands import Agent
from strands_tools import file_read, file_write, speak
import os
print(os.getcwd())
# This setup is correct
model_id = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
)

system_prompt = """
You are a helpful personal assistant capable of performing local file actions and simple tasks.

Your key capabilities:
1. Read, understand, and summarize files.
2. Create and write to files.
3. List directory contents and provide information on the files.
4. Summarize text content.

You can use the following tools to perform these actions:
- file_read: Read a file and return the content.
- file_write: Write to a file.
- speak: Speak a message to the user.
"""

agent = Agent(
    model=model_id,
    system_prompt=system_prompt,
    tools=[
        file_read,
        file_write,
        speak,
    ],
)

# A slightly more explicit prompt to guide the agent
agent("Read the content of the file 'chapter10.txt' in the 'docs' directory. Then, summarize the document in less than 20 words. Save this summary to a new file named 'chapter10_summary.txt' directly inside the 'docs' folder. Finally, read the summary out loud.")

#%%
from strands import Agent,tool
from strands_tools import calculator, current_time #, python_repl

@tool
def letter_counter(word:str,letter:str) -> int:
    """Counts the number of letters in a word"""
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0
    if len (letter) != 1:
        raise ValueError("Letter must be a single character")
    return word.lower().count(letter.lower())

agent = Agent(

    tools=[
        calculator,
        current_time,
        #python_repl,
        letter_counter,
    ],
)

message = """
tell me how many letter R's are in the word "Strawberry"
"""

agent(message)
# %%
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient

stdio_mcp_client = MCPClient(
    lambda:stdio_client(
    StdioServerParameters(
       command= "uv",
       args= ["run", "main.py"]
    ),
)
)