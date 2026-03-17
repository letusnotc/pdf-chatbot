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
        print(f"Uploading {file_path} to Gemini...")
        with open(file_path, 'rb') as f:
            uploaded_file = self.client.files.upload(
                file=f,
                config={'mime_type': 'application/pdf'}
            )
        return uploaded_file

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
