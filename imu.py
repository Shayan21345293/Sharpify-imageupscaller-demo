import requests
from PIL import Image
from io import BytesIO
import streamlit as st

# Set your API key and URL here
API_KEY = '74a5cf1c90544818847f82e763ea1e05'  # Replace this with your actual API key
API_URL = 'https://www.cutout.pro/api/v1/photoEnhance'

# Function to enhance the image using the API
def enhance_image(image):
    headers = {'APIKEY': API_KEY}
    files = {'file': image.getvalue()}  # Ensure file is in bytes

    try:
        response = requests.post(API_URL, files=files, headers=headers)
        
        # Check if the response status is OK (200)
        response.raise_for_status()  # Will raise an error for bad status codes
        
        if response.status_code == 200:
            # Check if the response is an image (Content-Type header)
            if 'image' in response.headers.get('Content-Type', ''):
                # If the response is an image, return it as a PIL Image
                return Image.open(BytesIO(response.content))
            else:
                # If it's not an image, log the response text for debugging
                print(f"Error: Response is not an image. Response Content: {response.text}")
                st.error("Error: The response is not an image.")
                return None
        else:
            print(f"API Error: {response.status_code}, {response.text}")
            st.error(f"API Error: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")
        st.error(f"Request failed: {e}")
        return None

# Streamlit UI
# Set the title and favicon (emoji as favicon)
st.set_page_config(page_title="Sharpify", page_icon="✨")

# Add a header/title for the app
st.title("Demo Version")
st.title("🔪Sharpify - Image Enhancer 📸")

# File uploader widget to allow the user to upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize session state to store uploaded and enhanced images
if "enhanced_image" not in st.session_state:
    st.session_state.enhanced_image = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Check if a file is uploaded
if uploaded_file is not None:
    # Check if the uploaded image is different from the previous one
    if uploaded_file != st.session_state.uploaded_file:
        # New image uploaded, reset enhanced image and process the new one
        st.session_state.enhanced_image = None  # Reset enhanced image
        st.session_state.uploaded_file = uploaded_file  # Store the new uploaded file

        with st.spinner("Enhancing image..."):
            # Enhance the new uploaded image
            st.session_state.enhanced_image = enhance_image(uploaded_file)

    # Create two columns: one for the uploaded image and one for the enhanced image
    col1, col2 = st.columns(2)
    
    with col1:
        # Show the uploaded image on the left side
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    with col2:
        if st.session_state.enhanced_image:
            # Display the enhanced image on the right side
            st.image(st.session_state.enhanced_image, caption="Enhanced Image", use_container_width=True)

            # Save the enhanced image to a BytesIO object for download
            enhanced_image_bytes = BytesIO()
            st.session_state.enhanced_image.save(enhanced_image_bytes, format='PNG')
            enhanced_image_bytes.seek(0)  # Reset the pointer to the beginning

            # Create a download button for the enhanced image
            st.download_button(
                label="Download Enhanced Image",
                data=enhanced_image_bytes,
                file_name="enhanced_image.png",
                mime="image/png"
            )
        else:
            st.write("No enhanced image available.")

# Footer text at the bottom in small size
st.markdown("<small style='color:gray;'>This app is created by Shayan.</small>", unsafe_allow_html=True)
