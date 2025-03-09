import streamlit as st
from drug_affection import DrugRegionParser
import numpy as np
import pandas as pd

def twod_visualizer():
    with st.form("visualize_form"):
        drug_name = st.text_input("Drug Name", key="drug_name")
        submit = st.form_submit_button("Visualize")

        if submit:
            st.write(f"Effects of {drug_name}")

            parser = DrugRegionParser(drug_name)
            # print(parser.findAffected())
            data = parser.findAffected()
            # df = pd.DataFrame(
            #     np.random.randn(10, 5), columns=['']
            # )

            for affections in data['affections']:
                print(affections)

            # st.table(df)