from app.agents.models import llm_groq
from app.agents.ex02.sql_constructor import gerar_consulta_sql
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from app.agents.ex03.validator import verificar_filtros
from app.agents.ex03.route_checker import verificar_rota


template = """
Você é um agente cujo trabalho é receber uma pergunta que o usuário fez, receber os dados que estão associados à pergunta dele num formato de lista e formatar um texto sucinto, mas explicativo e humanizado, referente aos dados dessa lista. 

Observações gerias: Seja mais direto e sem muito exagero na sua resposta.

Aqui está o que ele perguntou:
{pergunta}
Aqui está a resposta:
{resultado}
"""





def gerar_resposta(pergunta):
    prompt = PromptTemplate(
        template=template,
        input_variables=["pergunta", "resultado"]
    )

    validacao, rota = verificar_filtros(pergunta)

    consulta_sql = gerar_consulta_sql(pergunta)

    prompt_format = prompt.format(pergunta=pergunta, resultado=consulta_sql)
    resposta = llm_groq.invoke([HumanMessage(content=prompt_format)])

    return resposta.content


