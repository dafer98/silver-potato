import nltk_download_utils
import streamlit as st
from pyresparser import ResumeParser
import pandas as pd
import pathlib
from datetime import date



@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


def main():

    data_ingested = []

    st.title('My first app')
    st.write('')
    with st.form(key='resumeFile'):
        resume_parsed = st.file_uploader("Upload Excel file", type=['docx','pdf','doc','txt'], accept_multiple_files=True)
        submitted = st.form_submit_button('Submit Resume')

    if submitted:
        total_count_files = float(len(resume_parsed))
        current_file_count = 0.0
        progress_bar = st.empty()
        progress_bar.progress(0.0)
        for file in resume_parsed:
            st.write(file)
            print(file)
            progress_bar.progress(current_file_count/total_count_files)
            if pathlib.Path(file.name).suffix != '.doc':
                data = ResumeParser(file).get_extracted_data()
                data_ingested.append([data['name'], data['email'], data['mobile_number'], file.name])
                extraction_table = pd.DataFrame(data_ingested, columns=['name', 'email', 'mobile number', 'filename'])
            else:
                data = ResumeParser(file).get_extracted_data()
                data_ingested.append([data['name'], data['email'], data['mobile_number'], file.name])
                extraction_table = pd.DataFrame(data_ingested, columns=['name', 'email', 'mobile number', 'filename'])

            current_file_count += 1
            progress_bar.progress(current_file_count/total_count_files)

        progress_bar.success('Completed parsing documents.')
        st.write(extraction_table)
        csv = convert_df(extraction_table)
        st.download_button(
            label='Download Extracted Info',
            data=csv,
            file_name=f'Resume Output {date.today().strftime("%m-%d-%Y")}.csv',
            mime='text/csv',
        )

if __name__ == '__main__':
    main()