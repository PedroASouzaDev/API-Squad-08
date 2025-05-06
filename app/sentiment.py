import torch
from transformers import pipeline
from models import CSSentimento, CSAcoes
from database import SessionLocal
from schemas import CSSentimentoCreate

# Carregar o modelo de análise de sentimentos (usando o Hugging Face Transformers para simplificação)
modelo_sentimento = pipeline("text-classification", model="model/sentiment_model")

# Mapeamento dos rótulos de sentimentos para suas respectivas categorias
sentimentos_mapeados = {
    'satisfaction': 'Satisfação',
    'frustration': 'Frustração',
    'confusion': 'Confusão',
    'urgency': 'Urgência/Pressão',
    'anger': 'Raiva/Irritação',
    'neutral': 'Neutralidade'
}

def analisar_sentimento(descricao: str):
    """
    Analisar o sentimento da descrição do texto usando um modelo PyTorch.
    Retorna um sentimento conforme as categorias definidas.
    """
    # Classificação do texto usando o modelo
    resultado = modelo_sentimento(descricao)
    
    # Aqui, você pode mapear o resultado retornado para os sentimentos definidos
    sentimento_raw = resultado[0]['label'].lower()

    # Mapeando o sentimento para a lista fornecida
    sentimento = sentimentos_mapeados.get(sentimento_raw, 'Neutralidade')

    return sentimento

def salvar_sentimento_acao(acao_id: int, descricao: str):
    """
    Analisar o sentimento de uma ação e salvar no banco de dados.
    """
    # Analisar o sentimento
    sentimento = analisar_sentimento(descricao)

    # Criação da sessão de banco de dados
    db = SessionLocal()
    
    try:
        # Criar a instância do modelo CSSentimento
        dados_sentimento = CSSentimentoCreate(acao_id=acao_id, sentimento=sentimento)
        
        # Criar a entrada no banco de dados
        entrada_sentimento = CSSentimento(**dados_sentimento.dict())
        
        db.add(entrada_sentimento)
        db.commit()  # Salvar a entrada no banco
        db.refresh(entrada_sentimento)  # Atualizar a instância com os dados salvos (como o id gerado)
        
        return entrada_sentimento
    except Exception as e:
        db.rollback()  # Caso haja erro, reverter a transação
        raise e
    finally:
        db.close()
