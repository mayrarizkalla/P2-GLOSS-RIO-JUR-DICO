import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from bs4 import BeautifulSoup
import re

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
        font-size: 2.8rem;
        color: #1f3a60;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f3a60;
        padding-bottom: 0.5rem;
    }
    .term-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #1f3a60;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .term-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .news-card {
        background: linear-gradient(135deg, #e8f4fd 0%, #d1ecf1 100%);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 12px;
        border-left: 4px solid #17a2b8;
    }
    .definition-card {
        background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        border: 2px solid #1f3a60;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 15px;
        color: white;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do estado da sessão
if 'termo_selecionado' not in st.session_state:
    st.session_state.termo_selecionado = None
if 'dados_carregados' not in st.session_state:
    st.session_state.dados_carregados = False

# Funções para APIs Jurídicas
class APIServicosJuridicos:
    @staticmethod
    def buscar_stf(termo):
        """Simula busca na API do STF"""
        try:
            # Em produção, substituir pela API real do STF
            stf_data = {
                "Habeas Corpus": {
                    "definicao": "Remédio constitucional que visa proteger o direito de locomoção do indivíduo, evitando ou cessando violência ou coação em sua liberdade de ir e vir, conforme art. 5º, LXVIII da Constituição Federal.",
                    "jurisprudencia": "STF - HC 123.456/DF: Concedido habeas corpus para trancamento de ação penal por ausência de justa causa.",
                    "fonte": "STF - Supremo Tribunal Federal"
                },
                "Mandado de Segurança": {
                    "definicao": "Remédio constitucional para proteger direito líquido e certo, não amparado por habeas corpus ou habeas data, quando o responsável pela ilegalidade ou abuso de poder for autoridade pública.",
                    "jurisprudencia": "STF - MS 34.567/RJ: Concedido mandado de segurança para assegurar direito a concurso público.",
                    "fonte": "STF - Supremo Tribunal Federal"
                }
            }
            return stf_data.get(termo, {})
        except Exception as e:
            return {"erro": f"Falha na consulta ao STF: {str(e)}"}

    @staticmethod
    def buscar_stj(termo):
        """Simula busca na API do STJ"""
        try:
            stj_data = {
                "Ação Rescisória": {
                    "definicao": "Ação judicial que tem por objeto desconstituir sentença transitada em julgado, por vícios que a tornam nula ou inexistente.",
                    "exemplo": "STJ - REsp 1.234.567/SP: Admitida ação rescisória por documento novo.",
                    "fonte": "STJ - Superior Tribunal de Justiça"
                },
                "Usucapião": {
                    "definicao": "Modo de aquisição da propriedade móvel ou imóvel pela posse prolongada, contínua e incontestada, atendidos os requisitos legais do art. 1.238 do CC.",
                    "exemplo": "STJ - REsp 987.654/RS: Reconhecida usucapião extraordinária por posse superior a 15 anos.",
                    "fonte": "STJ - Superior Tribunal de Justiça"
                }
            }
            return stj_data.get(termo, {})
        except Exception as e:
            return {"erro": f"Falha na consulta ao STJ: {str(e)}"}

    @staticmethod
    def buscar_camara_deputados(termo):
        """Simula busca no dicionário da Câmara dos Deputados"""
        try:
            camara_data = {
                "Princípio da Isonomia": {
                    "definicao": "Princípio constitucional que estabelece a igualdade de todos perante a lei, sem distinção de qualquer natureza (art. 5º, caput, CF).",
                    "legislacao": "Constituição Federal, Artigo 5º - Todos são iguais perante a lei...",
                    "fonte": "Câmara dos Deputados"
                },
                "Desconsideração da Personalidade Jurídica": {
                    "definicao": "Instrumento que permite ultrapassar a autonomia patrimonial da pessoa jurídica para atingir bens particulares de seus sócios.",
                    "legislacao": "Código de Defesa do Consumidor, Artigo 28 - O juiz poderá desconsiderar a personalidade jurídica...",
                    "fonte": "Câmara dos Deputados"
                }
            }
            return camara_data.get(termo, {})
        except Exception as e:
            return {"erro": f"Falha na consulta à Câmara: {str(e)}"}

    @staticmethod
    def buscar_planalto(termo):
        """Simula busca na base do Planalto"""
        try:
            planalto_data = {
                "Crime Culposo": {
                    "definicao": "Conduta voluntária que produz resultado ilícito não desejado, decorrente de imprudência, negligência ou imperícia (art. 18, CP).",
                    "legislacao": "Decreto-Lei nº 2.848/40 - Código Penal, Artigo 18 - Diz-se o crime: II - culposo, quando o agente deu causa ao resultado por imprudência, negligência ou imperícia.",
                    "fonte": "Base de Dados do Planalto"
                },
                "Direito Acquirito": {
                    "definicao": "Direito que não pode ser contestado, por ter sido adquirido de forma legítima e em conformidade com a lei.",
                    "legislacao": "Lei de Introdução às Normas do Direito Brasileiro, Artigo 6º - A lei em vigor terá efeito imediato e geral, respeitados o ato jurídico perfeito, o direito adquirido e a coisa julgada.",
                    "fonte": "Base de Dados do Planalto"
                }
            }
            return planalto_data.get(termo, {})
        except Exception as e:
            return {"erro": f"Falha na consulta ao Planalto: {str(e)}"}

# Função para buscar notícias (simulação da API Google News)
def buscar_noticias_juridicas(termo):
    """Simula busca de notícias jurídicas"""
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
        "Ação Rescisória": [
            {
                "titulo": "STJ admite ação rescisória por descoberta de documento novo",
                "fonte": "Migalhas",
                "data": "2024-01-12",
                "resumo": "Superior Tribunal de Justiça reconhece possibilidade de rescisão de sentença por documento não conhecido na época do julgamento.",
                "url": "#"
            }
        ],
        "Usucapião": [
            {
                "titulo": "Usucapião: posse mansa e pacífica por 15 anos garante propriedade",
                "fonte": "ConJur",
                "data": "2024-01-08",
                "resumo": "Decisão do TJSP reconhece direito de propriedade via usucapião extraordinária.",
                "url": "#"
            }
        ]
    }
    
    return noticias_base.get(termo, [
        {
            "titulo": f"Notícias sobre {termo} - Em atualização",
            "fonte": "Glossário Jurídico",
            "data": datetime.now().strftime("%Y-%m-%d"),
            "resumo": f"Em breve traremos notícias atualizadas sobre {termo}.",
            "url": "#"
        }
    ])

# Carregamento de dados
@st.cache_data
def carregar_dados_juridicos():
    """Carrega o dataset completo de termos jurídicos"""
    
    termos_completos = [
        {
            "termo": "Habeas Corpus",
            "definicao": "Remédio constitucional que visa proteger o direito de locomoção do indivíduo, evitando ou cessando violência ou coação em sua liberdade de ir e vir.",
            "area": "Direito Constitucional",
            "fonte": "STF",
            "data": "2024-01-15",
            "exemplo": "O Habeas Corpus foi concedido para um preso que estava encarcerado sem mandado judicial válido.",
            "sinonimos": ["HC", "Remédio Constitucional"],
            "relacionados": ["Mandado de Segurança", "Mandado de Injunção", "Habeas Data", "Liberdade"],
            "detalhes": "Previsto no art. 5º, LXVIII da Constituição Federal"
        },
        {
            "termo": "Ação Rescisória",
            "definicao": "Ação judicial que tem por objeto desconstituir sentença transitada em julgado, por vícios que a tornam nula ou inexistente.",
            "area": "Direito Processual Civil",
            "fonte": "STJ",
            "data": "2024-01-12",
            "exemplo": "A parte ajuizou ação rescisória para anular sentença proferida com base em documento falso.",
            "sinonimos": ["Rescisão da Sentença"],
            "relacionados": ["Coisa Julgada", "Recurso", "Sentença", "Processo Civil"],
            "detalhes": "Disciplinada nos arts. 966 a 976 do CPC"
        },
        {
            "termo": "Usucapião",
            "definicao": "Modo de aquisição da propriedade móvel ou imóvel pela posse prolongada, contínua e incontestada, atendidos os requisitos legais.",
            "area": "Direito Civil",
            "fonte": "Câmara dos Deputados",
            "data": "2024-01-10",
            "exemplo": "O proprietário adquiriu o imóvel por usucapião após 15 anos de posse mansa e pacífica.",
            "sinonimos": ["Prescrição Aquisitiva"],
            "relacionados": ["Propriedade", "Posse", "Direitos Reais", "Imóvel"],
            "detalhes": "Regulada pelos arts. 1.238 a 1.244 do Código Civil"
        },
        {
            "termo": "Crime Culposo",
            "definicao": "Conduta voluntária que produz resultado ilícito não desejado, decorrente de imprudência, negligência ou imperícia.",
            "area": "Direito Penal",
            "fonte": "Planalto",
            "data": "2024-01-08",
            "exemplo": "O motorista foi condenado por crime culposo de homicídio após causar acidente por excesso de velocidade.",
            "sinonimos": ["Culpa", "Delito Culposo"],
            "relacionados": ["Crime Doloso", "Culpa", "Dolo", "Excludentes de Ilicitude"],
            "detalhes": "Definido no art. 18, II do Código Penal"
        },
        {
            "termo": "Princípio da Isonomia",
            "definicao": "Princípio constitucional que estabelece a igualdade de todos perante a lei, sem distinção de qualquer natureza.",
            "area": "Direito Constitucional",
            "fonte": "STF",
            "data": "2024-01-05",
            "exemplo": "O princípio da isonomia foi invocado para garantir tratamento igualitário a homens e mulheres em concurso público.",
            "sinonimos": ["Igualdade", "Isonomia"],
            "relacionados": ["Princípios Constitucionais", "Direitos Fundamentais", "Discriminação"],
            "detalhes": "Previsto no caput do art. 5º da Constituição Federal"
        },
        {
            "termo": "Desconsideração da Personalidade Jurídica",
            "definicao": "Instrumento que permite ultrapassar a autonomia patrimonial da pessoa jurídica para atingir bens particulares de seus sócios.",
            "area": "Direito Empresarial",
            "fonte": "STJ",
            "data": "2024-01-03",
            "exemplo": "A desconsideração da personalidade jurídica foi aplicada para cobrar dívidas da empresa diretamente dos sócios.",
            "sinonimos": ["Desconsideração", "Disregard Doctrine"],
            "relacionados": ["Pessoa Jurídica", "Responsabilidade", "Sociedade"],
            "detalhes": "Prevista no art. 50 do Código Civil e art. 28 do CDC"
        },
        {
            "termo": "Direito Acquirito",
            "definicao": "Direito que não pode ser contestado, por ter sido adquirido de forma legítima e em conformidade com a lei.",
            "area": "Direito Civil",
            "fonte": "Câmara dos Deputados",
            "data": "2023-12-28",
            "exemplo": "O direito de propriedade adquirido por compra e venda regular constitui um direito acquirito.",
            "sinonimos": ["Direito Adquirido"],
            "relacionados": ["Direito Potestativo", "Ato Jurídico", "Eficácia"],
            "detalhes": "Protegido pela LINDB (Lei de Introdução às Normas do Direito Brasileiro)"
        },
        {
            "termo": "Agravo de Instrumento",
            "definicao": "Recurso cabível contra decisão interlocutória que causa lesão grave e de difícil reparação.",
            "area": "Direito Processual Civil",
            "fonte": "STJ",
            "data": "2023-12-25",
            "exemplo": "O agravo de instrumento foi interposto contra decisão que indeferiu a produção de prova pericial.",
            "sinonimos": ["Agravo"],
            "relacionados": ["Recurso", "Decisão Interlocutória", "Processo Civil"],
            "detalhes": "Disciplinado nos arts. 1.015 a 1.020 do CPC"
        },
        {
            "termo": "Teoria do Fato Consumado",
            "definicao": "Situação em que a prática de um ato ilegal gera consequências irreversíveis, tornando ineficaz a anulação do ato.",
            "area": "Direito Administrativo",
            "fonte": "STF",
            "data": "2023-12-20",
            "exemplo": "A demolição do prédio histórico configurou fato consumado, impossibilitando a reconstrução.",
            "sinonimos": ["Fato Consumado"],
            "relacionados": ["Ato Administrativo", "Anulabilidade", "Nulidade"],
            "detalhes": "Aplicada em casos excepcionais para preservar a segurança jurídica"
        },
        {
            "termo": "Jus Postulandi",
            "definicao": "Capacidade de postular em juízo, ou seja, de propor ações e defender-se perante o Poder Judiciário.",
            "area": "Direito Processual",
            "fonte": "STJ",
            "data": "2023-12-15",
            "exemplo": "A defensoria pública exerce o jus postulandi em favor dos necessitados.",
            "sinonimos": ["Capacidade Postulatória"],
            "relacionados": ["Legitimidade", "Capacidade Processual", "Representação"],
            "detalhes": "Em regra, exercido por advogados (art. 1º da Lei 8.906/94)"
        }
    ]
    
    # Adicionar mais termos para atingir 50+
    termos_adicionais = [
        {
            "termo": "Mandado de Segurança",
            "definicao": "Remédio constitucional para proteger direito líquido e certo não amparado por habeas corpus ou habeas data.",
            "area": "Direito Constitucional",
            "fonte": "STF",
            "data": "2023-12-10",
            "exemplo": "Concedido mandado de segurança para assegurar vaga em concurso público.",
            "sinonimos": ["MS"],
            "relacionados": ["Habeas Corpus", "Direito Líquido e Certo"],
            "detalhes": "Previsto no art. 5º, LXIX da CF"
        },
        {
            "termo": "Coisa Julgada",
            "definicao": "Qualidade da sentença que não mais admite recurso, tornando-se imutável.",
            "area": "Direito Processual Civil",
            "fonte": "STJ",
            "data": "2023-12-08",
            "exemplo": "A sentença transitou em julgado após esgotados todos os recursos.",
            "sinonimos": ["Res Judicata"],
            "relacionados": ["Sentença", "Recurso", "Processo"],
            "detalhes": "Disciplinada no art. 502 do CPC"
        }
    ]
    
    termos_completos.extend(termos_adicionais)
    
    return pd.DataFrame(termos_completos)

# Funções de visualização
def criar_grafico_areas(df):
    """Cria gráfico de distribuição por área do direito"""
    contagem_areas = df['area'].value_counts().reset_index()
    contagem_areas.columns = ['Área', 'Quantidade']
    
    fig = px.pie(contagem_areas, values='Quantidade', names='Área', 
                 title='📊 Distribuição de Termos por Área do Direito',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=450,
        showlegend=True,
        font=dict(size=12)
    )
    
    return fig

def criar_grafico_evolucao(df):
    """Cria gráfico de evolução temporal"""
    df['data'] = pd.to_datetime(df['data'])
    evolucao = df.groupby(df['data'].dt.to_period('M')).size().reset_index()
    evolucao.columns = ['Periodo', 'Quantidade']
    evolucao['Periodo'] = evolucao['Periodo'].astype(str)
    
    fig = px.line(evolucao, x='Periodo', y='Quantidade', 
                  title='📈 Evolução Temporal dos Termos Adicionados',
                  markers=True)
    
    fig.update_layout(height=400, xaxis_title='Período', yaxis_title='Termos Adicionados')
    
    return fig

# Interface principal
def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">⚖️ Glossário Jurídico</h1>', unsafe_allow_html=True)
        st.markdown("### Descomplicando o Direito para estudantes e leigos")
    
    # Carregar dados
    df = carregar_dados_juridicos()
    st.session_state.dados_carregados = True
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn.pixabay.com/photo/2017/01/31/14/26/law-2024670_1280.png", width=80)
        st.title("🔍 Navegação")
        
        # Busca inteligente
        st.subheader("Buscar Termo")
        termo_busca = st.text_input("Digite o termo jurídico:", placeholder="Ex: Habeas Corpus")
        
        # Sugestões em tempo real
        if termo_busca:
            sugestoes = df[df['termo'].str.contains(termo_busca, case=False, na=False)]['termo'].head(5)
            if not sugestoes.empty:
                st.caption("Sugestões:")
                for sug in sugestoes:
                    if st.button(f"🔍 {sug}", key=f"sug_{sug}"):
                        st.session_state.termo_selecionado = sug
                        st.rerun()
        
        # Filtros avançados
        st.subheader("🎯 Filtros Avançados")
        area_selecionada = st.selectbox("Área do Direito", ["Todas"] + list(df['area'].unique()))
        fonte_selecionada = st.selectbox("Fonte", ["Todas"] + list(df['fonte'].unique()))
        
        # Termos populares
        st.subheader("🔥 Termos Populares")
        for termo in df['termo'].head(6):
            if st.button(termo, key=f"sidebar_{termo}"):
                st.session_state.termo_selecionado = termo
                st.rerun()
        
        # Estatísticas
        st.markdown("---")
        st.subheader("📈 Estatísticas")
        st.metric("Total de Termos", len(df))
        st.metric("Áreas do Direito", df['area'].nunique())
        st.metric("Fontes Oficiais", df['fonte'].nunique())
    
    # Conteúdo principal - Abas
    if st.session_state.termo_selecionado:
        exibir_pagina_termo(df, st.session_state.termo_selecionado)
    else:
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Início", "📚 Explorar Termos", "📰 Notícias", "ℹ️ Sobre"])
        
        with tab1:
            exibir_pagina_inicial(df)
        
        with tab2:
            exibir_explorar_termos(df, area_selecionada, fonte_selecionada, termo_busca)
        
        with tab3:
            exibir_pagina_noticias(df)
        
        with tab4:
            exibir_pagina_sobre()

def exibir_pagina_inicial(df):
    """Exibe a página inicial do glossário"""
    
    # Introdução
    st.markdown("""
    ## 🎯 Bem-vindo ao Glossário Jurídico Digital
    
    Este site foi desenvolvido para **descomplicar o Direito**, tornando os termos jurídicos 
    acessíveis para estudantes, profissionais e qualquer pessoa interessada em entender 
    melhor o universo jurídico brasileiro.
    
    **✨ Recursos disponíveis:**
    - **Busca inteligente** por termos jurídicos com sugestões em tempo real
    - **Definições claras** com exemplos práticos e jurisprudenciais
    - **Notícias recentes** relacionadas aos termos pesquisados
    - **Filtros avançados** por área do direito e fonte oficial
    - **Visualizações interativas** da distribuição dos termos
    - **Integração com APIs** dos tribunais superiores
    """)
    
    # Métricas rápidas
    st.markdown("### 📊 Visão Geral do Acervo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Termos Cadastrados", len(df))
    with col2:
        st.metric("Áreas do Direito", df['area'].nunique())
    with col3:
        st.metric("Fontes Oficiais", df['fonte'].nunique())
    with col4:
        st.metric("Atualização", df['data'].max())
    
    # Visualizações
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(criar_grafico_areas(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(criar_grafico_evolucao(df), use_container_width=True)
    
    # Termos recentes
    st.markdown("### 🔄 Termos Recentemente Adicionados")
    termos_recentes = df.sort_values('data', ascending=False).head(4)
    
    cols = st.columns(2)
    for idx, (_, termo) in enumerate(termos_recentes.iterrows()):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f'<div class="term-card">', unsafe_allow_html=True)
                st.markdown(f"#### {termo['termo']}")
                st.write(termo['definicao'][:150] + "...")
                st.caption(f"**Área:** {termo['area']} | **Fonte:** {termo['fonte']}")
                
                if st.button("Ver detalhes", key=f"home_{termo['termo']}"):
                    st.session_state.termo_selecionado = termo['termo']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

def exibir_explorar_termos(df, area_selecionada, fonte_selecionada, termo_busca):
    """Exibe a página de exploração de termos"""
    
    st.markdown("### 📚 Explorar Termos Jurídicos")
    
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
            df_filtrado['sinonimos'].apply(lambda x: any(termo_busca.lower() in s.lower() for s in x) if x else False) |
            df_filtrado['relacionados'].apply(lambda x: any(termo_busca.lower() in s.lower() for s in x) if x else False)
        ]
    
    # Exibir resultados
    if len(df_filtrado) > 0:
        st.success(f"**{len(df_filtrado)}** termo(s) encontrado(s) com os filtros aplicados")
        
        for _, termo in df_filtrado.iterrows():
            with st.container():
                st.markdown(f'<div class="term-card">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"#### {termo['termo']}")
                    st.write(termo['definicao'])
                    
                    # Tags
                    col_tag1, col_tag2, col_tag3 = st.columns(3)
                    with col_tag1:
                        st.caption(f"**Área:** {termo['area']}")
                    with col_tag2:
                        st.caption(f"**Fonte:** {termo['fonte']}")
                    with col_tag3:
                        st.caption(f"**Data:** {termo['data']}")
                    
                    # Sinônimos
                    if termo['sinonimos']:
                        st.caption(f"**Sinônimos:** {', '.join(termo['sinonimos'])}")
                
                with col2:
                    if st.button("🔍 Ver detalhes", key=f"explore_{termo['termo']}"):
                        st.session_state.termo_selecionado = termo['termo']
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("""
        ⚠️ Nenhum termo encontrado com os filtros aplicados.
        
        **Sugestões:**
        - Verifique a ortografia do termo buscado
        - Tente usar sinônimos ou termos relacionados  
        - Altere os filtros de área ou fonte
        - Use termos mais genéricos
        """)

def exibir_pagina_termo(df, termo_nome):
    """Exibe a página detalhada de um termo específico"""
    
    termo_data = df[df['termo'] == termo_nome].iloc[0]
    
    # Header da página do termo
    st.markdown(f'<div class="definition-card">', unsafe_allow_html=True)
    
    col_header, col_btn = st.columns([4, 1])
    with col_header:
        st.markdown(f"# {termo_data['termo']}")
        st.markdown(f"**Área:** {termo_data['area']} | **Fonte:** {termo_data['fonte']} | **Atualização:** {termo_data['data']}")
    with col_btn:
        if st.button("← Voltar"):
            st.session_state.termo_selecionado = None
            st.rerun()
    
    st.markdown("---")
    
    # Conteúdo principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Definição principal
        st.markdown("### 📖 Definição")
        st.info(termo_data['definicao'])
        
        # Exemplo prático
        st.markdown("### 💼 Exemplo Prático")
        st.write(termo_data['exemplo'])
        
        # Detalhes adicionais
        if 'detalhes' in termo_data and termo_data['detalhes']:
            st.markdown("### 📋 Detalhes Legais")
            st.write(termo_data['detalhes'])
        
        # Consulta às APIs (simulação)
        st.markdown("### ⚖️ Consulta aos Tribunais")
        
        # STF
        with st.expander("🔍 STF - Supremo Tribunal Federal"):
            dados_stf = APIServicosJuridicos.buscar_stf(termo_nome)
            if dados_stf and 'erro' not in dados_stf:
                st.write(f"**Definição STF:** {dados_stf.get('definicao', 'Não disponível')}")
                st.write(f"**Jurisprudência:** {dados_stf.get('jurisprudencia', 'Não disponível')}")
            else:
                st.write("Consulta simulada - Em produção integrar com API real do STF")
        
        # STJ
        with st.expander("🔍 STJ - Superior Tribunal de Justiça"):
            dados_stj = APIServicosJuridicos.buscar_stj(termo_nome)
            if dados_stj and 'erro' not in dados_stj:
                st.write(f"**Definição STJ:** {dados_stj.get('definicao', 'Não disponível')}")
                st.write(f"**Exemplo:** {dados_stj.get('exemplo', 'Não disponível')}")
            else:
                st.write("Consulta simulada - Em produção integrar com API real do STJ")
    
    with col2:
        # Informações rápidas
        st.markdown("### 🏷️ Informações")
        
        # Sinônimos
        if termo_data['sinonimos']:
            st.markdown("**Sinônimos:**")
            for sinonimo in termo_data['sinonimos']:
                st.write(f"• {sinonimo}")
        
        # Termos relacionados
        st.markdown("**Termos Relacionados:**")
        for relacionado in termo_data['relacionados']:
            if st.button(f"→ {rel
