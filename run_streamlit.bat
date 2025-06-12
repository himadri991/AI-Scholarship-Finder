@echo off
call venv\Scripts\activate
rem Delete the chroma_db directory if it exists
if exist chroma_db (
    rmdir /s /q chroma_db
)
streamlit run app.py 