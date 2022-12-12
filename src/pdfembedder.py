import base64
from notion_client import Client

class PdfEmbedder:
    def __init__(self, pdf_file_path, notion_page_id, token) -> None:
        self.pdf_file_path = pdf_file_path
        self.notion_page_id = notion_page_id
        self.token = token
        self.notion = Client(auth=token)
        self.parent = {
            "page_id": self.notion_page_id
        }

    def embed_pdf(self):
        with open(self.pdf_file_path, "rb") as pdf_file:
            pdf_base64 = base64.b64encode(pdf_file.read()).decode()

        page = self.notion.pages.update(
            parent=self.parent,
            properties={
                ""
            }
        )