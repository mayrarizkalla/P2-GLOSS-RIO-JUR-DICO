import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração básica
st.set_page_config(
    page_title="Glossário Jurídico",
    page_icon="⚖️",
    layout="wide"
)

# Dados do glossário
termos_juridicos = [
    {"termo": "Habeas Corpus", "definicao": "Remédio constitucional que protege o direito de locomoção.", "area": "Direito Constitucional", "fonte": "STF"},
    {"termo": "Mandado de Segurança", "definicao": "Ação para proteger direito líquido e certo.", "area": "Direito Constitucional", "fonte": "STF"},
    {"termo": "Ação Rescisória", "definicao": "Ação para desconstituir sentença transitada em julgado.", "area": "Direito Processual Civil", "fonte": "STJ"},
    {"termo": "Usucapião", "definicao": "Aquisição da propriedade pela posse prolongada.", "area": "Direito Civil", "fonte": "STJ"},
    {"termo": "Crime Culposo", "definicao": "Conduta com resultado ilícito não desejado.", "area": "Direito Penal", "fonte": "Câmara"},
    {"termo": "Princípio da Isonomia", "definicao": "Igualdade de todos perante a lei.", "area": "Direito Constitucional", "fonte": "Câmara"},
    {"termo": "Coisa Julgada", "definicao": "Qualidade da sentença imutável.", "area": "Direito Processual", "fonte": "STJ"},
    {"termo": "Agravo de Instrumento", "definicao": "Recurso contra decisão interlocutória.", "area": "Direito Processual", "fonte": "STJ"},
    {"termo": "Desconsideração da Personalidade Jurídica", "definicao": "Instrumento para atingir bens de sócios.", "area": "Direito Empresarial", "fonte": "STJ"},
    {"termo": "Recurso Extraordinário", "definicao": "Recurso por ofensa à Constituição.", "area": "Direito Constitucional", "fonte": "STF"},
    {"termo": "Liminar", "definicao": "Decisão judicial provisória.", "area": "Direito Processual", "fonte": "STJ"},
    {"termo": "Prescrição", "definicao": "Perda do direito pelo decurso do tempo.", "area": "Direito Civil", "fonte": "Planalto"},
    {"termo": "Fiança", "definicao": "Garantia pessoal em processo penal.", "area": "Direito Penal", "fonte": "Planalto"},
    {"termo": "Sentença", "definicao": "Decisão que põe fim à fase cognitiva.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Acórdão", "definicao": "Decisão de tribunal colegiado.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Processo", "definicao": "Conjunto de atos para solução de conflito.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Petição Inicial", "definicao": "Primeira manifestação que inicia o processo.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Contestação", "definicao": "Resposta do réu à petição inicial.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Prova", "definicao": "Meio para demonstrar a verdade dos fatos.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Testemunha", "definicao": "Pessoa que depõe sobre fatos relevantes.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Perícia", "definicao": "Prova técnica por profissional habilitado.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Prisão Preventiva", "definicao": "Medida cautelar de privação de liberdade.", "area": "Direito Penal", "fonte": "Planalto"},
    {"termo": "Liberdade Provisória", "definicao": "Concessão de liberdade durante processo.", "area": "Direito Penal", "fonte": "Planalto"},
    {"termo": "Habeas Data", "definicao": "Remédio para conhecimento de informações.", "area": "Direito Constitucional", "fonte": "Câmara"},
    {"termo": "Mandado de Injunção", "definicao": "Remédio para direito não regulamentado.", "area": "Direito Constitucional", "fonte": "Câmara"},
    {"termo": "Ação Popular", "definicao": "Instrumento para anular ato lesivo.", "area": "Direito Administrativo", "fonte": "Câmara"},
    {"termo": "Ação Civil Pública", "definicao": "Instrumento para defesa coletiva.", "area": "Direito Coletivo", "fonte": "Câmara"},
    {"termo": "Recurso Especial", "definicao": "Recurso por ofensa à lei federal.", "area": "Direito Processual", "fonte": "STJ"},
    {"termo": "Embargos de Declaração", "definicao": "Recurso para corrigir decisão.", "area": "Direito Processual", "fonte": "STJ"},
    {"termo": "Súmula Vinculante", "definicao": "Enunciado do STF com efeito vinculante.", "area": "Direito Constitucional", "fonte": "STF"},
    {"termo": "Arguição de Descumprimento de Preceito Fundamental", "definicao": "Ação para proteger preceito fundamental.", "area": "Direito Constitucional", "fonte": "STF"},
    {"termo": "Jus Postulandi", "definicao": "Capacidade de postular em juízo.", "area": "Direito Processual", "fonte": "STJ"},
    {"termo": "Arresto", "definicao": "Medida cautelar de apreensão de bens.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Sequestro", "definicao": "Medida cautelar de deposição judicial.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Busca e Apreensão", "definicao": "Medida para localizar e apreender.", "area": "Direito Processual", "fonte": "Planalto"},
    {"termo": "Interceptação Telefônica", "definicao": "Meio de prova para captar comunicações.", "area": "Direito Penal", "fonte": "Planalto"},
    {"termo": "Prisão Temporária", "definicao": "Prisão por prazo determinado.", "area": "Direito Penal", "fonte": "Planalto"},
    {"termo": "Sursis", "definicao": "Suspensão condicional da pena.", "area": "Direito Penal", "fonte": "Planalto"},
    {"termo": "Transação Penal", "definicao": "Acordo para pena alternativa.", "area": "Direito Penal", "fonte": "Planalto"},
    {"termo": "Suspensão Condicional do Processo", "definicao": "Paralisação temporária do processo.", "area": "Direito Penal", "fonte": "Planalto"}
]

df = pd.DataFrame(termos_juridicos)

# Interface principal
st.title("⚖️ Glossário Jurídico")
st.subheader("Descomplicando o Direito")

# Sidebar
with st.sidebar:
    st.header("🔍 Busca")
    termo_busca = st.text_input("Digite o termo:")
    
    st.header("🎯 Filtros")
    areas = ["Todas"] + sorted(df['area'].unique().tolist())
    area_selecionada = st.selectbox("Área do Direito", areas)
    
    st.header("📊 Estatísticas")
    st.metric("Total de Termos", len(df))

# Conteúdo principal
tab1, tab2, tab3 = st.tabs(["📚 Termos", "📊 Estatísticas", "ℹ️ Sobre"])

with tab1:
    st.header("📚 Termos Jurídicos")
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if area_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['area'] == area_selecionada]
    
    if termo_busca:
        df_filtrado = df_filtrado[df_filtrado['termo'].str.contains(termo_busca, case=False)]
    
    # Exibir resultados
    if len(df_filtrado) > 0:
        st.success(f"Encontrados {len(df_filtrado)} termos")
        
        for _, termo in df_filtrado.iterrows():
            with st.expander(f"**{termo['termo']}** - {termo['area']}"):
                st.write(f"**Definição:** {termo['definicao']}")
                st.write(f"**Fonte:** {termo['fonte']}")
    else:
        st.warning("Nenhum termo encontrado")

with tab2:
    st.header("📊 Estatísticas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Termos", len(df))
    
    with col2:
        st.metric("Áreas do Direito", df['area'].nunique())
    
    with col3:
        st.metric("Fontes", df['fonte'].nunique())
    
    # Gráfico de áreas
    contagem_areas = df['area'].value_counts()
    st.bar_chart(contagem_areas)

with tab3:
    st.header("ℹ️ Sobre o Projeto")
    st.write("""
    **Glossário Jurídico: Descomplicando o Direito**
    
    **Desenvolvido por:** Carolina Souza, Lara Carneiro e Mayra Rizkalla
    **Turma A** - Projeto P2 Programação
    
    **Fontes Oficiais:**
    - STF (Supremo Tribunal Federal)
    - STJ (Superior Tribunal de Justiça) 
    - Câmara dos Deputados
    - Base de dados do Planalto
    
    **Total de termos:** 40 termos jurídicos essenciais
    """)

st.markdown("---")
st.caption("Glossário Jurídico - Descomplicando o Direito © 2024")
