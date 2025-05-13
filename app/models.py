from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class CSUser(Base):
    __tablename__ = "cs_user"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(70), unique=True)
    username = Column(String(255))

    acoes = relationship("CSAcoes", back_populates="user")


class CSAgent(Base):
    __tablename__ = "cs_agents"

    agent_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)

    acoes = relationship("CSAcoes", back_populates="agent")


class CSEvent(Base):
    __tablename__ = "cs_events"

    event_id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    data_abertura = Column(DateTime, nullable=False)
    data_baixa = Column(DateTime)
    status_id = Column(Integer, nullable=False)

    acoes = relationship("CSAcoes", back_populates="event")


class CSAcoes(Base):
    __tablename__ = "cs_acoes"

    acao_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("cs_events.event_id"), nullable=False)
    descricao = Column(Text, nullable=False)
    agent_id = Column(Integer, ForeignKey("cs_agents.agent_id"))
    user_id = Column(Integer, ForeignKey("cs_user.user_id"))
    data_acao = Column(DateTime)

    event = relationship("CSEvent", back_populates="acoes")
    agent = relationship("CSAgent", back_populates="acoes")
    user = relationship("CSUser", back_populates="acoes")
    sentimento = relationship("CSSentimento", back_populates="acao")


class CSSentimento(Base):
    __tablename__ = "cs_sentimentos"

    id = Column(Integer, primary_key=True, index=True)
    acao_id = Column(Integer, ForeignKey("cs_acoes.acao_id"), nullable=False)
    sentimento = Column(String, nullable=False)

    acao = relationship("CSAcoes", back_populates="sentimento")
