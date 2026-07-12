import streamlit as st

def style_background_home():
    st.markdown("""
    <style>
               
        .stApp{
                background: #494D5F !important
                }

                .stApp div[data-testid="stColumn"]{
                    background-color:#e5eaf5 !important;
                    padding: 1.5rem !important;
                    border-radius: 4rem !important;
                }

    """,unsafe_allow_html=True)

def style_background_dashboard():
    st.markdown("""
    <style>
                .stApp{
                background: #E2E3FF !important
                }
                </style>

    """,unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,wght@6..144,1..1000&display=swap');
                /* Hide Tool Bar of streamlit */

                #MainMenu, footer, header {
                    visibility: hidden;
                }

                .block-container{
                    padding-top: 1.5rem !important
                }


                h1 {
                    font-family: 'Climate Crisis', sans-serif !important;
                    font-size: 2.5rem !important;
                    line-height: 0.9 !important;
                    margin-bottom: 0rem !important;
                    
                
                }

                h2 {
                    font-family: 'Climate Crisis', sans-serif !important;
                    font-size: 2rem !important;
                    line-height: 0.9 !important;
                    margin-bottom: 0rem !important;
                    color: black !important;
                
                }

                h3, h4, p {
                    font-family: 'Outfit', sans-serif;
                }

                div.stButton > button {
                    border-radius: 1.5rem !important;
                    background: #5865F2 !important;
                    color: white !important;
                    padding: 10px 20px !important;
                    border: none !important;
                    transition: transform 0.25s ease-in-out !important;
                }

                div.stButton > button:hover {
                    transform: translateY(-2px) scale(1.02);
                }

                div.stButton > button[kind="secondary"] {
                    background: #EB459E !important;
                }

                div.stButton > button[kind="tertiary"] {
                    background: black !important;
                }

                button:hover{
                    transform:scale(1.5)
                }
                

                </style>

    """,unsafe_allow_html=True)