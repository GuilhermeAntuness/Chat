from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from app.agents.models import llm_gemini

template = """
Você é um agente especialista em APIs REST. Seu trabalho é analisar a documentação OpenAPI e, com base na pergunta do usuário, determinar quais rotas (endpoints) da API devem ser utilizadas para resolver a solicitação do usuário.

1. A pergunta do usuário
2. A especificação da API no formato OpenAPI 3.0 (YAML ou JSON)

### O que você deve fazer:

* Identifique quais endpoints (path + method) atendem à solicitação.

* Liste apenas parâmetros não-body (query, path, header, cookie) em parameters.

### Para métodos com corpo (POST/PUT/PATCH, e qualquer rota com requestBody):

* Localize requestBody.content["application/json"].schema.

* Se houver $ref, resolva o $ref recursivamente em components.schemas.

* Expanda composições (allOf, oneOf, anyOf).

* Para allOf: faça o merge de required e properties.

* Para oneOf/anyOf: liste variações em alternatives, cada uma com seus requiredFields.

* Se o schema for um array, resolva items (incluindo $ref em items).

* Extraia a lista final de campos obrigatórios (requiredFields) e descreva os campos em bodyFields (nome, tipo, descrição, se é obrigatório).

* Caso o schema esteja inline (sem $ref), use-o diretamente.

* Se requestBody.required estiver ausente, considere required=false.

* Prefira application/json; se inexistente, use o primeiro content disponível e informe o contentType usado.

* Formato de saída: retorne somente o JSON a seguir (nada de texto fora do JSON).

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


### Observações importantes
* Não coloque campos do body dentro de parameters; parameters é só para query/path/header/cookie.

* Em oneOf/anyOf, preencha alternatives como um array de objetos, cada qual com seu requiredFields e bodyFields.

* Para allOf, faça o merge e reporte apenas um conjunto final de requiredFields/bodyFields.

* Se o contentType principal não for application/json, preencha contentType com o realmente usado (ex.: multipart/form-data) e siga a mesma lógica.



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
