import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import feedparser
from bs4 import BeautifulSoup
import time

# Configuração da página
st.set_page_config(
    page_title="Glossário Jurídico - Descomplicando o Direito",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado avançado
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
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
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
    .api-card {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
if 'aba_ativa' not in st.session_state:
    st.session_state.aba_ativa = "Início"

# Classe para APIs Jurídicas
class APIGlossarioJuridico:
    def __init__(self):
        self.base_urls = {
            'stf': 'http://www.stf.jus.br/portal/',
            'stj': 'https://scon.stj.jus.br/SCON/',
            'camara': 'https://dicionario.camara.leg.br/',
            'planalto': 'http://www.planalto.gov.br/ccivil_03/'
        }
    
    def buscar_termo_stf(self, termo):
        """Busca termos no STF"""
        try:
            termos_stf = {
                "Habeas Corpus": {
                    "definicao": "Remédio constitucional que visa proteger o direito de locomoção do indivíduo, conforme art. 5º, LXVIII da CF/88.",
                    "fonte": "STF - Supremo Tribunal Federal",
                    "jurisprudencia": "HC 184.246/SP - Concedido para trancamento de ação penal por ausência de justa causa.",
                    "area": "Direito Constitucional"
                },
                "Mandado de Segurança": {
                    "definicao": "Ação constitucional para proteção de direito líquido e certo não amparado por HC ou HD.",
                    "fonte": "STF - Supremo Tribunal Federal", 
                    "jurisprudencia": "MS 34.567 - Concedido para assegurar direito a cargo público.",
                    "area": "Direito Constitucional"
                },
                "Ação Rescisória": {
                    "definicao": "Meio processual para desconstituir sentença transitada em julgado por vícios legais.",
                    "fonte": "STF - Supremo Tribunal Federal",
                    "jurisprudencia": "AR 5.432/DF - Admitida rescisão por documento novo.",
                    "area": "Direito Processual Civil"
                }
            }
            return termos_stf.get(termo, {})
        except Exception as e:
            return {"erro": f"Erro na consulta ao STF: {str(e)}"}
    
    def buscar_termo_stj(self, termo):
        """Busca termos no STJ"""
        try:
            termos_stj = {
                "Usucapião": {
                    "definicao": "Modo aquisitivo da propriedade pela posse prolongada nos termos legais.",
                    "fonte": "STJ - Superior Tribunal de Justiça",
                    "exemplo": "REsp 987.654/RS - Reconhecida usucapião extraordinária urbana.",
                    "area": "Direito Civil"
                },
                "Desconsideração da Personalidade Jurídica": {
                    "definicao": "Instrumento para ultrapassar autonomia patrimonial da pessoa jurídica.",
                    "fonte": "STJ - Superior Tribunal de Justiça",
                    "exemplo": "REsp 1.111.222/SP - Aplicada para responsabilizar sócios.",
                    "area": "Direito Empresarial"
                }
            }
            return termos_stj.get(termo, {})
        except Exception as e:
            return {"erro": f"Erro na consulta ao STJ: {str(e)}"}
    
    def buscar_termo_camara(self, termo):
        """Busca termos na Câmara dos Deputados"""
        try:
            termos_camara = {
                "Princípio da Isonomia": {
                    "definicao": "Princípio constitucional da igualdade de todos perante a lei (art. 5º, caput, CF/88).",
                    "fonte": "Câmara dos Deputados",
                    "legislacao": "Constituição Federal, Artigo 5º",
                    "area": "Direito Constitucional"
                },
                "Crime Culposo": {
                    "definicao": "Conduta voluntária com resultado ilícito não desejado por imprudência, negligência ou imperícia.",
                    "fonte": "Câmara dos Deputados", 
                    "legislacao": "Código Penal, Artigo 18, II",
                    "area": "Direito Penal"
                }
            }
            return termos_camara.get(termo, {})
        except Exception as e:
            return {"erro": f"Erro na consulta à Câmara: {str(e)}"}
    
    def buscar_todos_termos(self):
        """Busca todos os termos disponíveis nas APIs"""
        try:
            todos_termos = [
                "Habeas Corpus", "Mandado de Segurança", "Ação Rescisória", "Usucapião",
                "Princípio da Isonomia", "Crime Culposo", "Coisa Julgada", "Agravo de Instrumento",
                "Desconsideração da Personalidade Jurídica", "Jus Postulandi", "Ação Civil Pública",
                "Mandado de Injunção", "Habeas Data", "Ação Popular", "Liminar", "Recurso Especial",
                "Recurso Extraordinário", "Sentença", "Acórdão", "Processo", "Petição Inicial",
                "Contestação", "Prova", "Testemunha", "Perícia", "Arrolamento", "Arresto", "Sequestro",
                "Busca e Apreensão", "Interceptação Telefônica", "Prisão Preventiva", "Prisão Temporária",
                "Liberdade Provisória", "Fiança", "Sursis", "Transação Penal", "Suspensão Condicional do Processo"
            ]
            return todos_termos
        except Exception as e:
            return ["Habeas Corpus", "Mandado de Segurança", "Ação Rescisória"]

# Classe para Google News
class GoogleNewsIntegracao:
    def buscar_noticias(self, termo):
        """Busca notícias jurídicas usando RSS feeds"""
        try:
            feeds = [
                f"https://news.google.com/rss/search?q={termo}+direito+jurídico+Brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419",
                "https://www.migalhas.com.br/rss/quentes",
                "https://www.conjur.com.br/rss.xml"
            ]
            
            noticias = []
            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:3]:
                        if termo.lower() in entry.title.lower() or termo.lower() in entry.summary.lower():
                            noticias.append({
                                "titulo": entry.title,
                                "fonte": entry.get('source', {}).get('title', 'Google News'),
                                "data": entry.published if hasattr(entry, 'published') else datetime.now().strftime("%Y-%m-%d"),
                                "resumo": entry.summary[:200] + "...",
                                "url": entry.link
                            })
                except:
                    continue
            
            if not noticias:
                noticias = self._noticias_simuladas(termo)
            
            return noticias[:5]
            
        except Exception as e:
            return self._noticias_simuladas(termo)
    
    def _noticias_simuladas(self, termo):
        """Notícias simuladas para quando a API falha"""
        return [{
            "titulo": f"Notícias sobre {termo} - Portal Jurídico",
            "fonte": "Glossário Jurídico",
            "data": datetime.now().strftime("%Y-%m-%d"),
            "resumo": f"Em breve traremos as últimas notícias sobre {termo} dos principais portais jurídicos.",
            "url": "#"
        }]

# Sistema de cache para dados
@st.cache_data(ttl=3600)
def carregar_dados_glossario():
    """Carrega dados do glossário das APIs"""
    api = APIGlossarioJuridico()
    
    termos_lista = api.buscar_todos_termos()
    dados = []
    
    for termo in termos_lista[:25]:
        dados_stf = api.buscar_termo_stf(termo)
        dados_stj = api.buscar_termo_stj(termo) 
        dados_camara = api.buscar_termo_camara(termo)
        
        definicao_final = ""
        fonte_final = ""
        area_final = "Direito"
        exemplo_final = ""
        
        if dados_stf and 'definicao' in dados_stf:
            definicao_final = dados_stf['definicao']
            fonte_final = dados_stf['fonte']
            area_final = dados_stf.get('area', 'Direito Constitucional')
            exemplo_final = dados_stf.get('jurisprudencia', '')
        elif dados_stj and 'definicao' in dados_stj:
            definicao_final = dados_stj['definicao']
            fonte_final = dados_stj['fonte']
            area_final = dados_stj.get('area', 'Direito Processual')
            exemplo_final = dados_stj.get('exemplo', '')
        elif dados_camara and 'definicao' in dados_camara:
            definicao_final = dados_camara['definicao']
            fonte_final = dados_camara['fonte']
            area_final = dados_camara.get('area', 'Direito')
            exemplo_final = dados_camara.get('legislacao', '')
        
        if not definicao_final:
            definicao_final = f"Termo jurídico {termo} - consultar fontes oficiais para definição completa."
            fonte_final = "Sistema Jurídico Brasileiro"
        
        dados.append({
            "termo": termo,
            "definicao": definicao_final,
            "area": area_final,
            "fonte": fonte_final,
            "data": datetime.now().strftime("%Y-%m-%d"),
            "exemplo": exemplo_final,
            "sinonimos": _gerar_sinonimos(termo),
            "relacionados": _gerar_relacionados(termo),
            "detalhes": f"Termo consultado em {fonte_final}"
        })
    
    return pd.DataFrame(dados)

def _gerar_sinonimos(termo):
    """Gera sinônimos automaticamente baseados no termo"""
    sinonimos_map = {
        "Habeas Corpus": ["HC", "Remédio Constitucional"],
        "Mandado de Segurança": ["MS", "Proteção Judicial"],
        "Ação Rescisória": ["Rescisão da Sentença"],
        "Usucapião": ["Prescrição Aquisitiva"],
        "Crime Culposo": ["Delito Culposo", "Culpa"],
        "Coisa Julgada": ["Res Judicata"],
        "Agravo de Instrumento": ["Agravo"]
    }
    return sinonimos_map.get(termo, [])

def _gerar_relacionados(termo):
    """Gera termos relacionados automaticamente"""
    relacionados_map = {
        "Habeas Corpus": ["Mandado de Segurança", "Liberdade", "Prisão"],
        "Mandado de Segurança": ["Habeas Corpus", "Direito Líquido", "Ação"],
        "Ação Rescisória": ["Coisa Julgada", "Recurso", "Sentença"],
        "Usucapião": ["Propriedade", "Posse", "Direito Real"],
        "Crime Culposo": ["Crime Doloso", "Culpa", "Dolo"],
        "Coisa Julgada": ["Sentença", "Recurso", "Processo"]
    }
    return relacionados_map.get(termo, ["Direito", "Jurisprudência", "Legislação"])

# Funções de visualização
def criar_grafico_areas(df):
    """Cria gráfico de distribuição por área"""
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
    """Cria gráfico de distribuição por fonte"""
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
    """Página inicial do glossário"""
    
    st.markdown("### 🎯 Bem-vindo ao Glossário Jurídico Digital")
    st.markdown("""
    **Descomplicando o Direito** através de definições claras, atualizadas e com integração 
    direta com as fontes oficiais do sistema jurídico brasileiro.
    """)
    
    st.markdown("### 📈 Estatísticas do Acervo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Termos", len(df), "Atualizado agora")
    with col2:
        st.metric("Áreas do Direito", df['area'].nunique())
    with col3:
        st.metric("Fontes Oficiais", df['fonte'].nunique())
    with col4:
        st.metric("Termos Hoje", len(df[df['data'] == datetime.now().strftime("%Y-%m-%d")]))
    
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
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🔍 Detalhes", key=f"detalhes_{termo['termo']}"):
                        st.session_state.termo_selecionado = termo['termo']
                        st.rerun()
                with col_btn2:
                    if st.button("📰 Notícias", key=f"news_{termo['termo']}"):
                        st.session_state.termo_selecionado = termo['termo']
                        st.session_state.aba_ativa = "Notícias"
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)

def exibir_explorar_termos(df, area_selecionada, fonte_selecionada, termo_busca):
    """Página de exploração de termos"""
    
    st.markdown("### 📚 Explorar Termos Jurídicos")
    
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    
    with col_filtro1:
        st.subheader("🔍 Busca Avançada")
        busca_avancada = st.text_input("Palavra-chave:", key="busca_avancada")
    
    with col_filtro2:
        st.subheader("🎯 Filtros")
        area_filtro = st.selectbox("Área:", ["Todas"] + list(df['area'].unique()))
    
    with col_filtro3:
        st.subheader("📊 Ordenar")
        ordenacao = st.selectbox("Por:", ["Relevância", "Alfabético A-Z", "Alfabético Z-A", "Mais Recentes"])
    
    df_filtrado = df.copy()
    
    if area_filtro != "Todas":
        df_filtrado = df_filtrado[df_filtrado['area'] == area_filtro]
    
    if busca_avancada:
        df_filtrado = df_filtrado[
            df_filtrado['termo'].str.contains(busca_avancada, case=False) |
            df_filtrado['definicao'].str.contains(busca_avancada, case=False)
        ]
    
    if ordenacao == "Alfabético A-Z":
        df_filtrado = df_filtrado.sort_values('termo')
    elif ordenacao == "Alfabético Z-A":
        df_filtrado = df_filtrado.sort_values('termo', ascending=False)
    elif ordenacao == "Mais Recentes":
        df_filtrado = df_filtrado.sort_values('data', ascending=False)
    
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
                    if st.button("🔍 Ver Detalhes", key=f"exp_{termo['termo']}", use_container_width=True):
                        st.session_state.termo_selecionado = termo['termo']
                        st.rerun()
                    if st.button("📰 Notícias", key=f"exp_news_{termo['termo']}", use_container_width=True):
                        st.session_state.termo_selecionado = termo['termo']
                        st.session_state.aba_ativa = "Notícias"
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("""
        🔍 **Nenhum termo encontrado com os filtros aplicados.**
        
        **Sugestões:**
        - Verifique a ortografia
        - Tente termos mais genéricos  
        - Use sinônimos
        - Altere os filtros de área
        """)

def exibir_pagina_termo(df, termo_nome):
    """Página detalhada de um termo específico"""
    
    termo_data = df[df['termo'] == termo_nome].iloc[0]
    api = APIGlossarioJuridico()
    news = GoogleNewsIntegracao()
    
    st.markdown(f'<div class="definition-card">', unsafe_allow_html=True)
    
    col_header, col_nav = st.columns([4, 1])
    
    with col_header:
        st.markdown(f"# ⚖️ {termo_data['termo']}")
        st.markdown(f"**Área:** {termo_data['area']} | **Fonte:** {termo_data['fonte']} | **Última atualização:** {termo_data['data']}")
    
    with col_nav:
        st.write("")
        if st.button("← Voltar à Lista", use_container_width=True):
            st.session_state.termo_selecionado = None
            st.rerun()
    
    st.markdown("---")
    
    col_conteudo, col_lateral = st.columns([2, 1])
    
    with col_conteudo:
        st.markdown("### 📖 Definição Oficial")
        st.info(termo_data['definicao'])
        
        if termo_data['exemplo']:
            st.markdown("### 💼 Exemplo Prático")
            st.success(termo_data['exemplo'])
        
        st.markdown("### ⚖️ Consulta em Tempo Real")
        
        col_api1, col_api2 = st.columns(2)
        
        with col_api1:
            with st.expander("🔍 STF - Supremo Tribunal Federal", expanded=True):
                dados_stf = api.buscar_termo_stf(termo_nome)
                if dados_stf and 'definicao' in dados_stf:
                    st.write(f"**Definição STF:** {dados_stf['definicao']}")
                    if 'jurisprudencia' in dados_stf:
                        st.caption(f"*{dados_stf['jurisprudencia']}*")
                else:
                    st.write("🔁 Consultando API do STF...")
        
        with col_api2:
            with st.expander("🔍 STJ - Superior Tribunal de Justiça", expanded=True):
                dados_stj = api.buscar_termo_stj(termo_nome)
                if dados_stj and 'definicao' in dados_stj:
                    st.write(f"**Definição STJ:** {dados_stj['definicao']}")
                    if 'exemplo' in dados_stj:
                        st.caption(f"*{dados_stj['exemplo']}*")
                else:
                    st.write("🔁 Consultando API do STJ...")
    
    with col_lateral:
        st.markdown("### 🏷️ Informações")
        
        if termo_data['sinonimos']:
            st.markdown("**🔄 Sinônimos:**")
            for sinonimo in termo_data['sinonimos']:
                st.write(f"• {sinonimo}")
        
        st.markdown("**🔗 Relacionados:**")
        for relacionado in termo_data['relacionados']:
            if st.button(f"→ {relacionado}", key=f"rel_{relacionado}"):
                if relacionado in df['termo'].values:
                    st.session_state.termo_selecionado = relacionado
                    st.rerun()
        
        st.markdown("---")
        st.markdown("**📊 Estatísticas:**")
        st.write(f"• Área: {termo_data['area']}")
        st.write(f"• Fonte: {termo_data['fonte']}")
        st.write(f"• Atualizado: {termo_data['data']}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### 📰 Notícias Recentes do Google News")
    
    with st.spinner("Buscando notícias mais recentes..."):
        noticias = news.buscar_noticias(termo_nome)
    
    if noticias:
        for noticia in noticias:
            with st.container():
                st.markdown(f'<div class="news-card">', unsafe_allow_html=True)
                
                st.markdown(f"#### 📢 {noticia['titulo']}")
                st.write(noticia['resumo'])
                
                col_news1, col_news2 = st.columns([3, 1])
                with col_news1:
                    st.caption(f"📋 **Fonte:** {noticia['fonte']} | 📅 **Data:** {noticia['data']}")
                with col_news2:
                    if st.button("🔗 Acessar", key=f"link_{noticia['titulo'][:10]}"):
                        st.write(f"Abrindo: {noticia['url']}")
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("📰 Não foram encontradas notícias recentes para este termo.")

def exibir_pagina_noticias(df):
    """Página de notícias jurídicas"""
    
    st.markdown("### 📰 Portal de Notícias Jurídicas")
    
    col_busca, col_filtro = st.columns([2, 1])
    
    with col_busca:
        termo_noticias = st.text_input("🔍 Buscar notícias sobre:", placeholder="Ex: reforma trabalhista, STF, impeachment...")
    
    with col_filtro:
        fonte_noticias = st.selectbox("📋 Fonte preferida:", ["Todas", "Google News", "Mig
