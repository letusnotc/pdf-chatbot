import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class MultimodalPDFProcessor:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_name = model_name

    async def process_pdf(self, file_path: str):
        """
        Uploads a PDF to Gemini using the new google-genai SDK.
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            print("ERROR: GOOGLE_API_KEY is missing or invalid in .env")
            raise ValueError("GOOGLE_API_KEY is not set. Please update the .env file in the server directory with a valid Gemini API key.")

        print(f"Uploading {file_path} to Gemini...")
        print(f"Using API Key (first 5 chars): {api_key[:5]}...")
        
        # In the google-genai SDK, the parameter is 'file' for the path string
        try:
            uploaded_file = self.client.files.upload(
                file=file_path,
                config={'mime_type': 'application/pdf'}
            )
            print(f"Upload to Gemini successful: {uploaded_file.name}")
            return uploaded_file
        except Exception as sdk_err:
            print(f"Gemini SDK Upload Error: {sdk_err}")
            raise sdk_err

    def extract_page(self, pdf_path: str, page_no: int):
        """
        Extracts a specific page from the PDF as an image (base64).
        """
        import fitz # PyMuPDF
        import base64
        
        doc = fitz.open(pdf_path)
        if page_no < 1 or page_no > len(doc):
            return None
        
        page = doc.load_page(page_no - 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # High res
        img_data = pix.tobytes("png")
        
        return base64.b64encode(img_data).decode('utf-8')

    def query_document(self, uploaded_file, query: str):
        """
        Queries the uploaded PDF multimodally.
        Note: The new SDK generate_content is synchronous by default in this context,
        or can be used with client.aio.models if async is needed.
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[uploaded_file, query]
        )
        return response.text
