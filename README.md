# PDF Chat App 📄

This is a simple application that lets you interact with your PDF documents by asking questions and getting answers. It's built to handle PDFs with both standard text and images, extracting all the content to create a powerful search and chat experience.

## Features

  - **Comprehensive Text Extraction**: The app reads all text from your PDF, including content from any images or scanned pages, ensuring no information is missed.
  - **Intelligent Search**: It processes the document's content and creates a fast, searchable index. This allows the application to quickly find the most relevant information for any question you ask.
  - **AI-Powered Answers**: Using a large language model, the app generates clear and concise answers based only on the information found within the PDF.

-----

## Getting Started

Follow these steps to set up and run the application on your local machine.

### Prerequisites

All necessary Python libraries are listed in the `requirements.txt` file. You can install them by running:

```bash
pip install -r requirements.txt
```

You must also have the **Tesseract OCR engine** installed on your system. This is a crucial component for reading text from images.

  - **Windows**: Download and run the installer from the official Tesseract GitHub page.
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`

### Setup

1.  **Obtain a Google API Key**: You will need an API key for the language model. Get one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

2.  **Configure Your Environment**: Create a new file named `.env` in the same directory as the application code and add your API key to it:

    ```ini
    GEMINI_API_KEY="your_api_key_here"
    ```

-----

## Usage

1.  **Run the App**: Open your terminal or command prompt, navigate to the directory where you saved the code, and execute the following command:

    ```bash
    streamlit run your_script_name.py
    ```

    A new tab will open in your web browser with the application interface.

2.  **Upload Your PDF**: Use the file uploader to select a PDF document from your computer.

3.  **Process and Chat**: Click the **"Process PDF"** button. Once the processing is complete, you can start typing your questions into the text box to get answers from the document.
