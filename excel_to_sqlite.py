"""Streamlit app to upload an Excel file and download it as a Sqlite file."""

import sqlite3
import pandas as pd

import streamlit as st

def main():
    """Main function to upload the Excel file and download the Sqlite file."""
    st.write('<h1>Excel to Sqlite</h1>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose one Excel-file to upload",
                                     type=['xls', 'xlsx'],
                                     accept_multiple_files=False)
    if uploaded_file is not None:
        df_dict = pd.read_excel(uploaded_file,
                                sheet_name = None, # None for all sheets
                                engine= 'openpyxl')
        # display file name
        fn = uploaded_file.name
        st.write(f'<h2>File: {fn}</h2>', unsafe_allow_html=True)

        # connect to sqlite
        con = sqlite3.connect(f"{fn.split('.')[0]}.sqlite")
        # get sheet names
        for sheet in list(df_dict.keys()):
            st.write(f'<h3>Sheet: {sheet}</h3>', unsafe_allow_html=True)
            if 10 > len(df_dict[sheet].index):
                shown_rows = len(df_dict[sheet].index)
            else:
                shown_rows = 10
            st.write(f'{shown_rows} rows of {str(len(df_dict[sheet].index))} shown here')
            st.write(df_dict[sheet].head(10))
            print('\n<br />\n')

            # store to sqlite file
            df_dict[sheet].to_sql(sheet, con, if_exists="replace")

        con.close()

        # download df_dict as sqlite
        st.write(f'<h2>Download: {fn.split('.')[0]}.sqlite</h2>', unsafe_allow_html=True)
        with open(f"{fn.split('.')[0]}.sqlite", "rb") as file:
            st.download_button(
            label="Download sqlite",
            data=file,
            file_name=f"{fn.split('.')[0]}.sqlite"
            )

if __name__ == '__main__':
    main()
