import altair as alt
import pandas as pd
import streamlit as st
import lxml
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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

# Display the data as a table using `st.dataframe`.
st.dataframe(
    tables[0],
    use_container_width=True,
    #column_config={"year": st.column_config.TextColumn("Year")},
)