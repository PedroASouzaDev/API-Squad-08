import torch
import torch.nn as nn
from transformers import AutoTokenizer
from models import CSSentimento, CSAcoes
from database import SessionLocal
from schemas import CSSentimentoCreate

# Configurações
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MAX_LEN = 50
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Classes de sentimento em português
label_encoder_classes = ['Raiva', 'Confusão', 'Frustração', 'Neutro', 'Satisfação', 'Urgência']
num_classes = len(label_encoder_classes)

# Definição da arquitetura do modelo
class SentimentModel(nn.Module):
    def __init__(self, vocab_size, embed_dim=128, hidden_dim=256, output_dim=num_classes):
        super(SentimentModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, input_ids, attention_mask):
        embedded = self.embedding(input_ids)
        lstm_out, _ = self.lstm(embedded)
        output = self.fc(lstm_out[:, -1, :])
        return output

# Carregar modelo treinado
model = SentimentModel(vocab_size=len(tokenizer)).to(device)
model.load_state_dict(torch.load("model/sentiment_model.pth", map_location=device))
model.eval()

def analisar_sentimento(descricao: str):
    """
    Analisar o sentimento da descrição do texto usando o modelo treinado.
    """
    inputs = tokenizer(descricao, padding='max_length', truncation=True, max_length=MAX_LEN, return_tensors="pt")
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask)
        predicted_class = torch.argmax(outputs, dim=1).item()

    sentimento = label_encoder_classes[predicted_class]
    return sentimento

def salvar_sentimento_acao(acao_id: int, descricao: str):
    """
    Analisar o sentimento de uma ação e salvar no banco de dados.
    """
    sentimento = analisar_sentimento(descricao)
    db = SessionLocal()
    
    try:
        dados_sentimento = CSSentimentoCreate(acao_id=acao_id, sentimento=sentimento)
        entrada_sentimento = CSSentimento(**dados_sentimento.dict())
        db.add(entrada_sentimento)
        db.commit()
        db.refresh(entrada_sentimento)
        return entrada_sentimento
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
