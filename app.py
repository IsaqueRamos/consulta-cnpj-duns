import streamlit as st
import requests

# Configuração da página
st.set_page_config(
    page_title="Assistente de Cadastro DUNS",
    page_icon="🏢",
    layout="centered"
)

# Estilização CSS personalizada para Tema Escuro Profissional
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 24px;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 24px;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .header-title {
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        color: #38bdf8;
    }
    .header-subtitle {
        font-size: 14px;
        color: #94a3b8;
        margin-top: 6px;
    }

    .stButton>button {
        width: 100%;
        background-color: #2563eb;
        color: #ffffff;
        font-weight: 600;
        font-size: 15px;
        border-radius: 8px;
        height: 2.8em;
        border: none;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: #ffffff;
    }

    .stCodeBlock {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    .stTextInput>div>div>input {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 8px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #38bdf8;
    }

    .duns-form-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    .duns-success-box {
        background-color: #064e3b;
        border: 1px solid #059669;
        border-left: 6px solid #10b981;
        padding: 18px;
        border-radius: 10px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Principal
st.markdown("""
    <div class="header-container">
        <div class="header-title">🏢 Assistente de Cadastro DUNS</div>
        <div class="header-subtitle">Digite o CNPJ para preencher os campos de pesquisa do DUNS automaticamente.</div>
    </div>
""", unsafe_allow_html=True)

# Entrada do CNPJ
with st.container():
    cnpj_input = st.text_input("Número do CNPJ", placeholder="Digite apenas os 14 números (ex: 14921638000170)", max_chars=18)
    btn_consultar = st.button("🔍 Consultar CNPJ & Gerar Campos DUNS")

def consultar_cnpj(cnpj):
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj_limpo) != 14:
        return None, "O CNPJ deve conter exatamente 14 dígitos numéricos."
    
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, "CNPJ não encontrado na base de dados da Receita Federal."
        else:
            return None, f"Erro ao consultar CNPJ. Código HTTP: {response.status_code}"
    except Exception as e:
        return None, f"Falha na conexão com o servidor: {str(e)}"

if btn_consultar and cnpj_input:
    with st.spinner("Buscando dados na Receita Federal..."):
        dados, erro = consultar_cnpj(cnpj_input)
        if erro:
            st.error(erro)
        else:
            st.session_state['dados_empresa'] = dados

# Formulario de Pesquisa DUNS gerado na página
if 'dados_empresa' in st.session_state:
    dados = st.session_state['dados_empresa']
    
    st.markdown("---")
    st.success("✅ **Campos do D-U-N-S Search preenchidos na página!** Use as folhinhas (📋) para copiar rapidamente.")

    # Extração de dados
    razao_social = dados.get('razao_social', '')
    logradouro = dados.get('logradouro', '')
    numero = dados.get('numero', '')
    bairro = dados.get('bairro', '')
    municipio = dados.get('municipio', '')
    uf = dados.get('uf', '')
    cep = dados.get('cep', '')
    
    endereco_linha = f"{logradouro}, {numero} - {bairro}"

    # Formulário visual "D-U-N-S Search" dentro da página
    st.markdown('### 📑 Formulário D-U-N-S Search (Dados Extraídos)')
    
    st.markdown("**Country:**")
    st.code("Brazil", language=None)

    st.markdown("**Full Legal Business Name:**")
    st.code(razao_social, language=None)

    st.markdown("**Address:**")
    st.code(endereco_linha, language=None)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**City:**")
        st.code(municipio, language=None)
    with col2:
        st.markdown("**State / Region / Territory:**")
        st.code(uf, language=None)
    with col3:
        st.markdown("**Postal Code:**")
        st.code(cep, language=None)

    st.markdown("---")
    
    # Redirecionamento
    url_formulario_duns = "https://support.dnb.com/?CUST=APPLEDEV"
    
    st.markdown("### 🎯 Finalizar Busca no Portal")
    st.info("Clique no botão abaixo para abrir a tela de validação da D&B:")
    
    st.markdown(f'''
        <a href="{url_formulario_duns}" target="_blank" style="text-decoration: none;">
            <button style="
                width: 100%;
                background: linear-gradient(135deg, #059669 0%, #047857 100%);
                color: white;
                padding: 12px;
                font-weight: 600;
                font-size: 16px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 0 4px 10px rgba(5, 150, 105, 0.3);
                transition: all 0.2s ease;">
                🌐 Enviar para a Consulta Oficial (D-U-N-S Search)
            </button>
        </a>
    ''', unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Registro final
    duns_numero = st.text_input("Número DUNS retornado:", placeholder="Cole o código DUNS encontrado aqui para registrar...")
    
    if duns_numero:
        st.markdown(f'''
        <div class="duns-success-box">
            <h4 style="margin:0; color: #a7f3d0;">✅ Registro Concluído com Sucesso!</h4>
            <p style="margin-top: 8px; margin-bottom: 4px; color: #f1f5f9;"><strong>Razão Social:</strong> {razao_social}</p>
            <p style="margin-bottom: 4px; color: #f1f5f9;"><strong>CNPJ:</strong> {dados.get('cnpj')}</p>
            <p style="margin-bottom: 0; color: #f1f5f9;"><strong>Código DUNS:</strong> <code style="font-size: 16px; background-color: #022c22; padding: 2px 8px; border-radius: 4px; color: #6ee7b7;">{duns_numero}</code></p>
        </div>
        ''', unsafe_allow_html=True)
