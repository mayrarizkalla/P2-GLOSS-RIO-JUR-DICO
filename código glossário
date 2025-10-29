import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import random
from bs4 import BeautifulSoup
import re

# Configuração da página
st.set_page_config(
    page_title="Glossário Jurídico",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f3a60;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .term-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #1f3a60;
    }
    .news-card {
        background-color: #e8f4fd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .definition-card {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Dados de exemplo (em um projeto real, estes dados viriam das APIs)
@st.cache_data
def carregar_dados():
    termos = [
        {
            "termo": "Habeas Corpus",
            "definicao": "Remédio constitucional que visa proteger o direito de locomoção do indivíduo, evitando ou cessando violência ou coação em sua liberdade de ir e vir.",
            "area": "Direito Constitucional",
            "fonte": "STF",
            "data": "2023-10-15",
            "exemplo": "O Habeas Corpus foi concedido para um preso que estava encarcerado sem mandado judicial válido.",
            "sinonimos": ["HC", "Remédio Constitucional"],
            "relacionados": ["Mandado de Segurança", "Mandado de Injunção", "Habeas Data"]
        },
        {
            "termo": "Ação Rescisória",
            "definicao": "Ação judicial que tem por objeto desconstituir sentença transitada em julgado, por vícios que a tornam nula ou inexistente.",
            "area": "Direito Processual Civil",
            "fonte": "STJ",
            "data": "2023-09-20",
            "exemplo": "A parte ajuizou ação rescisória para anular sentença proferida com base em documento falso.",
            "sinonimos": ["Rescisão da Sentença"],
            "relacionados": ["Coisa Julgada", "Recurso", "Sentença"]
        },
        {
            "termo": "Usucapião",
            "definicao": "Modo de aquisição da propriedade móvel ou imóvel pela posse prolongada, contínua e incontestada, atendidos os requisitos legais.",
            "area": "Direito Civil",
            "fonte": "Câmara dos Deputados",
            "data": "2023-08-10",
            "exemplo": "O proprietário adquiriu o imóvel por usucapião após 15 anos de posse mansa e pacífica.",
            "sinonimos": ["Prescrição Aquisitiva"],
            "relacionados": ["Propriedade", "Posse", "Direitos Reais"]
        },
        {
            "termo": "Crime Culposo",
            "definicao": "Conduta voluntária que produz resultado ilícito não desejado, decorrente de imprudência, negligência ou imperícia.",
            "area": "Direito Penal",
            "fonte": "STJ",
            "data": "2023-07-25",
            "exemplo": "O motorista foi condenado por crime culposo de homicídio após causar acidente por excesso de velocidade.",
            "sinonimos": ["Culpa", "Delito Culposo"],
            "relacionados": ["Crime Doloso", "Culpa", "Dolo", "Excludentes de Ilicitude"]
        },
        {
            "termo": "Princípio da Isonomia",
            "definicao": "Princípio constitucional que estabelece a igualdade de todos perante a lei, sem distinção de qualquer natureza.",
            "area": "Direito Constitucional",
            "fonte": "STF",
            "data": "2023-06-30",
            "exemplo": "O princípio da isonomia foi invocado para garantir tratamento igualitário a homens e mulheres em concurso público.",
            "sinonimos": ["Igualdade", "Isonomia"],
            "relacionados": ["Princípios Constitucionais", "Direitos Fundamentais", "Discriminação"]
        },
        {
            "termo": "Desconsideração da Personalidade Jurídica",
            "definicao": "Instrumento que permite ultrapassar a autonomia patrimonial da pessoa jurídica para atingir bens particulares de seus sócios.",
            "area": "Direito Empresarial",
            "fonte": "STJ",
            "data": "2023-05-15",
            "exemplo": "A desconsideração da personalidade jurídica foi aplicada para cobrar dívidas da empresa diretamente dos sócios.",
            "sinonimos": ["Desconsideração", "Disregard Doctrine"],
            "relacionados": ["Pessoa Jurídica", "Responsabilidade", "Sociedade"]
        },
        {
            "termo": "Direito Acquirito",
            "definicao": "Direito que não pode ser contestado, por ter sido adquirido de forma legítima e em conformidade com a lei.",
            "area": "Direito Civil",
            "fonte": "Câmara dos Deputados",
            "data": "2023-04-10",
            "exemplo": "O direito de propriedade adquirido por compra e venda regular constitui um direito acquirito.",
            "sinonimos": ["Direito Adquirido"],
            "relacionados": ["Direito Potestativo", "Ato Jurídico", "Eficácia"]
        },
        {
            "termo": "Agravo de Instrumento",
            "definicao": "Recurso cabível contra decisão interlocutória que causa lesão grave e de difícil reparação.",
            "area": "Direito Processual Civil",
            "fonte": "STJ",
            "data": "2023-03-22",
            "exemplo": "O agravo de instrumento foi interposto contra decisão que indeferiu a produção de prova pericial.",
            "sinonimos": ["Agravo"],
            "relacionados": ["Recurso", "Decisão Interlocutória", "Processo Civil"]
        },
        {
            "termo": "Teoria do Fato Consumado",
            "definicao": "Situação em que a prática de um ato ilegal gera consequências irreversíveis, tornando ineficaz a anulação do ato.",
            "area": "Direito Administrativo",
            "fonte": "STF",
            "data": "2023-02-18",
            "exemplo": "A demolição do prédio histórico configurou fato consumado, impossibilitando a reconstrução.",
            "sinonimos": ["Fato Consumado"],
            "relacionados": ["Ato Administrativo", "Anulabilidade", "Nulidade"]
        },
        {
            "termo": "Jus Postulandi",
            "definicao": "Capacidade de postular em juízo, ou seja, de propor ações e defender-se perante o Poder Judiciário.",
            "area": "Direito Processual",
            "fonte": "STJ",
            "data": "2023-01-05",
            "exemplo": "A defensoria pública exerce o jus postulandi em favor dos necessitados.",
            "sinonimos": ["Capacidade Postulatória"],
            "relacionados": ["Legitimidade", "Capacidade Processual", "Representação"]
        }
    ]
    
    # Criar DataFrame
    df = pd.DataFrame(termos)
    
    # Áreas do direito
    areas_direito = [
        "Direito Constitucional", "Direito Civil", "Direito Penal", 
        "Direito Processual Civil", "Direito Empresarial", "Direito Administrativo",
        "Direito do Trabalho", "Direito Tributário", "Direito Ambiental"
    ]
    
    return df, areas_direito

# Função para simular busca de notícias (em projeto real, usaria API do Google News)
def buscar_noticias(termo):
    noticias_simuladas = [
        {
            "titulo": f"Novo entendimento do STF sobre {termo}",
            "fonte": "Consultor Jurídico",
            "data": "2023-10-20",
            "resumo": f"O Supremo Tribunal Federal alterou seu posicionamento acerca do instituto do {termo} em julgamento recente.",
            "url": "#"
        },
        {
            "titulo": f"Especialistas discutem aplicação do {termo} na atualidade",
            "fonte": "Jornal do Direito",
            "data": "2023-10-15",
            "resumo": f"Evento reúne juristas para debater a evolução do conceito de {termo} no ordenamento jurídico brasileiro.",
            "url": "#"
        },
        {
            "titulo": f"Projeto de lei modifica regulamentação do {termo}",
            "fonte": "Câmara dos Deputados",
            "data": "2023-10-10",
            "resumo": f"Proposta em tramitação no Congresso busca atualizar as disposições legais sobre {termo}.",
            "url": "#"
        }
    ]
    return noticias_simuladas

# Função para gerar gráfico de distribuição por área
def criar_grafico_areas(df):
    contagem_areas = df['area'].value_counts().reset_index()
    contagem_areas.columns = ['Área', 'Quantidade']
    
    fig = px.pie(contagem_areas, values='Quantidade', names='Área', 
                 title='Distribuição de Termos por Área do Direito',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    return fig

# Função para gerar gráfico de termos por fonte
def criar_grafico_fontes(df):
    contagem_fontes = df['fonte'].value_counts().reset_index()
    contagem_fontes.columns = ['Fonte', 'Quantidade']
    
    fig = px.bar(contagem_fontes, x='Fonte', y='Quantidade',
                 title='Quantidade de Termos por Fonte',
                 color='Quantidade',
                 color_continuous_scale='Blues')
    
    fig.update_layout(height=400, xaxis_tickangle=-45)
    
    return fig

# Inicialização do estado da sessão
if 'termo_selecionado' not in st.session_state:
    st.session_state.termo_selecionado = None

# Carregar dados
df, areas_direito = carregar_dados()

# Interface principal
st.markdown('<h1 class="main-header">⚖️ Glossário Jurídico</h1>', unsafe_allow_html=True)
st.markdown("### Descomplicando o Direito para estudantes e leigos")

# Barra lateral
with st.sidebar:
    st.image("https://cdn.pixabay.com/photo/2017/01/31/14/26/law-2024670_1280.png", width=100)
    st.title("Navegação")
    
    # Busca
    st.subheader("Buscar Termo")
    termo_busca = st.text_input("Digite o termo jurídico:")
    
    # Filtros
    st.subheader("Filtros")
    area_selecionada = st.selectbox("Área do Direito", ["Todas"] + areas_direito)
    fonte_selecionada = st.selectbox("Fonte", ["Todas"] + list(df['fonte'].unique()))
    
    # Lista de termos
    st.subheader("Termos Populares")
    for termo in df['termo'].head(5):
        if st.button(termo, key=f"btn_{termo}"):
            st.session_state.termo_selecionado = termo

# Conteúdo principal
tab1, tab2, tab3 = st.tabs(["Início", "Explorar Termos", "Sobre o Projeto"])

with tab1:
    st.markdown("### Bem-vindo ao Glossário Jurídico Digital")
    st.write("""
    Este site foi desenvolvido para descomplicar o Direito, tornando os termos jurídicos 
    acessíveis para estudantes, profissionais e qualquer pessoa interessada em entender 
    melhor o universo jurídico.
    
    **Recursos disponíveis:**
    - Busca inteligente por termos jurídicos
    - Definições claras e exemplos práticos
    - Notícias recentes relacionadas aos termos
    - Filtros por área do direito e fonte
    - Visualizações gráficas da distribuição dos termos
    """)
    
    # Gráficos na página inicial
    col1, col2 = st.columns(2)
    
    with col1:
        fig_areas = criar_grafico_areas(df)
        st.plotly_chart(fig_areas, use_container_width=True)
    
    with col2:
        fig_fontes = criar_grafico_fontes(df)
        st.plotly_chart(fig_fontes, use_container_width=True)
    
    # Termos recentes
    st.markdown("### Termos Recentemente Adicionados")
    termos_recentes = df.sort_values('data', ascending=False).head(3)
    
    for _, termo in termos_recentes.iterrows():
        with st.expander(f"**{termo['termo']}** - {termo['area']}"):
            st.write(termo['definicao'])
            if st.button("Ver detalhes", key=f"detalhes_{termo['termo']}"):
                st.session_state.termo_selecionado = termo['termo']
                st.experimental_rerun()

with tab2:
    st.markdown("### Explorar Termos Jurídicos")
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if area_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['area'] == area_selecionada]
    
    if fonte_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['fonte'] == fonte_selecionada]
    
    if termo_busca:
        df_filtrado = df_filtrado[
            df_filtrado['termo'].str.contains(termo_busca, case=False, na=False) |
            df_filtrado['definicao'].str.contains(termo_busca, case=False, na=False) |
            df_filtrado['sinonimos'].apply(lambda x: any(termo_busca.lower() in s.lower() for s in x) if x else False)
        ]
    
    # Exibir termos filtrados
    if len(df_filtrado) > 0:
        st.write(f"**{len(df_filtrado)}** termo(s) encontrado(s)")
        
        for _, termo in df_filtrado.iterrows():
            with st.container():
                st.markdown(f'<div class="term-card">', unsafe_allow_html=True)
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"#### {termo['termo']}")
                    st.write(termo['definicao'])
                    st.caption(f"Área: {termo['area']} | Fonte: {termo['fonte']} | Data: {termo['data']}")
                
                with col2:
                    if st.button("Ver detalhes", key=f"ver_{termo['termo']}"):
                        st.session_state.termo_selecionado = termo['termo']
                        st.experimental_rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhum termo encontrado com os filtros aplicados. Tente alterar os critérios de busca.")

with tab3:
    st.markdown("### Sobre o Projeto")
    st.write("""
    **Glossário Jurídico: Descomplicando o Direito**
    
    Este projeto foi desenvolvido por estudantes de Direito que identificaram a dificuldade
    de acesso a conceitos jurídicos por parte de iniciantes na área e leigos.
    
    **Objetivos:**
    - Fornecer definições claras e acessíveis de termos jurídicos
    - Contextualizar os conceitos com exemplos práticos e jurisprudenciais
    - Integrar notícias recentes relacionadas aos termos pesquisados
    - Oferecer uma ferramenta de estudo gratuita e atualizada
    
    **Tecnologias utilizadas:**
    - Streamlit para a interface web
    - Python como linguagem principal
    - APIs jurídicas para dados atualizados
    - Google News API para integração com notícias
    - Web scraping para complementar as bases de dados
    
    **Fontes de dados:**
    - API do STF (Supremo Tribunal Federal)
    - Tesauro Jurídico do STJ (Superior Tribunal de Justiça)
    - Dicionário Jurídico da Câmara dos Deputados
    - Base de dados do Planalto para legislação federal
    """)
    
    st.markdown("---")
    st.markdown("**Desenvolvido por:** Carolina Souza, Lara Carneiro e Mayra Rizkalla")
    st.markdown("**Turma A** - Projeto P2 Programação 2")

# Página de detalhes do termo (se um termo foi selecionado)
if st.session_state.termo_selecionado:
    st.markdown("---")
    termo_detalhes = df[df['termo'] == st.session_state.termo_selecionado].iloc[0]
    
    st.markdown(f'<div class="definition-card">', unsafe_allow_html=True)
    st.markdown(f"# {termo_detalhes['termo']}")
    st.markdown(f"**Área:** {termo_detalhes['area']} | **Fonte:** {termo_detalhes['fonte']} | **Data:** {termo_detalhes['data']}")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Definição")
        st.write(termo_detalhes['definicao'])
        
        st.markdown("### Exemplo Prático")
        st.write(termo_detalhes['exemplo'])
        
        st.markdown("### Termos Relacionados")
        for relacionado in termo_detalhes['relacionados']:
            st.write(f"- {relacionado}")
    
    with col2:
        st.markdown("### Sinônimos")
        for sinonimo in termo_detalhes['sinonimos']:
            st.write(f"- {sinonimo}")
        
        st.markdown("### Visualização")
        # Gráfico simples para o termo
        areas_count = df['area'].value_counts()
        fig_termo = go.Figure(data=[go.Bar(
            x=areas_count.index,
            y=areas_count.values,
            marker_color=['#1f3a60' if area == termo_detalhes['area'] else '#a0aec0' for area in areas_count.index]
        )])
        
        fig_termo.update_layout(
            title=f"Distribuição de Termos por Área",
            xaxis_title="Área do Direito",
            yaxis_title="Quantidade de Termos",
            height=300
        )
        
        st.plotly_chart(fig_termo, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Seção de notícias
    st.markdown("### Notícias Recentes")
    noticias = buscar_noticias(termo_detalhes['termo'])
    
    for noticia in noticias:
        with st.container():
            st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
            st.markdown(f"#### {noticia['titulo']}")
            st.write(noticia['resumo'])
            st.caption(f"Fonte: {noticia['fonte']} | Data: {noticia['data']}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão para voltar
    if st.button("Voltar para a lista de termos"):
        st.session_state.termo_selecionado = None
        st.experimental_rerun()
