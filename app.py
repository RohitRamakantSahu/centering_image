import streamlit as st
from PIL import Image
import io

def center_image(img, canvas_width=1080, canvas_height=1080):
    # Create a new blank canvas with white background
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    
    # Calculate scaling factor to fit either width or height
    width_ratio = canvas_width / img.width
    height_ratio = canvas_height / img.height
    
    # Use the smaller ratio to ensure image fits without stretching
    scale_ratio = min(width_ratio, height_ratio)
    
    # Calculate new dimensions
    new_width = int(img.width * scale_ratio)
    new_height = int(img.height * scale_ratio)
    
    # Resize image maintaining aspect ratio
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Calculate position to center the image
    x = (canvas_width - new_width) // 2
    y = (canvas_height - new_height) // 2
    
    # Paste the resized image onto the canvas
    canvas.paste(resized_img, (x, y))
    
    return canvas

st.set_page_config(page_title="Image Center", page_icon="🎨", layout="wide")

st.title("Image Center Tool")
st.write("Upload an image to center it on a canvas while maintaining aspect ratio")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Canvas size inputs
col1, col2 = st.columns(2)
with col1:
    canvas_width = st.number_input("Canvas Width", min_value=100, max_value=4000, value=1080)
with col2:
    canvas_height = st.number_input("Canvas Height", min_value=100, max_value=4000, value=1080)

if uploaded_file is not None:
    # Display original image
    image = Image.open(uploaded_file)
    st.subheader("Original Image")
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Process and display centered image
    centered_image = center_image(image, canvas_width, canvas_height)
    st.subheader("Centered Image")
    st.image(centered_image, caption="Centered Image", use_column_width=True)
    
    # Download button
    buf = io.BytesIO()
    centered_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download Centered Image",
        data=byte_im,
        file_name="centered_image.png",
        mime="image/png"
    ) 