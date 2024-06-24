import streamlit as st
import requests
from PIL import Image
import io

# Streamlit configuration
st.set_page_config(
    page_title="Image Analyzer",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS for mobile-friendly design
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .stFileUploader > div > div > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def send_image_to_api(image):
    """Send image to API and return the response"""
    url = "https://doevent.ru/api/v1"
    files = {"image": ("image.jpg", image, "image/jpeg")}
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the API: {e}")
        return None

def main():
    st.title("Image Analyzer")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Send image to API
        with st.spinner("Analyzing image..."):
            result = send_image_to_api(img_byte_arr)
        
        if result:
            # Display received image
            st.image(result["image_url"], caption="Processed Image", use_column_width=True)
            
            # Display received text
            st.write("Analysis Result:")
            st.write(result["text"])

if __name__ == "__main__":
    main()
