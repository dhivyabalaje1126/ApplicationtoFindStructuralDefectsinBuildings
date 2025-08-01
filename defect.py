# Libraries
import os
import streamlit as st 
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title='Defect Detection in Buildings',page_icon='🏢',layout='wide')

st.title('AI Assistant for :green[Detection and Analysis of Structural Defects in Buildings]')
st.subheader('Prototype for automated structural defect analysis',divider=True)

st.sidebar.text('Designed by Dhivya Balaje')
st.sidebar.text('My Linkedin:  https://www.linkedin.com/in/dhivya-balaje-a4b886205/')
st.sidebar.text('My Github: https://github.com/dhivyabalaje1126')

with st.expander('About the Application:'):
    st.markdown(f''' This prototype is used to detect the presence of
            structural defects in images provided of buildings. 
            These defects and their implications will be analyzed using an AI-powered system. 
            It performs **Defect Detection** (automatically detects structural defects such as cracks, weathering, in images),
            **Recommendation** (provides solutions and recommendations for actions based on the defects), and
            **Report Generation** (provides a report about the defects and the recommendations for documentation purposes). 
            ''' )
   
# Getting api key 
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)

st.subheader('Upload your images here!')
input_image = st.file_uploader('Drop files',
                 type=['png','jpg','jpeg'])

# Using Image from pillow
if input_image:
    img = Image.open(input_image)
    st.image(img,caption='Uploaded image')
    
    # Prompt to feed to the gemini model
    prompt = f'''
    Act as a construction, safety, and building defect specialist. 
    Analyze the provided image and identify defects related to construction. 
    You will be looking for cracks, weathering and climate-related damage in buildings, structural integrity,
    damage to the building based on the image provided.
    Your task then, is to list down the defects you find, and list the possible causes of these defects, like error in manufacturing,
    possible damage due to high-impact collisions or natural disasters and events. Cover all possible scenarios. 
    Then, relay the impact of these defects you've spotted one by one, ranked based on descending order of severity of the defect and the worst impact it can have,
    all the way to the minimal impact. 
    Your priority is the safety of the building's structural integrity and of the general public. 
    Rate the safety level of the building based on the defect present from a scale of 1 (minimal harm, safe) to 10 (immediate action required, unsafe to use building).
    List down ways to prevent such defects, with recommended actions for the defects found. Be very thorough and detailed. 
    Then summarize the information you've provided with the safety rating, key insights about the defects and immediate recommended actions.
    ''' 
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_results(prompt,input_image):
        result = model.generate_content(f''' Using the given {prompt},
                                        analyze the given image {input_image} and generate results.''')
        return result.text
    
    submit = st.button('Analyze the defect')
    if submit:
        with st.spinner('Analyzing. Will get back to you shortly..'):
            response = generate_results(prompt, input_image)
            st.markdown(':green[Results]')
            st.write(response)

    


