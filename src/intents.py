def route_intent(text: str):
    t = text.lower()

    if any(k in t for k in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]):
        return "saudacao", 0.90

    if any(k in t for k in ["erro", "bug", "não funciona", "problema", "suporte", "acesso"]):
        return "suporte", 0.75

    if any(k in t for k in ["fatura", "boleto", "saldo", "cartão", "pagamento"]):
        return "financeiro", 0.70

    return "fallback", 0.40