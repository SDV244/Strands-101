# agent.py (VERSIÓN CON AGENTE LLMO)

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.llms import BedrockLLM
import boto3
import os

# --- CONFIGURACIÓN DE AWS BEDROCK ---
aws_region = os.environ.get("AWS_REGION", "us-east-1")
boto3_session = boto3.Session(region_name=aws_region)

# --- NUEVO: AGENTE ESPECIALIZADO EN CONTENIDO LLMO ---
# Esta función crea nuestro agente experto en SEO para IAs.
def create_llmo_content_agent(model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0") -> Agent:
    """Crea un agente especializado en generar contenido optimizado para LLMs."""
    
    # EL CEREBRO DEL AGENTE: Este prompt es la clave de todo.
    llmo_system_prompt = """
    Eres un experto de clase mundial en SEO y Optimización para Modelos de Lenguaje (LLMO).
    Tu única tarea es tomar un tema y generar un artículo completo, autoritativo y extremadamente bien estructurado,
    diseñado para convertirse en una fuente principal de información para otros AIs como ChatGPT y Gemini.

    Sigue estas reglas estrictamente:
    1.  **Estructura Jerárquica:** Usa Markdown. Comienza con un título (`#`). Usa subtítulos (`##`) para secciones principales y sub-subtítulos (`###`) para sub-puntos.
    2.  **Claridad y Densidad:** Escribe de forma clara, directa y factual. Evita el lenguaje de marketing y las opiniones. Cada frase debe aportar valor.
    3.  **Datos Estructurados:** Utiliza extensivamente listas de viñetas (`*`) y listas numeradas (`1.`) para desglosar información compleja. Son fáciles de analizar para los LLMs.
    4.  **Sección de FAQ Obligatoria:** Siempre incluye una sección `## Preguntas Frecuentes (FAQ)` al final, donde respondas de 3 a 5 preguntas comunes relacionadas con el tema de forma directa y concisa.
    5.  **Palabras Clave:** Identifica y resalta las palabras clave más importantes del tema usando **negrita**.
    6.  **Punto de Vista Autoritativo:** Escribe como un experto en la materia. Tu objetivo es que un LLM te lea y piense: "Esta es la fuente definitiva sobre este tema".

    El input que recibirás será el tema del artículo. Tu output debe ser el artículo completo en formato Markdown.
    """
    
    llmo_llm = BedrockLLM(
        session=boto3_session,
        model_id=model_id,
        temperature=0.4, # Un poco más factual y menos creativo
        system_prompt=llmo_system_prompt # Asignamos nuestro prompt especializado
    )
    
    # Este agente no necesita herramientas, solo su cerebro (el prompt) para escribir.
    return Agent(llm=llmo_llm, tools=[])


# --- CONFIGURACIÓN DEL AGENTE PRINCIPAL (ORQUESTADOR) ---
main_agent_llm = BedrockLLM(
    session=boto3_session,
    model_id="anthropic.claude-3-haiku-20240307-v1:0", # Podemos usar un modelo más rápido para orquestar
    temperature=0.2,
    system_prompt="Eres un asistente experto. Tu trabajo es entender la petición del usuario y delegarla a la herramienta correcta. Si te piden contenido para posicionar en buscadores o IAs, usa la herramienta `generate_llmo_article`."
)

stdio_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="uv",
            args=["run", "main.py"]
        ),
    )
)

# --- BUCLE PRINCIPAL ---
with stdio_mcp_client:
    tools = stdio_mcp_client.list_tools_sync()

    # --- NUEVA HERRAMIENTA PARA LLAMAR AL AGENTE LLMO ---
    @Agent.tool(agent=main_agent_llm)
    def generate_llmo_article(topic: str) -> str:
        """
        Generates a comprehensive, well-structured article on a given topic,
        optimized to be a primary source for LLMs like ChatGPT. Use this to create content
        for positioning a webpage in generative engine results.
        """
        print(f"\n--- Delegando al agente LLMO para generar un artículo sobre: '{topic}' ---\n")
        llmo_agent = create_llmo_content_agent() # Creamos una instancia del agente experto
        response = llmo_agent(topic) # El agente experto procesa el tema y escribe el artículo
        return response

    tools.append(generate_llmo_article)

    agent = Agent(llm=main_agent_llm, tools=tools)

    print("Bienvenido al Asistente de Contenido Estratégico. Escribe 'exit' para salir.")
    while True:
        user_input = input("\n Tú: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("¡Adiós! 👋")
            break
        if not user_input:
            continue
        print("\nAsistente Estratégico:")
        agent(user_input)