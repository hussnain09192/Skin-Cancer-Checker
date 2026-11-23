import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.set_page_config(page_title="Skin Cancer Classification", layout="centered")

st.title("🩺 Skin Cancer (Benign vs Malignant) Classifier")
st.write("Upload an image of the skin lesion, and the trained CNN model will predict whether it is Benign or Malignant.")

# Load the Keras model
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('skin_cancer_cnn_model.keras')

try:
    model = load_my_model()
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

uploaded_file = st.file_uploader("Choose a skin lesion image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Image open karo
    image = Image.open(uploaded_file)

    # 2. FIX: Har qisam ki image ko RGB me convert karo
    # RGBA, P, L, CMYK sab ab RGB ban jayegi
    image = image.convert("RGB")

    st.image(image, caption='Uploaded Image', use_container_width=True)

    # 3. Preprocess image to match the model's training parameters (128x128)
    resized_image = image.resize((128, 128))
    img_array = np.array(resized_image) / 255.0

    # 4. FIX: Ab shape hamesha (128, 128, 3) hogi, is liye direct batch banao
    img_array = np.expand_dims(img_array, axis=0)

    if st.button('Predict'):
        with st.spinner('Analyzing...'):
            prediction = model.predict(img_array)[0][0]

        # Class mapping: {'benign': 0, 'malignant': 1}
        if prediction > 0.5:
            confidence = prediction * 100
            st.error(f"**Prediction: Malignant** (Confidence: {confidence:.2f}%)")
        else:
            confidence = (1 - prediction) * 100
            st.success(f"**Prediction: Benign** (Confidence: {confidence:.2f}%)")
