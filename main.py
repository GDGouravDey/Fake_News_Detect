import threading
import uvicorn
import pickle
import requests
import json
import streamlit as st
from fastapi import FastAPI
from pydantic import BaseModel
from newspaper import Article

# Define FastAPI app
app = FastAPI()

class Input(BaseModel):
    News: str

# Load model and vectorizer
model = pickle.load(open('news_model.pkl', 'rb'))
vectorizer = pickle.load(open('news_vectorizer.pkl', 'rb'))

@app.get("/")
def read_root():
    return {"msg": "Fake News Detector"}

@app.post("/detect")
def predict_news(input: Input):
    data_in = [input.News]  
    transformed_data = vectorizer.transform(data_in)
    
    prediction = model.predict(transformed_data)
    
    if prediction[0] == 0:
        return {'prediction': 'Non-Reliable or Fake News'}
    else:
        return {'prediction': 'Reliable News'}

def fetch_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return None

def streamlit_app():
    st.title("Fake News Detector App")
    url = st.text_input("Enter the news article or URL of the news article:")

    if st.button("Predict"):
        if url:
            if url.startswith("http") or url.startswith("www"):
                article_content = fetch_article_content(url)
            else:
                article_content = url
            
            if article_content:
                input_string = {"News": article_content}
                
                try:
                    response = requests.post(
                        url="http://127.0.0.1:8000/detect",
                        data=json.dumps(input_string),
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
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

def run_app():
    def run_fastapi():
        uvicorn.run(app, host="127.0.0.1", port=8000)
    
    threading.Thread(target=run_fastapi, daemon=True).start()
    
    streamlit_app()

if __name__ == "__main__":
    run_app()
