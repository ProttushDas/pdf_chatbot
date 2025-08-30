import os
import asyncio
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

def read_pdf_with_images(pdf_file):
    """Read all text from PDF including text in images"""
    all_text = ""
    
    # Open the PDF
    pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        
        # Get regular text
        text = page.get_text()
        all_text += text + "\n"
        
        # Get images and read text from them
        images = page.get_images()
        
        for img in images:
            try:
                # Extract image
                xref = img[0]
                pix = fitz.Pixmap(pdf, xref)
                
                # Convert to PIL image and read text
                if pix.n - pix.alpha < 4:
                    img_data = pix.tobytes("ppm")
                    image = Image.open(BytesIO(img_data))
                    image_text = pytesseract.image_to_string(image)
                    
                    if image_text.strip():
                        all_text += f"\n[Image text]: {image_text}\n"
                
                pix = None
            except:
                continue
    
    pdf.close()
    return all_text

def split_text(text):
    """Split text into chunks"""
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_text(text)

def create_search_index(chunks, api_key):
    """Create searchable index"""
    # Fix async issue
    try:
        asyncio.get_event_loop()
    except:
        asyncio.set_event_loop(asyncio.new_event_loop())
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    
    return FAISS.from_texts(chunks, embeddings)

def main():
    load_dotenv()
    
    st.set_page_config(page_title="PDF Chat", page_icon="📄")
    st.title("Chat with PDF 📄")
    st.write("Upload a PDF and ask questions!")
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Add GEMINI_API_KEY to your .env file")
        return
    
    # Upload PDF
    pdf_file = st.file_uploader("Upload PDF", type="pdf")
    
    if pdf_file:
        # Process PDF
        if st.button("Process PDF"):
            with st.spinner("Reading PDF and images..."):
                # Read all text
                text = read_pdf_with_images(pdf_file)
                
                if not text.strip():
                    st.error("No text found in PDF")
                    return
                
                # Split into chunks
                chunks = split_text(text)
                st.write(f"Found {len(chunks)} text sections")
                
                # Create search index
                search_index = create_search_index(chunks, api_key)
                st.session_state.search_index = search_index
                
                st.success("PDF ready! Ask questions below.")
        
        # Chat
        if "search_index" in st.session_state:
            question = st.text_input("Ask a question:")
            
            if question:
                with st.spinner("Finding answer..."):
                    # Search for relevant text
                    docs = st.session_state.search_index.similarity_search(question, k=3)
                    context = "\n\n".join([doc.page_content for doc in docs])
                    
                    # Ask AI
                    prompt = f"""
Answer the question using only this text from the PDF:

{context}

Question: {question}
Answer:"""
                    
                    llm = ChatGoogleGenerativeAI(
                        model="gemini-1.5-flash",
                        google_api_key=api_key,
                        temperature=0.1
                    )
                    
                    answer = llm.predict(prompt)
                    st.write("**Answer:**")
                    st.write(answer)

if __name__ == "__main__":
    main()