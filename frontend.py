import streamlit as st
import requests
import json

def main():
    st.title("Fake News Detector")
    
    # Create a text area for user input
    news = st.text_area("Enter news details:", height=300)
    
    # Button to trigger prediction
    if st.button("Predict"):
        # Prepare the input data
        input_string = {"News": news}
        
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

if __name__ == "__main__":
    main()
