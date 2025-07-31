from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from app.agents.models import llm_gemini

template = """
Você é um agente especialista em APIs REST. Seu trabalho é analisar a documentação OpenAPI e, com base na pergunta do usuário, determinar quais rotas (endpoints) da API devem ser utilizadas para resolver a solicitação do usuário.

### Instruções:
- Leia cuidadosamente a pergunta do usuário.
- Analise a documentação da API fornecida (em formato OpenAPI).
- Identifique quais rotas são mais apropriadas para responder à pergunta.
- Para cada rota selecionada, extraia:
  - O método HTTP (GET, POST, PUT, etc.)
  - A URL da rota
  - Os parâmetros de consulta (query), parâmetros de caminho (path), e corpo da requisição (body), se houver.
- Responda apenas com um JSON contendo as rotas relevantes.

### Formato de saída:

```json
[
  {{
    "path": "/exemplo/de/rota",
    "method": "GET",
    "description": "Descrição da finalidade da rota",
    "parameters": [
      {{
        "name": "param1",
        "in": "query",
        "required": true,
        "type": "string",
        "description": "Descrição do parâmetro"
      }},
      {{
        "name": "id",
        "in": "path",
        "required": true,
        "type": "integer",
        "description": "ID do recurso"
      }}
    ],
    "requestBody": {{
      "required": true,
      "content": {{
        "application/json": {{
          "schema": {{
            "field1": "string",
            "field2": "integer"
          }}
        }}
      }}
    }}
  }}
]
```
Pergunta do usuário:
{pergunta}

Documentação Openapi
{openapi}

Responda somente com o JSON no formato acima. Não adicione explicações, comentários ou texto extra.
"""

def verificar_rota(pergunta):
    prompt = PromptTemplate(
        template=template,
        input_variables=["pergunta", "openapi"]
    )

    with open('openapi.json', 'r', encoding='utf-8') as file:
        openapi = file.read()


    prompt_format = prompt.format(pergunta=pergunta, openapi=openapi)
    resposta = llm_gemini.invoke([HumanMessage(content=prompt_format)])

    return resposta.content


response = verificar_rota(pergunta="Quais livros tenho salvo?")
print(response)