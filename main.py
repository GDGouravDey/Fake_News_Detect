from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pickle

# Load model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

app = FastAPI()

class Input(BaseModel):
    News: str
    
@app.get("/")
def read_root():
    return {"msg": "Fake News Detector"}
    
@app.post("/detect")
def predict_news(input: Input):
    # Transform input data
    print(input.News)
    data_in = [input.News]  # Make it a list to match the expected input shape
    transformed_data = vectorizer.transform(data_in)
    
    # Make prediction
    prediction = model.predict(transformed_data)
    
    # Return the result
    if prediction[0] == 0:
        return {'prediction': 'Non-Reliable or Fake News'}
    else:
        return {'prediction': 'Reliable News'}
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
