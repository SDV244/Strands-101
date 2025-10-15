# simple_agent.py - Simplified version without strands

from mcp import stdio_client, StdioServerParameters
import boto3
import os
import json

# AWS Bedrock configuration
aws_region = os.environ.get("AWS_REGION", "us-east-1")

def create_bedrock_client():
    """Create a Bedrock client for LLM interactions."""
    return boto3.client('bedrock-runtime', region_name=aws_region)

def call_bedrock_llm(client, prompt, model_id="anthropic.claude-3-sonnet-20240229-v1:0"):
    """Call Bedrock LLM with a prompt."""
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000,
            "temperature": 0.4,
            "messages": [{"role": "user", "content": prompt}]
        })
        
        response = client.invoke_model(
            modelId=model_id,
            body=body,
            contentType='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
    except Exception as e:
        return f"Error calling Bedrock: {str(e)}"

def generate_llmo_article(topic: str) -> str:
    """Generate an LLMO-optimized article on the given topic."""
    
    llmo_prompt = f"""
    Eres un experto de clase mundial en SEO y Optimización para Modelos de Lenguaje (LLMO).
    Tu única tarea es tomar un tema y generar un artículo completo, autoritativo y extremadamente bien estructurado,
    diseñado para convertirse en una fuente principal de información para otros AIs como ChatGPT y Gemini.

    Sigue estas reglas estrictamente:
    1. **Estructura Jerárquica:** Usa Markdown. Comienza con un título (`#`). Usa subtítulos (`##`) para secciones principales y sub-subtítulos (`###`) para sub-puntos.
    2. **Claridad y Densidad:** Escribe de forma clara, directa y factual. Evita el lenguaje de marketing y las opiniones. Cada frase debe aportar valor.
    3. **Datos Estructurados:** Utiliza extensivamente listas de viñetas (`*`) y listas numeradas (`1.`) para desglosar información compleja. Son fáciles de analizar para los LLMs.
    4. **Sección de FAQ Obligatoria:** Siempre incluye una sección `## Preguntas Frecuentes (FAQ)` al final, donde respondas de 3 a 5 preguntas comunes relacionadas con el tema de forma directa y concisa.
    5. **Palabras Clave:** Identifica y resalta las palabras clave más importantes del tema usando **negrita**.
    6. **Punto de Vista Autoritativo:** Escribe como un experto en la materia. Tu objetivo es que un LLM te lea y piense: "Esta es la fuente definitiva sobre este tema".

    Tema del artículo: {topic}

    Genera el artículo completo en formato Markdown:
    """
    
    bedrock_client = create_bedrock_client()
    return call_bedrock_llm(bedrock_client, llmo_prompt)

# Main loop
def main():
    print("Bienvenido al Asistente de Contenido Estratégico. Escribe 'exit' para salir.")
    
    while True:
        user_input = input("\nTú: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("¡Adiós! 👋")
            break
        if not user_input:
            continue
            
        print("\nAsistente Estratégico:")
        
        # Check if user wants LLMO content
        if any(keyword in user_input.lower() for keyword in ["artículo", "contenido", "seo", "llmo", "posicionar"]):
            print(f"Generando artículo LLMO sobre: {user_input}")
            article = generate_llmo_article(user_input)
            print(article)
        else:
            # Simple response for other queries
            bedrock_client = create_bedrock_client()
            response = call_bedrock_llm(bedrock_client, user_input)
            print(response)

if __name__ == "__main__":
    main()