import streamlit as st

def footer_home():
    st.markdown("""
    <style>
    .footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 14px;
        padding-top: 40px;
        padding-bottom: 10px;
    }
    </style>

    <div class="footer">
        ❤️ Created by <b>Rohit Valvi</b>
    </div>
    """, unsafe_allow_html=True)