import concurrent.futures
import io

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

from config import Logger
from src.models import RealEstateFunds
from src.services import ExtractInfoFromREF


def generate_data(actives):
    result_actives = []

    logger = Logger().logger

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ExtractInfoFromREF().get_info_active, active) for active in actives]

        for future in concurrent.futures.as_completed(futures):

            try:
                active = future.result()

                if isinstance(active, str):
                    active = ExtractInfoFromREF().get_active_keys_indicators(active)

                result_actives.append(active)
            except Exception as e:
                logger.error(f"Error to get information for active {active.name}")
                logger.error(e)

    return pd.DataFrame(result_actives)


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

with st.expander("Visualizar dados brutos"):
    st.dataframe(df)

df = df[['TIPO DE INVESTIMENTO', 'DESCRIÇÃO', 'VALOR BRUTO', "QUANTIDADE"]]

fiis = df[df['TIPO DE INVESTIMENTO'] == 'FII'].copy()

with st.spinner('Loading...'):
    df_infos = generate_data(fiis['DESCRIÇÃO'].unique())

df_infos.columns = RealEstateFunds.get_meaning_of_fields().values()

with st.expander("Visualizar dados brutos"):
    st.dataframe(df_infos)

df_infos = df_infos[["Nome", "Cotação", "P/VP", "VAL. PATRIMONIAL P/ COTA", 'SEGMENTO']]

fiis["SEGMENTO"] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["SEGMENTO"])
fiis["COTAÇÃO"] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["Cotação"])
fiis["P/VP"] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["P/VP"])

fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('.', '')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('R$ ', '')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace(',', '.')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].astype(float)

fiis['QUANTIDADE'] = fiis['QUANTIDADE'].str.replace(',0', '')
fiis['QUANTIDADE'] = fiis['QUANTIDADE'].astype(int)

fiis.drop(columns=['TIPO DE INVESTIMENTO'], inplace=True)

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
