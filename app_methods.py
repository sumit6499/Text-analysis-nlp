import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import use as matplotlib_use
from textblob import TextBlob
from collections import Counter
import base64
import time
from wordcloud import WordCloud
from PyPDF2 import PdfReader
import docx2txt
import spacy
from spacy.cli import download as spacy_download
import neattext as nt
import neattext.functions as nfx

# Configure matplotlib to use the 'Agg' backend
matplotlib_use("Agg")

# Load the spaCy model
spacy_download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

# Time Format for filename
timestr = time.strftime("%Y%m%d-%H%M%S")

# Functions
def text_analyzer(my_text):
    docx = nlp(my_text)
    all_data = [(token.text, token.shape_, token.pos_, token.tag_,
                 token.lemma_, token.is_alpha, token.is_stop) for token in docx]
    df = pd.DataFrame(all_data, columns=['Token', 'Shape', 'PoS', 'Tag', 'Lemma', 'Is_Alpha', 'Is_Stopword'])
    return df

def get_entities(my_text):
    docx = nlp(my_text)
    entities = [(entity.text, entity.label_) for entity in docx.ents]
    return entities

def get_most_common_tokens(my_text, num=5):
    word_tokens = Counter(my_text.split(' '))
    most_common_tokens = dict(word_tokens.most_common(num))
    return most_common_tokens

def get_sentiment(my_text):
    blob = TextBlob(my_text)
    sentiment = blob.sentiment
    return sentiment

def plot_wordcloud(my_text):
    wc = WordCloud().generate(my_text)
    fig = plt.figure()
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)

def download_csv(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_file_name = f'nlp_result_{timestr}_.csv'
    st.markdown('### ⬇️ Download CSV File ⬇️')
    href = f'<a href="data:file/csv;base64, {b64}" download="{new_file_name}">Click Here !!</a>'
    st.markdown(href, unsafe_allow_html=True)

def read_pdf(file):
    pdf_reader = PdfReader(file)
    count = len(pdf_reader.pages)
    all_page_text = ""
    for i in range(count):
        page = pdf_reader.pages[i]
        all_page_text += page.extract_text()
    return all_page_text

def analyze_text(raw_text, num_most_common):
    with st.expander("Original Text"):
        st.write(raw_text)

    with st.expander("Text Analysis"):
        token_res_df = text_analyzer(raw_text)
        st.dataframe(token_res_df)

    with st.expander("Entities"):
        entity_res = get_entities(raw_text)
        st.write(entity_res)

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("Word Stats"):
            st.info("Word Statistics")
            docx = nt.TextFrame(raw_text)
            st.write(docx.word_stats())

        with st.expander("Top Keywords"):
            st.info("Top Keywords/Tokens")
            processed_text = nfx.remove_stopwords(raw_text)
            key_words = get_most_common_tokens(processed_text, num_most_common)
            st.write(key_words)

        with st.expander("Sentiment"):
            sent_res = get_sentiment(raw_text)
            st.write(sent_res)

    with col2:
        with st.expander("Plot Word's Frequency"):
            fig = plt.figure()
            top_key_words = get_most_common_tokens(processed_text, num_most_common)
            plt.bar(key_words.keys(), top_key_words.values())
            st.pyplot(fig)

        with st.expander("Plot Part Of Speech"):
            try:
                fig = plt.figure()
                sns.countplot(x=token_res_df['PoS'], palette='viridis')
                plt.xticks(rotation=45)
                st.pyplot(fig)
            except:
                st.warning("Insufficient Data")

        with st.expander("Plot WordCloud"):
            plot_wordcloud(raw_text)

    with st.expander("Download Text Analysis Result"):
        download_csv(token_res_df)

def handle_uploaded_file(text_file):
    if text_file.type == 'application/pdf':
        raw_text = read_pdf(text_file)
    elif text_file.type == 'text/plain':
        raw_text = str(text_file.read(), encoding='utf-8')
    else:
        raw_text = docx2txt.process(text_file)
    return raw_text
