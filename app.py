import streamlit as st
from pathlib import Path
import google.generativeai as genai
import urllib3
from google.generativeai import caching
from api_key import api_key

genai.configure(api_key=api_key) 

generation_config={
    "temperature":0.4,
    "top_p":1,
    "top_k":32,
    "max_output_tokens":4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]
system_prompt="""
You are a highly advanced medical image analysis system designed to assist healthcare professionals in diagnosing and evaluating medical conditions from imaging data. Your primary task is to analyze medical images, such as X-rays, MRIs, CT scans, or ultrasound images, and provide detailed insights and potential diagnoses based on the visual data.

Input Type: You will receive high-resolution medical images in standard formats (e.g., DICOM, JPEG, PNG).
Output Requirements: Provide a comprehensive analysis that includes:
Identification of any abnormalities or anomalies present in the image.
A list of potential diagnoses or conditions associated with the observed features.
Recommendations for further tests or follow-up actions if necessary.
Confidence levels for each identified condition or feature.
Constraints: Ensure that all analyses are based on established medical knowledge and guidelines. Avoid making definitive diagnoses without suggesting further clinical evaluation.
Ethical Considerations: Maintain patient confidentiality and privacy at all times. Ensure that your analyses are unbiased and based solely on the image data provided.


"""
model=genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    safety_settings=safety_settings
    )



st.set_page_config(page_title="Medical image analysis",page_icon=":robot:")


st.title("medical image analyser")
st.subheader("an app to identify the medical images know their problem")
uploaded_file=st.file_uploader("upload the medical image",type=["png",'jpg'])


submit_button = st.button("generate analysis")

if submit_button:
    
    image_data=uploaded_file.getvalue()
    
    image_parts=[
        {
            "mime_type":"image/jpeg",
            "data":image_data
        }
    ]
    
    prompt_parts=[
        image_parts[0],
        system_prompt,       
    ]
    response=model.generate_content(prompt_parts)
    st.write(response.text)
    