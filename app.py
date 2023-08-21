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


st.set_page_config(page_title='PyInvestAnalyser', page_icon='📊', layout='wide')

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

# with st.expander("Visualizar dados brutos"):
#     st.dataframe(df)

df = df[['TIPO DE INVESTIMENTO', 'DESCRIÇÃO', 'VALOR BRUTO', "QUANTIDADE"]]

fiis = df[df['TIPO DE INVESTIMENTO'] == 'FII'].copy()

with st.spinner('Loading...'):
    df_infos = generate_data(fiis['DESCRIÇÃO'].unique())

df_infos.columns = RealEstateFunds.get_meaning_of_fields().values()

# with st.expander("Visualizar dados brutos"):
#     st.dataframe(df_infos)

df_infos = df_infos[["Nome", "Cotação", "P/VP", "VAL. PATRIMONIAL P/ COTA", 'SEGMENTO', "Valorização"]]

fiis['VALORIZAÇÃO'] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["Valorização"])
fiis["SEGMENTO"] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["SEGMENTO"])
fiis["COTAÇÃO"] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["Cotação"])
fiis["P/VP"] = fiis["DESCRIÇÃO"].map(df_infos.set_index("Nome")["P/VP"])

fiis["P/VP"] = fiis["P/VP"].str.replace(',', '.')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('.', '')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace('R$ ', '')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].str.replace(',', '.')
fiis['VALOR BRUTO'] = fiis['VALOR BRUTO'].astype(float)

fiis["COTAÇÃO"] = fiis["COTAÇÃO"].str.replace(',', '.')
fiis["COTAÇÃO"] = fiis["COTAÇÃO"].str.replace('R$ ', '')
fiis['COTAÇÃO'] = fiis['COTAÇÃO'].astype(float)

fiis["VALORIZAÇÃO"] = fiis["VALORIZAÇÃO"].str.replace(',', '.')
fiis["VALORIZAÇÃO"] = fiis["VALORIZAÇÃO"].str.replace('%', '')
fiis["VALORIZAÇÃO"] = fiis["VALORIZAÇÃO"].astype(float)

fiis['QUANTIDADE'] = fiis['QUANTIDADE'].str.replace(',0', '')
fiis['QUANTIDADE'] = fiis['QUANTIDADE'].astype(int)

fiis.drop(columns=['TIPO DE INVESTIMENTO'], inplace=True)


def bigger_than_pvp(value):
    if float(value) < 1.0:
        return 'background-color: green'

    if float(value) > 1.0:
        return 'background-color: Firebrick'


def bigger_than_val(value):
    if float(value) > 0:
        return 'background-color: green'

    if float(value) < 0:
        return 'background-color: Firebrick'


styled_df = fiis.style
styled_df = styled_df.format({
    'VALOR BRUTO': 'R${:,.2f}',
    'VALORIZAÇÃO': '{:.2f}%',
    'COTAÇÃO': 'R$ {:,.2f}'})

styled_df = styled_df.applymap(bigger_than_pvp, subset=['P/VP'])
styled_df = styled_df.applymap(bigger_than_val, subset=['VALORIZAÇÃO'])

st.dataframe(styled_df, use_container_width=True)

st.title('Gráficos Por:')

col1, col2, col3 = st.columns(3)

# Tamanho fixo para as figuras
fig_width = 300
fig_height = 300

with col1:
    fig1, ax1 = plt.subplots(figsize=(fig_width / 100, fig_height / 100))
    ax1.pie(fiis['VALOR BRUTO'], labels=fiis['DESCRIÇÃO'], autopct='%1.1f%%')
    ax1.axis('equal')
    st.pyplot(fig1)

with col2:
    segmentos = fiis.groupby('SEGMENTO').sum().reset_index()
    segmentos.sort_values(by=['VALOR BRUTO'], inplace=True, ascending=False)

    fig2, ax2 = plt.subplots(figsize=(fig_width / 100, fig_height / 60.5))
    ax2.pie(segmentos["VALOR BRUTO"], labels=segmentos["SEGMENTO"], autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)


with col3:
    seg_valor = fiis.groupby('SEGMENTO').sum().reset_index().sort_values(by=['VALOR BRUTO'], ascending=False)
    st.dataframe(seg_valor[["SEGMENTO", "VALOR BRUTO"]], use_container_width=True)
