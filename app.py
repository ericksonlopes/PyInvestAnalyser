import io

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

from run import generate_csv
from src.models import RealEstateFunds

st.set_page_config(page_title='PyInvestAnalyser',
                   page_icon='📊',
                   initial_sidebar_state='auto')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('PyInvestAnalyser')

data = st.file_uploader('Escolha o arquivo para analise de dados', type=['csv'])

if data is None:
    st.warning(
        """
        Por favor, escolha um arquivo para analise de dados."):
        """)
    st.stop()

content = data.read().decode('latin-1')
content_lines = content.split('\n')
content_without_first_line = '\n'.join(content_lines[1:])

df = pd.read_csv(io.StringIO(content_without_first_line), sep=';')

df = df[['TIPO DE INVESTIMENTO', 'DESCRIÇÃO', 'VALOR BRUTO', "QUANTIDADE"]]

fiis = df[df['TIPO DE INVESTIMENTO'] == 'FII'].copy()

with st.spinner('Loading...'):
    df_infos = generate_csv(fiis['DESCRIÇÃO'].unique())

df_infos.columns = RealEstateFunds.get_meaning_of_fields().values()

df_infos = df_infos[["Nome", "Cotação", "P/VP", "VAL. PATRIMONIAL P/ COTA", 'SEGMENTO']]

fiis["SEGMENTO"] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["SEGMENTO"])

fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('.', '')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('R$ ', '')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace(',', '.')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].astype(float)

fiis['QUANTIDADE'] = fiis['QUANTIDADE'].str.replace(',0', '')
fiis['QUANTIDADE'] = fiis['QUANTIDADE'].astype(int)

st.dataframe(fiis, use_container_width=True)

st.title('Gráficos Por:')

nome, segmento = st.tabs(['Ativos', 'Segmentos'])

with nome:
    fig1, ax1 = plt.subplots()
    ax1.pie(fiis['VALOR BRUTO'], labels=fiis['DESCRIÇÃO'], autopct='%1.1f%%')
    ax1.axis('equal')
    st.pyplot(fig1)

with segmento:
    segmentos = fiis.groupby('SEGMENTO').sum().reset_index()
    segmentos.sort_values(by=['VALOR BRUTO'], inplace=True, ascending=False)

    fig2, ax2 = plt.subplots()
    ax2.pie(segmentos["VALOR BRUTO"], labels=segmentos["SEGMENTO"], autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)
