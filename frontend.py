import nltk
nltk.download('punkt')
import streamlit as st
import requests
import json
from newspaper import Article

def fetch_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return None

def main():
    st.title("Fake News Detector App")
    
    # Create a text input for the URL
    url = st.text_input("Enter the news article or URL of the news article:")

    # Button to trigger prediction
    if st.button("Predict"):
        if url:
            if url.startswith("http") or url.startswith("www"):
                article_content = fetch_article_content(url)
            # Fetch the article content from the URL
            else:
                article_content = url
            
            if article_content:
                # Prepare the input data
                input_string = {"News": article_content}
                
                try:
                    # Send the request to the backend API
                    response = requests.post(
                        url="http://127.0.0.1:8000/detect",
                        data=json.dumps(input_string)
                    )
                    
                    # Check the response status
                    if response.status_code == 200:
                        # Parse and display the result
                        result = response.json()
                        st.success(f"Prediction: {result['prediction']}")
                    else:
                        st.error(f"Error: Received status code {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Failed to fetch article content. Please check the URL.")
        else:
            st.warning("Please enter a URL.")

if __name__ == "__main__":
    main()
