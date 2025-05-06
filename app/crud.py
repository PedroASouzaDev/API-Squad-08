from sqlalchemy.orm import Session
from app import models, schemas
from app.sentiment import SentimentAnalyzer
from fastapi import HTTPException

# Função para criar um sentimento associado a uma ação
def criar_sentimento(db: Session, acao_id: int, descricao: str):
    # Analisando o sentimento da descrição da ação
    sentimento_analisado = SentimentAnalyzer.analisar_sentimento(descricao)
    
    # Criando um novo sentimento para a ação
    sentimento = models.CSSentimentos(acao_id=acao_id, sentimento=sentimento_analisado)
    
    # Adicionando o novo sentimento no banco de dados
    db.add(sentimento)
    db.commit()
    db.refresh(sentimento)
    
    return sentimento

# Função para buscar os sentimentos de uma ação
def obter_sentimentos_acao(db: Session, acao_id: int):
    sentimentos = db.query(models.CSSentimentos).filter(models.CSSentimentos.acao_id == acao_id).all()
    if not sentimentos:
        raise HTTPException(status_code=404, detail="Sentimentos não encontrados para essa ação")
    return sentimentos

# Função para obter os dados de uma ação
def obter_acao(db: Session, acao_id: int):
    acao = db.query(models.CSAcao).filter(models.CSAcao.acao_id == acao_id).first()
    if not acao:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
    return acao
