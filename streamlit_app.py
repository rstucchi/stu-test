import pandas as pd
import streamlit as st
import lxml
import ssl
import datetime
import numpy as np
from pytz import timezone

def calc_orario_prev(row):
    dum = row['Orario'].split()[1]
    items = dum.split(':')
    return items[0]+':'+items[1]

def calc_ritardo(row):
    if str(row['Ritardo']) == '0.0':
        return '0 min'
    elif str(row['Ritardo']) == 'nan':
        return '-'
    else:
        return row['Ritardo'].replace(' min.', '')+' min'

def calc_orario_eff(row):
    tim = datetime.datetime.strptime(row['Orario_previsto'], '%H:%M').time()
    if str(row['Ritardo']) == '0.0':
        return tim.strftime('%H:%M')
    elif str(row['Ritardo']) == 'nan':
        return '-'
    else:
        rit = int(row['Ritardo'].replace(' min.', ''))
        new_tim = datetime.datetime.combine(datetime.date.today(), tim) + datetime.timedelta(minutes=rit)
        return new_tim.strftime('%H:%M')
    
def calc_in_arrivo(row):
    if row['Orario_effettivo'] == '-':
        return '-'
    else:
        tim = datetime.datetime.strptime(row['Orario_effettivo'], '%H:%M').time()
        new_tim = datetime.datetime.combine(datetime.date.today(), tim)
        tim2 = datetime.datetime.now(timezone('Europe/Rome'))
        new_tim_str = new_tim.strftime('%d.%m.%Y %H:%M')
        print(new_tim_str)
        tim2_str = tim2.strftime('%d.%m.%Y %H:%M')
        print(tim2_str)
        delta = datetime.datetime.strptime(new_tim_str, '%d.%m.%Y %H:%M') - datetime.datetime.strptime(tim2_str, '%d.%m.%Y %H:%M')
        return str(int(delta.total_seconds()/60)) + ' min'
    
def color_text(val):
    val_check = val.replace(' min', '')
    if val_check == '-':
        color = 'black'
    elif int(val_check) > 0:
        color = 'red'
    else:
        color = 'green'
    return 'color: %s' % color

def font_bold(val):
    #return 'font-weight: bold'
    return 'background-color: lemonchiffon'

def update_dataframe(direzione, fermata):
    # Read table
    url = r'https://www.asfautolinee.it/subpage_orari_osm.php?lang=it&linea=N_1&direzione='+direzione+'&fermata='+fermata
    tables = pd.read_html(url)

    df = tables[0].iloc[:5]

    df['Orario_previsto'] = df.apply(lambda row: calc_orario_prev(row), axis=1)
    df['Ritardo_new'] = df.apply(lambda row: calc_ritardo(row), axis=1)
    df['Orario_effettivo'] = df.apply(lambda row: calc_orario_eff(row), axis=1)
    df['In_arrivo'] = df.apply(lambda row: calc_in_arrivo(row), axis=1)

    df = df.drop(['Orario', 'Ritardo', 'Orario_effettivo'], axis=1)

    # Display the data as a table using `st.dataframe`.
    st.dataframe(
        df.style.applymap(color_text, subset=['Ritardo_new']).applymap(font_bold, subset=['In_arrivo']),
        use_container_width=True,
        hide_index=True,
        column_config={"Orario_previsto": st.column_config.TextColumn("Orario previsto"), "Ritardo_new": st.column_config.TextColumn("Ritardo"), "In_arrivo": st.column_config.TextColumn("In arrivo tra")},
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
