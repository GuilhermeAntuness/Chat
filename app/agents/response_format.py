from click import prompt

from models import client
from sql_constructor import gerar_consulta

template = """
Você é um agente cujo trabalho é receber uma pergunta que o usuário fez, receber os dados que estão associados à pergunta dele num formato de lista e formatar um texto sucinto, mas explicativo e humanizado, referente aos dados dessa lista. 

Observações gerias: Seja mais direto e sem muito exagero na sua resposta.

Aqui está o que ele perguntou:
{pergunta}
Aqui está a resposta:
{resultado}
"""

def gerar_resposta(question):
        # Gera a consulta SQL
        consulta_sql = gerar_consulta(question)

        # Formata o prompt a partir do template
        prompt_formatado = template.format(pergunta=question, resultado=consulta_sql)

        # Faz a chamada à API com o prompt formatado
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt_formatado
                },
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        # Retorna apenas o conteúdo da resposta
        return chat_completion.choices[0].message.content
