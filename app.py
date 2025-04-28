import streamlit as st
from fuzzywuzzy import fuzz, process
import json

st.set_page_config(page_title="Chat de Regras – Auditoria, Moskit e 360", layout="centered")
st.title("🤖 Chat Inteligente – Regras, Moskit e Solução 360")
st.write("Digite sua dúvida sobre modelos de gestão, Moskit ou 360:")

# Carregar a base de conhecimento
@st.cache_data(ttl=0)
def carregar_base():
    with open("base_conhecimento.json", "r", encoding="utf-8") as f:
        return json.load(f)

base_conhecimento = carregar_base()

pergunta = st.text_input("Sua dúvida:")

# Função para encontrar a resposta com base na pergunta do usuário
def encontrar_resposta(pergunta_usuario):
    todas_chaves = []
    mapa_respostas = {}

    # Preenche as chaves e respostas a partir da base de conhecimento
    for categoria, perguntas in base_conhecimento.items():
        for chave, resposta in perguntas.items():
            todas_chaves.append(chave)
            mapa_respostas[chave] = resposta

    # Verificar se a pergunta é sobre "modelo de gestão"
    if verificar_modelo_de_gestao(pergunta_usuario.lower()):
        return mapa_respostas["modelo de gestão"]  # Resposta para "Modelos de Gestão"

    # Verificar se a pergunta é sobre "cadastrar empresa no Moskit"
    if verificar_cadastrar_empresa_moskit(pergunta_usuario.lower()):
        return mapa_respostas["cadastrar empresa no moskit"]

    # Verificar se a pergunta é sobre "funil" ou "etapas"
    if verificar_funil_etapas(pergunta_usuario.lower()):
        return mapa_respostas["funil (etapas) do moskit"]

    # Verificar se a pergunta é sobre "ID" da empresa
    if verificar_id_empresa_moskit(pergunta_usuario.lower()):
        return mapa_respostas["id da empresa moskit"]

    # Verificar se a pergunta é sobre "360"
    if verificar_360(pergunta_usuario.lower()):
        return mapa_respostas["Sistema 360"]

    # Verificar se a pergunta é sobre "proposta no 360"
    if verificar_proposta_360(pergunta_usuario.lower()):
        return mapa_respostas["como preencher proposta no 360"]

    # Verificar se a pergunta é sobre "tipo de proposta"
    if verificar_tipo_proposta(pergunta_usuario.lower()):
        return mapa_respostas["Tipo de proposta (porte)"]

    # Verificar se a pergunta é sobre "diagnóstico"
    if verificar_diagnostico(pergunta_usuario.lower()):
        return mapa_respostas["diagnóstico no 360"]

    # Verificar se a pergunta é sobre "combo"
    if verificar_combo(pergunta_usuario.lower()):
        return mapa_respostas["combo sst no 360"]

    # Verificar se a pergunta é sobre "unidade executora"
    if verificar_unidade_executora(pergunta_usuario.lower()):
        return mapa_respostas["unidade executora 360"]

    # Verificar se a pergunta é sobre "aba produto"
    if verificar_aba_produto(pergunta_usuario.lower()):
        return mapa_respostas["aba produto não aparece"]

    # Verificar se a pergunta é sobre "sebrae"
    if verificar_sebrae(pergunta_usuario.lower()):
        return mapa_respostas["sebrae"]
    
    # Verificar se a pergunta é sobre "mensal"
    if verificar_mensal(pergunta_usuario.lower()):
        return mapa_respostas["mensal"]

    # Verificar se a pergunta é sobre "após execução"
    if verificar_apos_execucao(pergunta_usuario.lower()):
        return mapa_respostas["após execução"]

    # Verificar se a pergunta é sobre "após assinatura"
    if verificar_apos_assinatura(pergunta_usuario.lower()):
        return mapa_respostas["após assinatura"]

    # Verificar se a pergunta é sobre "após pagamento"
    if verificar_apos_pagamento(pergunta_usuario.lower()):
        return mapa_respostas["após pagamento"]
         
    # Verificar se a pergunta é sobre "forma de pagamento"
    if verificar_forma_pagamento(pergunta_usuario.lower()):
        return mapa_respostas["forma de pagamento"]

    # Verificar se a pergunta é sobre "link"
    if verificar_link(pergunta_usuario.lower()):
        return mapa_respostas["link, não gerou link"]

    # Verificar se a pergunta é sobre fontes financiadoras
    if verificar_fonte_financiadora(pergunta_usuario.lower()):
        return obter_informacoes_fonte_financiadora()

    # Verificar se a pergunta é sobre formas de pagamento
    if verificar_pagamento(pergunta_usuario.lower()):
        return obter_informacoes_pagamento(pergunta_usuario)

    # Encontrar a melhor correspondência usando fuzzy matching
    melhor, score = process.extractOne(pergunta_usuario.lower(), todas_chaves, scorer=fuzz.partial_ratio)

    # Se a correspondência for boa (score >= 70), retorna a resposta
    if score >= 70:
        return mapa_respostas[melhor]
    else:
        # Caso contrário, sugere possíveis perguntas que podem ser o que o usuário quis dizer
        sugestões = [m for m, s in process.extract(pergunta_usuario.lower(), todas_chaves, limit=3) if s >= 50]
        if sugestões:
            sugestao_txt = "\n".join([f"- {s}" for s in sugestões])
            return f"🤔 Não encontrei resposta exata, mas talvez você quis dizer:\n\n{suggestao_txt}"
        return "❌ Ainda não sei responder essa pergunta. Tente outra pergunta ou fale com o Mateus!"


# Função para verificar se a pergunta é sobre "modelo de gestão"
def verificar_modelo(pergunta_usuario):
    palavra_chave_modelo = "modelo de gestão"
    
    # Verificar se a palavra "modelo" está na pergunta
    if fuzz.partial_ratio(pergunta_usuario, palavra_chave_modelo) > 80:
        return True
    return False

# Função para verificar se a pergunta é sobre "cadastrar empresa no Moskit"
def verificar_cadastrar_empresa_moskit(pergunta_usuario):
    palavras_chave_cadastro = [
        "cadastrar empresa no moskit", 
        "cadastrar", 
        "cadastro de empresa no moskit", 
        "incluir empresa no moskit"
    ]
    
    for palavra in palavras_chave_cadastro:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar se a pergunta é sobre fontes financiadoras
def verificar_fonte_financiadora(pergunta_usuario):
    fontes_financiadoras = ["fonte financiadora", "B + P", "Procompi", "ABDI"]
    for fonte in fontes_financiadoras:
        if fuzz.partial_ratio(pergunta_usuario, fonte) > 80:
            return True
    return False

# Função para retornar informações gerais sobre fontes financiadoras
def obter_informacoes_fonte_financiadora():
    return """
    🔹 **Fonte Financiadora**:
    - Para **fontes financiadoras** como **Procompi**, **B + P**, **ABDI**, etc., deve-se utilizar o **modelo Após Execução** com **Depósito em Conta**.
    """

# Função para verificar se a pergunta é sobre formas de pagamento
def verificar_pagamento(pergunta_usuario):
    palavras_chave = ["boleto", "cartão de crédito", "cartão de débito", "depósito em conta", "pix", "transferência"]
    for palavra in palavras_chave:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "funil" ou "etapas" no Moskit
def verificar_funil_etapas(pergunta_usuario):
    palavras_chave_funil_etapas = ["etapas", "funil"]
    for palavra in palavras_chave_funil_etapas:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "ID" da empresa no Moskit
def verificar_id_empresa_moskit(pergunta_usuario):
    palavras_chave_id = ["id"]
    for palavra in palavras_chave_id:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "360"
def verificar_360(pergunta_usuario):
    palavras_chave_360 = ["360"]
    for palavra in palavras_chave_360:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "proposta no 360"
def verificar_proposta_360(pergunta_usuario):
    palavras_chave_proposta_360 = ["proposta no 360", "a proposta", "proposta"]
    for palavra in palavras_chave_proposta_360:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "Tipo de proposta"
def verificar_tipo_proposta(pergunta_usuario):
    palavras_chave_tipo_proposta = ["tipo de proposta", "porte"]
    for palavra in palavras_chave_tipo_proposta:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "diagnóstico"
def verificar_diagnostico(pergunta_usuario):
    palavras_chave_diagnostico = ["diagnóstico"]
    for palavra in palavras_chave_diagnostico:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "combo"
def verificar_combo(pergunta_usuario):
    palavras_chave_combo = ["combo"]
    for palavra in palavras_chave_combo:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "unidade executora"
def verificar_unidade_executora(pergunta_usuario):
    palavras_chave_unidade_executora = ["unidade executora"]
    for palavra in palavras_chave_unidade_executora:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "aba produto"
def verificar_aba_produto(pergunta_usuario):
    palavras_chave_aba_produto = ["aba produto", "aba do produto", "produto"]
    for palavra in palavras_chave_aba_produto:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar "sebrae"
def verificar_sebrae(pergunta_usuario):
    palavras_chave_sebrae = ["sebrae"]
    for palavra in palavras_chave_sebrae:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

def verificar_mensal(pergunta_usuario):
    palavras_chave_mensal = ["mensal", "modelo mensal"]
    for palavra in palavras_chave_mensal:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

def verificar_apos_execucao(pergunta_usuario):
    palavras_chave_apos_execucao = ["após execução", "modelo após execução"]
    for palavra in palavras_chave_apos_execucao:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

def verificar_apos_assinatura(pergunta_usuario):
    palavras_chave_apos_assinatura = ["após assinatura", "modelo após assinatura"]
    for palavra in palavras_chave_apos_assinatura:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

def verificar_apos_pagamento(pergunta_usuario):
    palavras_chave_apos_pagamento = ["após pagamento", "modelo após pagamento"]
    for palavra in palavras_chave_apos_pagamento:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Função para verificar se a pergunta é sobre "forma de pagamento"
def verificar_forma_pagamento(pergunta_usuario):
    palavras_chave_pagamento = ["forma de pagamento", "pagamento"]
    for palavra in palavras_chave_pagamento:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

    if respostas:
        return "\n".join(respostas)
    else:
        return "❌ Não encontrei informações sobre essa forma de pagamento. Tente outra forma ou fale com o Mateus!"

# Função para verificar se a pergunta é sobre "link"
def verificar_link(pergunta_usuario):
    palavras_chave_link = ["link"]
    
    for palavra in palavras_chave_link:
        if fuzz.partial_ratio(pergunta_usuario, palavra) > 80:
            return True
    return False

# Quando o usuário digita a pergunta, tenta encontrar a resposta
if pergunta:
    resposta = encontrar_resposta(pergunta)
    st.write(resposta)

# Gerenciar o histórico de perguntas
if "historico" not in st.session_state:
    st.session_state.historico = []

if pergunta:
    st.session_state.historico.append(pergunta)

# Exibe o histórico de perguntas
if st.session_state.historico:
    with st.expander("📜 Ver histórico"):
        for h in reversed(st.session_state.historico[-5:]):
            st.markdown(f"• {h}")
