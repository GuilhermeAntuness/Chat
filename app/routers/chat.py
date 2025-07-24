from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.agents.response_format import gerar_resposta


router = APIRouter(prefix="/chat", tags=["chat"])
class ChatBase(BaseModel):
    question: str

@router.post("/", response_model=ChatBase, status_code=status.HTTP_201_CREATED, summary="Enviar nova mensagem de consulta")
def enviar_mensagem(pergunta: ChatBase):
    resposta = gerar_resposta(pergunta.mensagem)
    return {"resposta": resposta}