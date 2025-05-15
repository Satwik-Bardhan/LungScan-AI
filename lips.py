import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, UnidentifiedImageError
import time
from doctors_data import DOCTORS
from css import CUSTOM_CSS


# CONSTANTS & CONFIG
CLASS_LABELS = {0: 'Healthy', 1: 'Pneumonia', 2: 'Tuberculosis'}
MODEL_PATH = 'model.keras'
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

# Improved is_xray_image function
def is_xray_image(image):
    """
    Check if the uploaded image is likely an X-ray.
    This improved version includes checks for grayscale, dimensions, and pixel intensity distribution.
    """
    # Convert image to grayscale if it's not already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Check image dimensions (X-rays are typically large)
    width, height = image.size
    if width < 500 or height < 500:  # Adjust thresholds as needed
        return False
    
    # Check pixel intensity distribution (X-rays often have a specific intensity range)
    pixel_values = list(image.getdata())
    avg_intensity = sum(pixel_values) / len(pixel_values)
    
    # X-rays typically have a wide range of intensities, but the average is often mid-range
    if avg_intensity < 50 or avg_intensity > 200:  # Adjust thresholds as needed
        return False
    
    return True

# Streamlit Page Configuration
st.set_page_config(page_title="Lung Scan AI", page_icon="🩺")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# MODEL LOADING
@st.cache_resource
def load_model(model_path):
    """Load and cache the pre-trained TensorFlow model"""
    try:
        model = tf.keras.models.load_model(model_path)
        if model.output_shape[-1] != len(CLASS_LABELS):
            st.error("Model output dimension doesn't match class labels!")
            st.stop()
        return model
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        st.stop()

# IMAGE PROCESSING
def preprocess_image(image_file):
    """Process uploaded image for model consumption"""
    try:
        # Attempt to open the image
        img = Image.open(image_file).convert('RGB')
        img = img.resize((64, 64))
        img_array = np.array(img) / 255.0
        return np.expand_dims(img_array, axis=0)
    except UnidentifiedImageError:
        st.error("The uploaded file is not a valid image. Please upload a valid JPG, JPEG, or PNG file.")
        st.stop()
    except Exception as e:
        st.error(f"Image processing error: {str(e)}")
        st.stop()

# RESULT DISPLAY WITH ANIMATIONS
def display_results(prediction, confidence, processing_time):
    """Display diagnosis results with styled components and animations"""
    color_map = {
        'Healthy': '#00ff88',
        'Pneumonia': '#ff7675',
        'Tuberculosis': '#ff4757'
    }
    
    animation_class = {
        'Healthy': 'pulse-positive',
        'Pneumonia': 'pulse-warning',
        'Tuberculosis': 'pulse-alert'
    }[prediction]

    st.markdown(f"""
    <div class="diagnosis-card {animation_class}">
        <h2 style="color: {color_map[prediction]}; text-align: center; margin: 0;">
            {prediction}
        </h2>
        <p style="text-align: center; color: {color_map[prediction]}; margin: 0.5rem 0; font-size: 1.1rem;">
            {confidence:.1f}% confidence
        </p>
        <p style="text-align: center; color: #cccccc; margin-top: 0.5rem;">
            Analysis completed in {processing_time:.2f}s
        </p>
    </div>
    """, unsafe_allow_html=True)

    if prediction == 'Healthy':
        message = "✅ No issues detected!"
        color = '#00c6ff'
        st.balloons()
    else:
        message = "⚠️ Consult a healthcare professional immediately!"
        color = '#ff4b4b'
    
    st.markdown(f"""
    <div style="
        padding: 15px;
        background: {color};
        color: white;
        border-radius: 10px;
        animation: slideIn 0.5s ease-out;
        margin: 1rem 0;
        text-align: center;
    ">
        <strong>{message}</strong>
    </div>
    """, unsafe_allow_html=True)

# DOCTOR PAGE
def show_doctor_page():
    st.markdown(f"""
    <h2 style='text-align: center; color: #00c6ff; margin-bottom: 2rem;'>
        Recommended {st.session_state.diagnosis} Specialists
    </h2>
    """, unsafe_allow_html=True)
    
    doctors = DOCTORS.get(st.session_state.diagnosis)
    
    # Create columns for doctor cards
    cols = st.columns(2)
    for i, doctor in enumerate(doctors):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="doctor-card" style="animation: slideIn 0.3s ease-out {i*0.1}s;">
                <h3 style="color: #63c5da; margin-top: 0;">{doctor['name']}</h3>
                <p style="margin: 0.5rem 0;">
                    <strong>📌 Location:</strong> {doctor['location']}
                </p>
                <p style="margin: 0.5rem 0;">
                    <strong>📧 Contact:</strong> {doctor['contact']}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; margin-top: 2rem;'>", unsafe_allow_html=True)
    if st.button("← Back to Analysis Results", key='back_btn'):
        st.session_state.show_doctors = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# MAIN APPLICATION
def main():
    # Initialize session state variables
    if 'show_doctors' not in st.session_state:
        st.session_state.show_doctors = False
    if 'analyze_clicked' not in st.session_state:
        st.session_state.analyze_clicked = False
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None

    # Check for doctor page first
    if st.session_state.show_doctors:
        show_doctor_page()
        return

    st.markdown("""
    <h1 style='
        text-align: center; 
        color: #00c6ff;
        position: relative;
    '>
        LungScan AI
        <span style='
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            margin-left: 0.5rem;
        '>🔍</span>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ffffff;'>Chest X-ray Analysis powered by Deep Learning</p>", 
                unsafe_allow_html=True)

    # Load model
    model = load_model(MODEL_PATH)

    # File Upload Section
    with st.expander("Upload X-ray Image", expanded=True):
        uploaded_file = st.file_uploader(
            "Select a chest X-ray image", 
            type=ALLOWED_EXTENSIONS,
            help="Supported formats: JPG, JPEG, PNG"
        )

        # Validate the uploaded file
        if uploaded_file is not None:
            try:
                # Attempt to open the image to check if it's valid
                image = Image.open(uploaded_file).convert('RGB')
                
                # Check if the image is likely an X-ray
                if not is_xray_image(image):
                    st.warning("⚠️ The uploaded image does not appear to be an X-ray. Please upload a valid chest X-ray image.")
                    st.stop()

                st.success("Image uploaded successfully! 🎉")

            except UnidentifiedImageError:
                st.error("❌ The uploaded file is not a valid image. Please upload a valid JPG, JPEG, or PNG file.")
                st.stop()

            # Reset session state if a new file is uploaded
            if uploaded_file != st.session_state.uploaded_file:
                st.session_state.uploaded_file = uploaded_file
                st.session_state.analyze_clicked = False  # Reset analyze_clicked

    # Main Content
    if uploaded_file:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.image(uploaded_file, 
                    caption="Uploaded X-ray", 
                    use_container_width=True)
            
            if st.button("Analyze Scan 🚀", type="primary", use_container_width=True): 
                st.session_state.analyze_clicked = True
                st.rerun()

        with col2:
            if st.session_state.analyze_clicked:
                with st.spinner("Analyzing..."):
                    start_time = time.time()
                    
                    # Process and predict
                    processed_image = preprocess_image(uploaded_file)
                    raw_prediction = model.predict(processed_image, verbose=0)
                    predictions = tf.nn.softmax(raw_prediction[0])
                    prediction_idx = np.argmax(predictions)
                    prediction_label = CLASS_LABELS[prediction_idx]
                    confidence = predictions[prediction_idx].numpy() * 100
                    processing_time = time.time() - start_time

                    # Store diagnosis in session state
                    st.session_state.diagnosis = prediction_label
                    st.session_state.analysis_done = True

                    # Display results
                    display_results(prediction_label, confidence, processing_time)

                # Show consultation button if needed
                if prediction_label != 'Healthy':
                    if st.button("📞 Consult a Specialist Doctor", 
                                type = "primary", 
                                use_container_width = True,
                                key = "consult_btn"):
                        st.session_state.show_doctors = True
                        st.session_state.analyze_clicked = False
                        st.rerun()

    # Footer Disclaimer
    st.markdown("""
    <div class="footer">
        <small>
            Note: This AI tool is intended for research and educational purposes only. 
            Always consult a qualified healthcare professional for medical diagnosis.
        </small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <small>
            © LungScan AI | All Rights Reserved
        </small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
