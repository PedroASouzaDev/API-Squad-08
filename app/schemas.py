from pydantic import BaseModel
from typing import Optional

class CSSentimentoBase(BaseModel):
    acao_id: int
    sentimento: str

class CSSentimentoCreate(CSSentimentoBase):
    pass

class CSSentimento(CSSentimentoBase):
    id: int

    class Config:
        orm_mode = True

class CSAcaoBase(BaseModel):
    event_id: int
    descricao: str
    agent_id: Optional[int] = None
    user_id: Optional[int] = None
    data_acao: Optional[str] = None

class CSAcaoCreate(CSAcaoBase):
    pass

class CSAcao(CSAcaoBase):
    acao_id: int

    class Config:
        orm_mode = True
