import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
from PIL import Image
from io import BytesIO
import base64

load_dotenv()
openai.api_key = os.getenv('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')

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))


lida = Manager(text_gen = llm("openai"))
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)

menu = st.sidebar.selectbox("Choose an Option", ["Summarize", "Question based Graph"])

if menu == "Summarize":
    st.subheader("contextualVisualize pro")
    file_uploader = st.file_uploader("Upload your CSV", type="csv")
    if file_uploader is not None:
        path_to_save = "filename.csv"
        with open(path_to_save, "wb") as f:
            f.write(file_uploader.getvalue())
        summary = lida.summarize("filename.csv", summary_method="default", textgen_config=textgen_config)
        st.write(summary)
        goals = lida.goals(summary, n=2, textgen_config=textgen_config)
        for goal in goals:
            st.write(goal)
        i = 0
        library = "seaborn"
        textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
        charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)  
        img_base64_string = charts[0].raster
        img = base64_to_image(img_base64_string)
        st.image(img)
        


        

            



