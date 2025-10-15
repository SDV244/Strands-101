from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP("My dice roll server.")

@mcp.tool()
def dice_roll(sides: int = 6) -> str:
    """Rolls a dice with the specified number of sides."""
    return f"You rolled a {random.randint(1, sides)}."

    
@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluates a simple mathematical expression (e.g., '5 * (3 + 2)')."""
    try:
        # Nota: eval() puede ser inseguro con entradas no confiables.
        # Para un uso real, considera una librería más segura como 'numexpr'.
        result = eval(expression, {"__builtins__": {}}, {})
        return f"The result of '{expression}' is {result}."
    except Exception as e:
        return f"Invalid expression. Error: {e}"
    
from datetime import datetime

@mcp.tool()
def get_current_datetime() -> str:
    """Returns the current date and time."""
    now = datetime.now()
    return f"The current date and time is: {now.strftime('%Y-%m-%d %H:%M:%S')}."

import os

@mcp.tool()
def list_files(directory: str = ".") -> str:
    """Lists all files and directories in a specified directory."""
    try:
        files = os.listdir(directory)
        if not files:
            return f"The directory '{directory}' is empty."
        return "Contents:\n- " + "\n- ".join(files)
    except FileNotFoundError:
        return f"Error: Directory '{directory}' not found."
    except Exception as e:
        return f"An error occurred: {e}"
    
import requests
from bs4 import BeautifulSoup # pip install beautifulsoup4

@mcp.tool()
def fetch_url(url: str) -> str:
    """Fetches and returns the clean text content of a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Usa BeautifulSoup para limpiar el HTML y obtener solo el texto
        soup = BeautifulSoup(response.content, 'html.parser')
        return ' '.join(soup.get_text().split())[:2000] # Devuelve los primeros 2000 caracteres
    except Exception as e:
        return f"Error fetching URL {url}: {e}"

if __name__ == "__main__":
    mcp.run(transport = "stdio")
