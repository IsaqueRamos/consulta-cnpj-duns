import streamlit as st
import requests

st.set_page_config(
    page_title="Consulta DUNS por CNPJ",
    page_icon="🏢",
    layout="centered"
)

st.markdown('''
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #0d6efd;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        border: none;
    }
    .duns-box {
        background-color: #e7f1ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #0d6efd;
        margin-top: 15px;
    }
    </style>
''', unsafe_allow_html=True)

st.title("🏢 Localizador de DUNS via CNPJ")
st.markdown("Digite o CNPJ abaixo para extrair os dados e preencher na tela do D-U-N-S Search.")

st.divider()

cnpj_input = st.text_input("Número do CNPJ", placeholder="Digite apenas números (ex: 14921638000170)", max_chars=18)
btn_consultar = st.button("🔍 Consultar CNPJ")

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
            return None, "CNPJ não encontrado na base de dados."
        else:
            return None, f"Erro ao consultar CNPJ. Código: {response.status_code}"
    except Exception as e:
        return None, f"Falha na conexão: {str(e)}"

if btn_consultar and cnpj_input:
    with st.spinner("Buscando dados cadastrais..."):
        dados, erro = consultar_cnpj(cnpj_input)
        if erro:
            st.error(erro)
        else:
            st.session_state['dados_empresa'] = dados

if 'dados_empresa' in st.session_state:
    dados = st.session_state['dados_empresa']
    st.success("✅ CNPJ localizado com sucesso!")
    
    # Extração de campos para o formulário D-U-N-S Search
    razao_social = dados.get('razao_social', '')
    logradouro = dados.get('logradouro', '')
    numero = dados.get('numero', '')
    bairro = dados.get('bairro', '')
    municipio = dados.get('municipio', '')
    uf = dados.get('uf', '')
    cep = dados.get('cep', '')
    
    endereco_linha = f"{logradouro}, {numero} - {bairro}"
    
    st.subheader("📌 Dados da Empresa para a Tela de Busca")
    
    # Exibição dos campos fáceis de selecionar e copiar
    st.text_input("Full Legal Business Name:", value=razao_social)
    st.text_input("Address:", value=endereco_linha)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("City:", value=municipio)
    with col2:
        st.text_input("State / Region:", value=uf)
    with col3:
        st.text_input("Postal Code:", value=cep)
    
    st.divider()
    
    # Link direto fornecido do formulário D&B Apple Developer
    url_formulario_duns = "https://support.dnb.com/?CUST=APPLEDEV"
    
    st.subheader("🎯 Abrir Formulário D-U-N-S Search")
    st.info("Copie os dados gerados nos campos acima e clique no botão para abrir a tela de busca do DUNS:")
    
    st.markdown(f'''
        <a href="{url_formulario_duns}" target="_blank">
            <button style="width:100%; background-color:#198754; color:white; padding:12px; font-weight:bold; border:none; border-radius:8px; cursor:pointer;">
                🌐 Abrir Formulário D-U-N-S Search (AppleDev)
            </button>
        </a>
    ''', unsafe_allow_html=True)
    
    st.write("")
    duns_numero = st.text_input("Número DUNS localizado:", placeholder="Cole o número DUNS encontrado para registrar")
    
    if duns_numero:
        st.markdown(f'''
        <div class="duns-box">
            <h4>✅ Registro Concluído</h4>
            <p><strong>Empresa:</strong> {razao_social}</p>
            <p><strong>CNPJ:</strong> {dados.get('cnpj')}</p>
            <p><strong>Número DUNS:</strong> <code>{duns_numero}</code></p>
        </div>
        ''', unsafe_allow_html=True)
