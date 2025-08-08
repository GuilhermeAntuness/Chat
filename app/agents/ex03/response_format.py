from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

import requests
import json

from app.agents.models import llm_groq
from app.agents.ex03.validator import verificar_filtros



template = """
Você é um agente cujo trabalho é receber uma pergunta que o usuário fez, receber os dados que estão associados à pergunta dele num formato de lista e formatar um texto sucinto, mas explicativo e humanizado, referente aos dados dessa lista. 

Existe a possibilidade de você receber uma validação faltante. Analise se a resposta é informando campos de filtros ou parâmetros faltantes para complementar as respostas.

Observações gerias: Seja mais direto e sem muito exagero na sua resposta.
Atenção: Retire todo e qualquer markdown que vier na resposta, deixe apenas o texto cru. tie barras e barra inversa e aspass desnecessarias

Aqui está o que ele perguntou:
{pergunta}
Aqui está a resposta:
{resultado}
"""



def executar_rota(rota):
    rota = rota.strip("```json").strip("```").strip()
    rota = json.loads(rota)
    method = rota[0]['method']
    path = rota[0]['path']

    if method == "POST":
        body = {

        }
        resultado_api = requests.get(f"http://127.0.0.1:5000{path}")

    elif method == "GET":

        resultado_api = requests.get(f"http://127.0.0.1:5000{path}")
        resultado_api = resultado_api.text
        print(resultado_api)
    else:
        resultado_api = None


    return resultado_api


def gerar_resposta(pergunta):
    prompt = PromptTemplate(
        template=template,
        input_variables=["pergunta", "resultado"]
    )

    validacao, rota = verificar_filtros(pergunta)
    validacao = validacao.strip("```json").strip("```").strip()
    validacao = json.loads(validacao)
    if validacao['validated'] == False:
        resultado_api = validacao

    else:
        resultado_api = executar_rota(rota=rota)


    prompt_format = prompt.format(pergunta=pergunta, resultado=resultado_api)
    resposta = llm_groq.invoke([HumanMessage(content=prompt_format)])

    return resposta.content


resposta= gerar_resposta (pergunta="Quero visualizar os livros cadastrados")
print(resposta)