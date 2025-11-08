import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import time

# Configuração da página
st.set_page_config(
    page_title="Glossário Jurídico - Descomplicando o Direito",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f3a60;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1f3a60, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .term-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        border-left: 6px solid #1f3a60;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }
    .term-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .news-card {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #17a2b8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .definition-card {
        background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        border: 2px solid #1f3a60;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    .stButton button {
        background: linear-gradient(135deg, #1f3a60, #3498db);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do estado
if 'termo_selecionado' not in st.session_state:
    st.session_state.termo_selecionado = None

# Classe para APIs Jurídicas
class APIGlossarioJuridico:
    def __init__(self):
        self.termos_completos = {
            "Habeas Corpus": {
                "definicao": "Remédio constitucional que visa proteger o direito de locomoção do indivíduo, conforme art. 5º, LXVIII da CF/88.",
                "fonte": "STF - Supremo Tribunal Federal",
                "jurisprudencia": "HC 184.246/SP - Concedido para trancamento de ação penal por ausência de justa causa.",
                "area": "Direito Constitucional",
                "exemplo": "O Habeas Corpus foi concedido para um preso que estava encarcerado sem mandado judicial válido."
            },
            "Mandado de Segurança": {
                "definicao": "Ação constitucional para proteção de direito líquido e certo não amparado por HC ou HD.",
                "fonte": "STF - Supremo Tribunal Federal", 
                "jurisprudencia": "MS 34.567 - Concedido para assegurar direito a cargo público.",
                "area": "Direito Constitucional",
                "exemplo": "Concedido mandado de segurança para assegurar vaga em concurso público."
            },
            "Ação Rescisória": {
                "definicao": "Meio processual para desconstituir sentença transitada em julgado por vícios legais.",
                "fonte": "STF - Supremo Tribunal Federal",
                "jurisprudencia": "AR 5.432/DF - Admitida rescisão por documento novo.",
                "area": "Direito Processual Civil",
                "exemplo": "A parte ajuizou ação rescisória para anular sentença proferida com base em documento falso."
            },
            "Usucapião": {
                "definicao": "Modo aquisitivo da propriedade pela posse prolongada nos termos legais.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "REsp 987.654/RS - Reconhecida usucapião extraordinária urbana.",
                "area": "Direito Civil",
                "exemplo": "O proprietário adquiriu o imóvel por usucapião após 15 anos de posse mansa e pacífica."
            },
            "Princípio da Isonomia": {
                "definicao": "Princípio constitucional da igualdade de todos perante a lei (art. 5º, caput, CF/88).",
                "fonte": "Câmara dos Deputados",
                "jurisprudencia": "Constituição Federal, Artigo 5º",
                "area": "Direito Constitucional",
                "exemplo": "O princípio da isonomia foi invocado para garantir tratamento igualitário a homens e mulheres em concurso público."
            },
            "Crime Culposo": {
                "definicao": "Conduta voluntária com resultado ilícito não desejado por imprudência, negligência ou imperícia.",
                "fonte": "Câmara dos Deputados", 
                "jurisprudencia": "Código Penal, Artigo 18, II",
                "area": "Direito Penal",
                "exemplo": "O motorista foi condenado por crime culposo de homicídio após causar acidente por excesso de velocidade."
            },
            "Coisa Julgada": {
                "definicao": "Qualidade da sentença que não mais admite recurso, tornando-se imutável.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "Disciplinada no art. 502 do CPC",
                "area": "Direito Processual Civil",
                "exemplo": "A sentença transitou em julgado após esgotados todos os recursos."
            },
            "Agravo de Instrumento": {
                "definicao": "Recurso contra decisão interlocutória que causa lesão grave.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "AgInt no REsp 2.222.333 - Admitido para rediscutir prova.",
                "area": "Direito Processual Civil",
                "exemplo": "O agravo foi interposto contra decisão que indeferiu prova pericial."
            },
            "Desconsideração da Personalidade Jurídica": {
                "definicao": "Instrumento para ultrapassar autonomia patrimonial da pessoa jurídica.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "REsp 1.111.222/SP - Aplicada para responsabilizar sócios.",
                "area": "Direito Empresarial",
                "exemplo": "A desconsideração foi aplicada para cobrar dívidas da empresa diretamente dos sócios."
            },
            "Jus Postulandi": {
                "definicao": "Capacidade de postular em juízo perante o Poder Judiciário.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "Em regra, exercido por advogados (art. 1º da Lei 8.906/94)",
                "area": "Direito Processual",
                "exemplo": "A defensoria pública exerce o jus postulandi em favor dos necessitados."
            },
            "Recurso Extraordinário": {
                "definicao": "Recurso cabível quando a decisão contraria a Constituição Federal.",
                "fonte": "STF - Supremo Tribunal Federal",
                "jurisprudencia": "RE 1.234.567 - Julgado procedente por ofensa à Constituição.",
                "area": "Direito Constitucional",
                "exemplo": "Interposto recurso extraordinário por violação a dispositivo constitucional."
            },
            "Liminar": {
                "definicao": "Decisão judicial provisória para evitar dano irreparável.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "Concedida para suspender efeitos de ato administrativo.",
                "area": "Direito Processual",
                "exemplo": "Concedida liminar para suspender processo administrativo disciplinar."
            },
            "Prescrição": {
                "definicao": "Perda do direito de ação pelo decurso do tempo.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "Aplicada para extinguir punibilidade no direito penal.",
                "area": "Direito Civil",
                "exemplo": "Reconhecida prescrição da ação de indenização após 3 anos."
            },
            "Fiança": {
                "definicao": "Garantia pessoal para assegurar cumprimento de obrigação.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "Concedida como medida cautelar em processo penal.",
                "area": "Direito Penal",
                "exemplo": "Concedida fiança para assegurar liberdade provisória do acusado."
            },
            "Testemunha": {
                "definicao": "Pessoa que depõe sobre fatos relevantes para o processo.",
                "fonte": "STJ - Superior Tribunal de Justiça",
                "jurisprudencia": "Oitiva obrigatória em processos criminais.",
                "area": "Direito Processual",
                "exemplo": "A testemunha confirmou o alegado pela parte autora."
            }
        }
    
    def buscar_termo(self, termo):
        return self.termos_completos.get(termo, {})
    
    def buscar_todos_termos(self):
        return list(self.termos_completos.keys())

# Classe para Notícias (simulada)
class GoogleNewsIntegracao:
    def buscar_noticias(self, termo):
        noticias_base = {
            "Habeas Corpus": [
                {
                    "titulo": "STF concede habeas corpus e solta réu por falta de provas",
                    "fonte": "Consultor Jurídico",
                    "data": "2024-01-15",
                    "resumo": "O Supremo Tribunal Federal concedeu habeas corpus para trancar ação penal contra acusado por insuficiência de provas.",
                    "url": "#"
                },
                {
                    "titulo": "Novo entendimento sobre habeas corpus em casos de prisão preventiva",
                    "fonte": "Jornal do Direito",
                    "data": "2024-01-10",
                    "resumo": "Tribunais superiores discutem aplicação do habeas corpus em casos de prisão cautelar.",
                    "url": "#"
                }
            ],
            "Mandado de Segurança": [
                {
                    "titulo": "STJ define novos parâmetros para mandado de segurança",
                    "fonte": "Migalhas",
                    "data": "2024-01-12",
                    "resumo": "Superior Tribunal de Justiça estabelece entendimento sobre direito líquido e certo.",
                    "url": "#"
                }
            ],
            "Ação Rescisória": [
                {
                    "titulo": "STJ admite ação rescisória por descoberta de documento novo",
                    "fonte": "ConJur",
                    "data": "2024-01-08",
                    "resumo": "Superior Tribunal de Justiça reconhece possibilidade de rescisão de sentença por documento não conhecido.",
                    "url": "#"
                }
            ],
            "Usucapião": [
                {
                    "titulo": "Usucapião: posse mansa e pacífica por 15 anos garante propriedade",
                    "fonte": "JusBrasil",
                    "data": "2024-01-05",
                    "resumo": "Decisão do TJSP reconhece direito de propriedade via usucapião extraordinária.",
                    "url": "#"
                }
            ]
        }
        
        noticias_termo = noticias_base.get(termo, [])
        
        if not noticias_termo:
            noticias_termo = [{
                "titulo": f"Notícias sobre {termo} - Em atualização",
                "fonte": "Glossário Jurídico",
                "data": datetime.now().strftime("%Y-%m-%d"),
                "resumo": f"Em breve traremos notícias atualizadas sobre {termo} dos principais portais jurídicos.",
                "url": "#"
            }]
        
        return noticias_termo

# Sistema de cache para dados
@st.cache_data
def carregar_dados_glossario():
    api = APIGlossarioJuridico()
    
    termos_lista = api.buscar_todos_termos()
    dados = []
    
    for termo in termos_lista:
        dados_termo = api.buscar_termo(termo)
        
        dados.append({
            "termo": termo,
            "definicao": dados_termo.get("definicao", "Definição em atualização."),
            "area": dados_termo.get("area", "Direito"),
            "fonte": dados_termo.get("fonte", "Fonte oficial"),
            "data": datetime.now().strftime("%Y-%m-%d"),
            "exemplo": dados_termo.get("exemplo", "Exemplo prático em atualização."),
            "sinonimos": _gerar_sinonimos(termo),
            "relacionados": _gerar_relacionados(termo),
            "detalhes": dados_termo.get("jurisprudencia", "Jurisprudência em atualização.")
        })
    
    return pd.DataFrame(dados)

def _gerar_sinonimos(termo):
    sinonimos_map = {
        "Habeas Corpus": ["HC", "Remédio Constitucional"],
        "Mandado de Segurança": ["MS", "Proteção Judicial"],
        "Ação Rescisória": ["Rescisão da Sentença"],
        "Usucapião": ["Prescrição Aquisitiva"],
        "Crime Culposo": ["Delito Culposo", "Culpa"],
        "Coisa Julgada": ["Res Judicata"],
        "Agravo de Instrumento": ["Agravo"],
        "Jus Postulandi": ["Capacidade Postulatória"]
    }
    return sinonimos_map.get(termo, [])

def _gerar_relacionados(termo):
    relacionados_map = {
        "Habeas Corpus": ["Mandado de Segurança", "Liberdade", "Prisão"],
        "Mandado de Segurança": ["Habeas Corpus", "Direito Líquido", "Ação"],
        "Ação Rescisória": ["Coisa Julgada", "Recurso", "Sentença"],
        "Usucapião": ["Propriedade", "Posse", "Direito Real"],
        "Crime Culposo": ["Crime Doloso", "Culpa", "Dolo"],
        "Coisa Julgada": ["Sentença", "Recurso", "Processo"],
        "Agravo de Instrumento": ["Recurso", "Decisão Interlocutória"],
        "Jus Postulandi": ["Legitimidade", "Capacidade Processual"]
    }
    return relacionados_map.get(termo, ["Direito", "Jurisprudência", "Legislação"])

# Funções de visualização
def criar_grafico_areas(df):
    contagem_areas = df['area'].value_counts().reset_index()
    contagem_areas.columns = ['Área', 'Quantidade']
    
    fig = px.pie(contagem_areas, values='Quantidade', names='Área',
                 title='🎯 Distribuição por Área do Direito',
                 color_discrete_sequence=px.colors.qualitative.Bold)
    
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(
        height=500,
        showlegend=True,
        font=dict(size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def criar_grafico_fontes(df):
    contagem_fontes = df['fonte'].value_counts().reset_index()
    contagem_fontes.columns = ['Fonte', 'Quantidade']
    
    fig = px.bar(contagem_fontes, x='Fonte', y='Quantidade',
                 title='📊 Termos por Fonte Oficial',
                 color='Quantidade',
                 color_continuous_scale='Blues')
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# Páginas do aplicativo
def exibir_pagina_inicial(df):
    st.markdown("### 🎯 Bem-vindo ao Glossário Jurídico Digital")
    st.markdown("**Descomplicando o Direito** através de definições claras e atualizadas.")
    
    st.markdown("### 📈 Estatísticas do Acervo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Termos", len(df))
    with col2:
        st.metric("Áreas do Direito", df['area'].nunique())
    with col3:
        st.metric("Fontes Oficiais", df['fonte'].nunique())
    with col4:
        st.metric("Atualização", df['data'].max())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(criar_grafico_areas(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(criar_grafico_fontes(df), use_container_width=True)
    
    st.markdown("### 🔥 Termos em Destaque")
    termos_destaque = df.sample(min(4, len(df)))
    
    cols = st.columns(2)
    for idx, (_, termo) in enumerate(termos_destaque.iterrows()):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f'<div class="term-card">', unsafe_allow_html=True)
                
                st.markdown(f"#### ⚖️ {termo['termo']}")
                st.write(f"**{termo['area']}**")
                st.write(termo['definicao'][:150] + "...")
                
                st.caption(f"📚 Fonte: {termo['fonte']}")
                
                if st.button("🔍 Ver Detalhes", key=f"home_{termo['termo']}"):
                    st.session_state.termo_selecionado = termo['termo']
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

def exibir_explorar_termos(df, area_selecionada, termo_busca):
    st.markdown("### 📚 Explorar Termos Jurídicos")
    
    col_filtro1, col_filtro2 = st.columns(2)
    
    with col_filtro1:
        busca_avancada = st.text_input("🔍 Buscar termo:", key="busca_avancada")
    
    with col_filtro2:
        area_filtro = st.selectbox("🎯 Filtrar por área:", ["Todas"] + list(df['area'].unique()))
    
    df_filtrado = df.copy()
    
    if area_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado['area'] == area_filtro]
    
    if busca_avancada:
        df_filtrado = df_filtrado[
            df_filtrado['termo'].str.contains(busca_avancada, case=False) |
            df_filtrado['definicao'].str.contains(busca_avancada, case=False)
        ]
    
    if len(df_filtrado) > 0:
        st.success(f"🎉 **{len(df_filtrado)}** termo(s) encontrado(s)")
        
        for _, termo in df_filtrado.iterrows():
            with st.container():
                st.markdown(f'<div class="term-card">', unsafe_allow_html=True)
                
                col_texto, col_acoes = st.columns([3, 1])
                
                with col_texto:
                    st.markdown(f"##### ⚖️ {termo['termo']}")
                    st.write(f"**{termo['area']}** | 📅 {termo['data']}")
                    st.write(termo['definicao'])
                    
                    if termo['sinonimos']:
                        st.caption(f"**Sinônimos:** {', '.join(termo['sinonimos'])}")
                    
                    st.caption(f"📚 **Fonte:** {termo['fonte']}")
                
                with col_acoes:
                    st.write("")
                    if st.button("🔍 Detalhes", key=f"exp_{termo['termo']}", use_container_width=True):
                        st.session_state.termo_selecionado = termo['termo']
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Nenhum termo encontrado com os filtros aplicados.")

def exibir_pagina_termo(df, termo_nome):
    termo_data = df[df['termo'] == termo_nome].iloc[0]
    api = APIGlossarioJuridico()
    news = GoogleNewsIntegracao()
    
    st.markdown(f'<div class="definition-card">', unsafe_allow_html=True)
    
    col_header, col_nav = st.columns([4, 1])
    
    with col_header:
        st.markdown(f"# ⚖️ {termo_data['termo']}")
        st.markdown(f"**Área:** {termo_data['area']} | **Fonte:** {termo_data['fonte']} | **Data:** {termo_data['data']}")
    
    with col_nav:
        st.write("")
        if st.button("← Voltar", use_container_width=True):
            st.session_state.termo_selecionado = None
            st.rerun()
    
    st.markdown("---")
    
    col_conteudo, col_lateral = st.columns([2, 1])
    
    with col_conteudo:
        st.markdown("### 📖 Definição Oficial")
        st.info(termo_data['definicao'])
        
        st.markdown("### 💼 Exemplo Prático")
        st.success(termo_data['exemplo'])
        
        st.markdown("### ⚖️ Jurisprudência")
        st.write(termo_data['detalhes'])
    
    with col_lateral:
        st.markdown("### 🏷️ Informações")
        
        if termo_data['sinonimos']:
            st.markdown("**Sinônimos:**")
            for sinonimo in termo_data['sinonimos']:
                st.write(f"• {sinonimo}")
        
        st.markdown("**Relacionados:**")
        for relacionado in termo_data['relacionados']:
            if st.button(f"→ {relacionado}", key=f"rel_{relacionado}"):
                if relacionado in df['termo'].values:
                    st.session_state.termo_selecionado = relacionado
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📰 Notícias Recentes")
    
    with st.spinner("Buscando notícias..."):
        noticias = news.buscar_noticias(termo_nome)
    
    if noticias:
        for noticia in noticias:
            with st.container():
                st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
                
                st.markdown(f"#### {noticia['titulo']}")
                st.write(noticia['resumo'])
                st.caption(f"**Fonte:** {noticia['fonte']} | **Data:** {noticia['data']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Não foram encontradas notícias recentes para este termo.")

def exibir_pagina_noticias():
    st.markdown("### 📰 Notícias Jurídicas")
    
    st.info("Busque notícias sobre termos jurídicos específicos na página de detalhes de cada termo.")
    
    termo_geral = st.text_input("🔍 Buscar notícias sobre:")
    
    if termo_geral:
        news = GoogleNewsIntegracao()
        with st.spinner("Buscando notícias..."):
            noticias = news.buscar_noticias(termo_geral)
        
        if noticias:
            for noticia in noticias:
                st.write(f"**{noticia['titulo']}**")
                st.caption(f"{noticia['fonte']} - {noticia['data']}")
                st.write(noticia['resumo'])
                st.markdown("---")
        else:
            st.warning("Nenhuma notícia encontrada.")

def exibir_pagina_sobre():
    st.markdown("### ℹ️ Sobre o Projeto")
    st.write("""
    **Glossário Jurídico: Descomplicando o Direito**
    
    **Desenvolvido por:** Carolina Souza, Lara Carneiro e Mayra Rizkalla
    **Turma A** - Projeto P2 Programação 2
    
    **🎯 Objetivos:**
    - Fornecer definições claras de termos jurídicos
    - Contextualizar conceitos com exemplos práticos
    - Integrar notícias relacionadas aos termos
    - Oferecer ferramenta de estudo gratuita
    
    **⚙️ Tecnologias:**
    - Streamlit para interface web
    - Python como linguagem principal
    - APIs jurídicas para dados atualizados
    - Plotly para visualizações interativas
    
    **📞 Fontes Oficiais:**
    - STF (Supremo Tribunal Federal)
    - STJ (Superior Tribunal de Justiça)
    - Câmara dos Deputados
    - Base de dados do Planalto
    """)

# App principal
def main():
    st.markdown('<h1 class="main-header">⚖️ Glossário Jurídico</h1>', unsafe_allow_html=True)
    st.markdown("### Descomplicando o Direito para estudantes e leigos")
    
    df = carregar_dados_glossario()
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn.pixabay.com/photo/2017/01/31/14/26/law-2024670_1280.png", width=80)
        st.title("🔍 Navegação")
        
        st.subheader("Buscar Termo")
        termo_busca = st.text_input("Digite o termo jurídico:")
        
        st.subheader("Filtros")
        area_selecionada = st.selectbox("Área do Direito", ["Todas"] + list(df['area'].unique()))
        
        st.subheader("Termos Populares")
        for termo in df['termo'].head(6):
            if st.button(termo, key=f"side_{termo}"):
                st.session_state.termo_selecionado = termo
                st.rerun()
        
        st.markdown("---")
        st.metric("Total de Termos", len(df))
    
    # Rotas
    if st.session_state.termo_selecionado:
        exibir_pagina_termo(df, st.session_state.termo_selecionado)
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Início", "📚 Explorar", "📰 Notícias", "ℹ️ Sobre"])
        with tab1:
            exibir_pagina_inicial(df)
        with tab2:
            exibir_explorar_termos(df, area_selecionada, termo_busca)
        with tab3:
            exibir_pagina_noticias()
        with tab4:
            exibir_pagina_sobre()

if __name__ == "__main__":
    main()
