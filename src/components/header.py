import base64
import streamlit as st
from pathlib import Path

def header_home():
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"

    try:
        # Check if file exists and has content
        if logo_path.exists() and logo_path.stat().st_size > 0:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            
            st.markdown(f"""
            <div style="display: flex; justify-content: center; padding: 20px 0;">
                <img src="data:image/png;base64,{encoded}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Logo file is empty or missing. Please add a logo image to: src/assets/logo.png")
    except Exception as e:
        st.error(f"Error loading logo: {str(e)}")
    
    # Title and tagline
    st.markdown("""
                
    <h3 style="
        color:#6495ed;
        font-weight:400;
        margin-top:8px;
        text-align:center;">
        AI Powered Smart Attendance System
    </h3>

    <p style="
        color:#9CA3AF;
        font-size:18px;
        font-style:italic;
        text-align:center;">
        Capture Once. Mark Everyone.
    </p>
    """, unsafe_allow_html=True)

def header_dashboard():
    logo_path = Path(__file__).parent.parent / "assets" / "logo.png"

    try:
        # Check if file exists and has content
        if logo_path.exists() and logo_path.stat().st_size > 0:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            
            st.markdown(f"""
            <div style="display: flex; justify-content: center; padding: 20px 0;">
                <img src="data:image/png;base64,{encoded}" style="width: 200px; height: 200px; border-radius: 50%; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Logo file is empty or missing. Please add a logo image to: src/assets/logo.png")
    except Exception as e:
        st.error(f"Error loading logo: {str(e)}")