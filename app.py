import streamlit as st
from app_methods import *

# Desing Application name on browser and default settings
st.set_page_config(page_title="Text Analysis Tool",
                   page_icon='📊',
                   initial_sidebar_state='expanded')


def main():
    """
    Main function to run the Streamlit NLP application.
    
    This function sets up the Streamlit interface with a sidebar menu
    and handles user interactions for text analysis or file uploads.
    """

    st.title("NLP Application With Streamlit") # Title of the app

    # Design Menu
    menu = ['Text Analysis Dashboard', 'File-Based NLP Analysis', "About This Application"]
    choice = st.sidebar.selectbox("Menu", menu) # Sidebar menu for navigation

    if choice == "Text Analysis Dashboard":
        st.subheader("Analyze Text")
        # Text area for user to input text
        raw_text = st.text_area("Enter Text Here...", height=250)

        # Sidebar input to choose the number of most common tokens to display
        num_most_common = st.sidebar.number_input("Most Common Tokens", 1, 10)

        # Button to trigger text analysis
        if st.button("Analyze"):
            analyze_text(raw_text, num_most_common) # Call function to analyze text

    elif choice == "File-Based NLP Analysis":
        st.subheader("Upload and Analyze Text Files")
        # File uploader to allow users to upload text files (PDF, DOCX, TXT)
        text_file = st.file_uploader("Upload Files", type=['pdf', 'docx', 'txt'])

        # Sidebar input to choose the number of most common tokens to display
        num_most_common = st.sidebar.number_input("Most Common Tokens", 1, 10)

        # Check if a file is uploaded
        if text_file is not None:
            raw_text = handle_uploaded_file(text_file) # Call function to handle uploaded file
            analyze_text(raw_text, num_most_common) # Call function to analyze text


    # About section
    else:
        st.write("""
        Welcome to the NLP Application with Streamlit!

        This interactive application is designed to provide comprehensive text analysis using Natural Language Processing (NLP) techniques. Whether you're a data scientist, researcher, or simply curious about text analysis, this tool offers a user-friendly platform to explore various aspects of text data.
        """)

        st.subheader("Key Features:")

        st.markdown("""
        1. **Text Analysis Dashboard:**
           - Enter your text directly into the application and receive detailed insights.
           - Analyze the structure and components of your text, including tokenization, part-of-speech tagging, and lemmatization.
           - Identify named entities (such as names, locations, and organizations) within your text.

        2. **File-Based NLP Analysis:**
           - Upload text files in PDF, DOCX, or TXT formats for analysis.
           - Extract and process text from uploaded files seamlessly.
           - Perform the same in-depth analysis as the Text Analysis Dashboard on your file content.

        3. **Comprehensive Visualizations:**
           - Generate visual representations of word frequencies, part-of-speech distributions, and more.
           - Create word clouds to visualize the most prominent words in your text.
           - Interactive charts and graphs to help you understand your data better.

        4. **Sentiment Analysis:**
           - Determine the sentiment of your text using advanced algorithms.
           - Gain insights into the overall tone and emotional impact of the content.

        5. **Downloadable Results:**
           - Export your analysis results as CSV files for further use and documentation.
           - Download visualizations for reports and presentations.
        """)

        st.write("""
        This application leverages powerful libraries and tools, including SpaCy for NLP, TextBlob for sentiment analysis, and Seaborn and Matplotlib for data visualization. With its intuitive interface and robust functionalities, our NLP application aims to make text analysis accessible and insightful for everyone.

        We hope you find this tool valuable and insightful. For any questions, feedback, or further information, please feel free to reach out.
        """)

        st.subheader("About the Developer")

        st.write("""
        This NLP Application was developed by Mohammadreza Mohammadi, a passionate software developer and data scientist.
                With a strong background in Natural Language Processing and data visualization.
        - **LinkedIn:** [LinkedIn Profile](https://www.linkedin.com/in/mohammadreza-mohammadi-24a3a61b3/)
        - **GitHub:** [GitHub Profile](https://github.com/mohammadreza-mohammadi94)
        - **Email:** mr.mhmdi93@gmail.com

        For any inquiries or collaboration opportunities, feel free to connect through the above channels.
        """)




if __name__ == '__main__':
    main()