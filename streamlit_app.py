import pandas as pd
import streamlit as st
import lxml
import ssl
import datetime
import numpy as np

def edit_table(row):
    dum = row['Orario'].split()[1]
    items = dum.split(':')
    return items[0]+':'+items[1]

def edit_table_2(row):
    if str(row['Ritardo']) == '0.0':
        return '0'
    elif str(row['Ritardo']) == 'nan':
        return '-'
    else:
        return row['Ritardo'].replace(' min.', '')

def edit_table_3(row):
    tim = datetime.datetime.strptime(row['Orario_previsto'], '%H:%M').time()
    if str(row['Ritardo']) == '0.0':
        return tim.strftime('%H:%M')
    elif str(row['Ritardo']) == 'nan':
        return '-'
    else:
        rit = int(row['Ritardo'].replace(' min.', ''))
        new_tim = datetime.datetime.combine(datetime.date.today(), tim) + datetime.timedelta(minutes=rit)
        return new_tim.strftime('%H:%M')

def color_text(val):

    if val == '-':
        color = 'black'
    elif int(val) > 0:
        color = 'red'
    else:
        color = 'green'
    return 'color: %s' % color

def update_dataframe(direzione, fermata):
    # Read table
    #url = r'https://www.asfautolinee.it/subpage_orari_osm.php?lang=it&linea=N_1&direzione=1&fermata=COMO_A07'
    url = r'https://www.asfautolinee.it/subpage_orari_osm.php?lang=it&linea=N_1&direzione='+direzione+'&fermata='+fermata
    tables = pd.read_html(url)

    df = tables[0].iloc[:5]

    df['Orario_previsto'] = df.apply(lambda row: edit_table(row), axis=1)
    df['Ritardo_new'] = df.apply(lambda row: edit_table_2(row), axis=1)
    df['Orario_effettivo'] = df.apply(lambda row: edit_table_3(row), axis=1)

    df = df.drop(['Orario', 'Ritardo'], axis=1)

    # Display the data as a table using `st.dataframe`.
    st.dataframe(
        df.style.applymap(color_text, subset=['Ritardo_new']),
        use_container_width=True,
        hide_index=True,
        column_config={"Orario_previsto": st.column_config.TextColumn("Orario previsto"), "Ritardo_new": st.column_config.TextColumn("Ritardo"), "Orario_effettivo": st.column_config.TextColumn("Orario effettivo")},
    )

# To not have an error
ssl._create_default_https_context = ssl._create_unverified_context

# Show the page title and description.
st.set_page_config(page_title="Orario bus", page_icon="🚌")
st.title("🚌 Orario bus")
st.write(
    """
    ASF autolinee
    """
)

b1, b2, b3 = st.columns(3)
if b1.button("💼 Rosales➜Chiasso", use_container_width=True):
    update_dataframe(direzione = '2', fermata = 'AURORR01')
if b2.button("🏠 Chiasso➜Rosales (in arrivo)", use_container_width=True):
    update_dataframe(direzione = '2', fermata = 'PCHIAR08')
if b3.button("🏢 Rosales➜Como", use_container_width=True):
    update_dataframe(direzione = '1', fermata = 'AURORA01')
