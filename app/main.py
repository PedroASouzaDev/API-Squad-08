from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import models, sentiment
from schemas import CSAcaoCreate, CSSentimentoCreate
import crud
import database

# Criando a aplicação FastAPI
app = FastAPI()

# Iniciar o banco de dados e as tabelas (apenas se necessário)
models.Base.metadata.create_all(bind=engine)

# Classe para representar a requisição de ação
class AçãoRequest(BaseModel):
    descricao: str
    event_id: int
    user_id: int = None
    agent_id: int = None

# Rota para recuperar o sentimento de uma ação
@app.get("/sentimentos/{acao_id}")
def obter_sentimento(acao_id: int):
    db = SessionLocal()
    try:
        # Buscar o sentimento da ação pelo acao_id
        sentimento = db.query(models.CSSentimento).filter(models.CSSentimento.acao_id == acao_id).first()
        
        if not sentimento:
            raise HTTPException(status_code=404, detail="Sentimento não encontrado para essa ação")
        
        return {"acao_id": sentimento.acao_id, "sentimento": sentimento.sentimento}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

# Endpoint para analisar o sentimento de uma ação específica
@app.post("/analisar/{acao_id}")
def analisar_sentimento(acao_id: int, db: Session = Depends(database.get_db)):
    # Primeiro, obtemos a ação pelo seu ID
    acao = crud.obter_acao(db, acao_id)
    
    # Depois, criamos o sentimento baseado na descrição da ação
    sentimento = crud.criar_sentimento(db, acao_id, acao.descricao)
    
    return {"acao_id": acao_id, "sentimento": sentimento.sentimento}
