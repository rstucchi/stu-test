import altair as alt
import pandas as pd
import streamlit as st
import lxml

# Show the page title and description.
st.set_page_config(page_title="Orario bus", page_icon="🚌")
st.title("🚌 Orario bus")
st.write(
    """
    ASF autolinee
    """
)

# Read table
url = r'https://www.asfautolinee.it/subpage_orari_osm.php?lang=it&linea=N_1&direzione=1&fermata=COMO_A07'
tables = pd.read_html(url)