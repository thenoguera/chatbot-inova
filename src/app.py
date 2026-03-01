from fastapi import FastAPI
from pydantic import BaseModel

from src.policies import sanitize_text
from src.intents import route_intent
from src.rag import retrieve
from src.metrics import summarize

app = FastAPI(title="Chatbot MVP - Desafio ICT Itaú")
@app.get("/metrics")
def metrics():
    return summarize()
class ChatRequest(BaseModel):
    user_id: str = "anon"
    message: str

class ChatResponse(BaseModel):
    intent: str
    answer: str
    confidence: float
from src.feedback import save_feedback

class FeedbackRequest(BaseModel):
    user_id: str = "anon"
    message: str
    intent: str
    helpful: bool
    comment: str | None = None

@app.post("/feedback")
def feedback(req: FeedbackRequest):
    save_feedback(req.model_dump())
    return {"status": "saved"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    clean = sanitize_text(req.message)
    intent, confidence = route_intent(clean)

    # 1) tenta buscar na base de conhecimento
    kb_hits = retrieve(clean, top_k=1)
    if kb_hits:
        filename, snippet, score = kb_hits[0]
        if score >= 0.10:
            answer = (
                "Encontrei uma orientação na base de conhecimento.\n\n"
                f"Resumo: {snippet}\n\n"
                f"Fonte: {filename} (score={score:.2f})"
            )
            return ChatResponse(intent=intent, answer=answer, confidence=confidence)

    # 2) fallback (sem KB)
    answer = {
        "saudacao": "Olá! Como posso ajudar hoje?",
        "suporte": "Entendi. Qual erro aparece e em qual sistema/serviço ocorreu?",
        "financeiro": "Certo. É sobre qual assunto (fatura, boleto, saldo, cartão, pagamento)?",
        "fallback": "Não tenho confiança suficiente. Posso encaminhar para atendimento humano?"
    }.get(intent, "Como posso ajudar?")

    return ChatResponse(intent=intent, answer=answer, confidence=confidence)


