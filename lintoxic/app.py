import os
import sys
import asyncio

from PIL import Image
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from lintoxic.services.evaluate.toxicity import check_toxicity
from lintoxic.services.evaluate.fact import check_fact_accuracy
from lintoxic.utils.image import extract_text as extract_text_from_image
from lintoxic.utils.nsfw import NSFWImageClassificationModel
from lintoxic.utils.audio import AudioProcessor

load_dotenv()

nsfw_image_classification: NSFWImageClassificationModel = NSFWImageClassificationModel.get_instance()
audio_processor = AudioProcessor.get_instance()

upload_directory = os.getenv("UPLOAD_DIR") if os.getenv("UPLOAD_DIR") else os.path.join(Path.home(), "lintoxic", "upload")
parent_dir = os.getenv("PREPROCESSING_DIR") if os.getenv("PREPROCESSING_DIR") else os.path.join(Path.home(), "lintoxic", "preprocessing")

try:
    os.makedirs(upload_directory, exist_ok=True)
    os.makedirs(parent_dir, exist_ok=True)

except:
    sys.exit(1)

async def check_text(text: str):
    (toxic, result) = check_toxicity(text)
    if toxic:
        reasons = []
        if (label := result.get("label")):
            key_name = " ".join(list(map(str.capitalize, label.split("_"))))
            reasons.append(f"- **{label}**: **{int(result.get("score")) * 100}%**")    
        else:
            for (key, value) in result:
                key_name = " ".join(list(map(str.capitalize, key.split("_"))))
                reasons.append(f"- **{key_name}**: **{int(value * 100)}%**")
            reasons_string = "\n".join(reasons)
            return (True, f"""
                <h1>Unacceptable Content in Text!</h1>
                <h2>Reasons:</h2>
                {reasons_string}
            """)
        accuracy = await check_fact_accuracy(text=text)
        if accuracy.false_information:
            reasons = []
            for information in accuracy.false_information:
                if information.is_correct == "False":
                    reason = f"""
                    <li><b style="color: red;">{information.is_correct}</b>: {information.explanations}</li>
                    """
                    reasons.append(reason)
                else:
                    reason = f"""
                    <li><b style="color: blue;">{information.is_correct}</b>: {information.explanations}</li>
                    """
                    reasons.append(reason)
                reasons_string = "\n".join(reasons)
                return (True, f"""
                        <h1>Misleading content present in Text!</h1>
                        <h2>Reasons:</h2>
                        <ul>
                        {reasons_string}
                        </ul>
                        """)
        else:
            return (False, "The content is not toxic and is factually accurate")


async def app():
    st.set_page_config(page_title="Lintoxic", page_icon="broom")

    async def check_content(text=None, image=None, audio=None, video=None):
        if text:
            result = await check_text(text)
            return result

        if image:
            text = extract_text_from_image(image)
            if text:
                result = await check_text(text)
                if result[1] != "The content is not toxic and is factually accurate":
                    return (True, result)
            nsfw = nsfw_image_classification.predict(image_content=image)
            if nsfw[0] == 1:
                return (True, """<p style="font-size: 2em;"The given image contains NSFW content</p>""")
            return (False, """<p style="font-size: 2em;"Acceptable Content in Image</p>""")
        
        if audio:
            upload_path = os.path.join(upload_directory, audio.name)
            with open(upload_path, "wb") as f:
                f.write(audio.getbuffer())
            transcription = audio_processor.process_audio(upload_path)
            if transcription:
                result = await check_text(transcription)
                if result[1] != "The content is not toxic and is factually accurate":
                    return (True, result)
                return result
        
        if video:
            upload_path = os.path.join(upload_directory, video.name)
            with open(upload_path, "wb") as f:
                f.write(video.getbuffer())
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
        audio_upload = st.file_uploader("Upload Audio", type=["mp3", "wav", "flac"])
        uploaded_content = audio_upload
        if uploaded_content is not None:
            st.audio(uploaded_content, format=uploaded_content.type)

    elif content_type == "Video":
        video_upload = st.file_uploader("Upload Video", type=["mp4", "avi", "mov", "mkv"])
        uploaded_content = video_upload
        if uploaded_content is not None:
            st.video(uploaded_content)

    else:
        uploaded_content = None

    if st.button("Check Content"):
        if uploaded_content:
            result = None
            if content_type == "Text":
                result = await check_content(text=uploaded_content)
            elif content_type == "Image":
                image = Image.open(uploaded_content)
                result = await check_content(image=image)
            elif content_type == "Audio":
                result = await check_content(audio=uploaded_content)
            elif content_type == "Video":
                result = await check_content(video=uploaded_content)
            if result:
                st.html(f"""
                <div style="background-color: #f0808088;padding: 16px;border-radius: 2em;text-align: center;">
                {result[1]}
                </div>
                """)
            else:
                st.html(f"""
                <div style="background-color: #9de7bf88;padding: 16px;border-radius: 2em;text-align: center;">
                {result[1]}
                </div>
                """)

        else:
            st.write("Please upload content to check.")

asyncio.run(app())