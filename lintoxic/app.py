import os

from PIL import Image
import streamlit as st

from lintoxic.services.evaluate.toxicity import check_toxicity

st.set_page_config(page_title="Lintoxic", page_icon="broom")

def check_content(text=None, image=None, audio=None, video=None):
    if text:
        (toxic, result) = check_toxicity(text=text)
        if toxic:
            reasons = []
            if (label := result.get("label")):
                print(label)
                key_name = " ".join(list(map(str.capitalize, label.split("_"))))
                reasons.append(f"- **{label}**: **{result.get("score") * 100}%**")
            
            else:
                for (key, value) in result:
                    key_name = " ".join(list(map(str.capitalize, key.split("_"))))
                    reasons.append(f"- **{key_name}**: **{int(value * 100)}%**")
            reasons_string = "\n".join(reasons)
            return f"""
                    # Unacceptable Content in Text!
                    ## Reasons:
                    {reasons_string}
                    """
        
        else:
            return "The content is not toxic"

    if image:
        return "Acceptable Content in Image"
    
    if audio:
        return "Acceptable Content in Audio"
    
    if video:
        return "Acceptable Content in Video"
    
    return "Acceptable Content"

st.title("Content Upload and Checking Dashboard")

content_type = st.selectbox(
    "Select the type of content you want to upload",
    ["Select", "Text", "Image", "Audio", "Video"]
)

if content_type == "Text":
    text_input = st.text_area("Enter Text Content", "")
    uploaded_content = text_input

elif content_type == "Image":
    image_upload = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    uploaded_content = image_upload
    if uploaded_content is not None:
        image = Image.open(uploaded_content)
        st.image(image)


elif content_type == "Audio":
    audio_upload = st.file_uploader("Upload Audio", type=["mp3", "wav", "ogg"])
    uploaded_content = audio_upload

elif content_type == "Video":
    video_upload = st.file_uploader("Upload Video", type=["mp4", "avi", "mov", "mkv"])
    uploaded_content = video_upload

else:
    uploaded_content = None

if st.button("Check Content"):
    if uploaded_content:
        result = None
        if content_type == "Text":
            result = check_content(text=uploaded_content)
        elif content_type == "Image":
            image = Image.open(uploaded_content)
            result = check_content(image=image)
        elif content_type == "Audio":
            result = check_content(audio=uploaded_content)
        elif content_type == "Video":
            result = check_content(video=uploaded_content)

        st.write(result)

    else:
        st.write("Please upload content to check.")
