import re

def sanitize_text(text: str) -> str:
    text = text.strip()
    # Exemplo simples: mascara CPF (não é perfeito, mas demonstra cuidado)
    text = re.sub(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", "[CPF]", text)
    text = re.sub(r"\b\d{11}\b", "[CPF]", text)
    return text