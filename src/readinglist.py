from notion_client import Client
from datetime import datetime
import base64
import os
from tempfile import TemporaryDirectory
from pathlib import Path
from typing import List
from notion_client import Client
import notion_client
import pdf2image


class NotionReadingListClient:
    def __init__(self, database_id, relation_database_id, token, set_notion_version) -> None:
        self.token = token
        self.database_id = database_id
        self.relation_database_id = relation_database_id
        self.notion = Client(auth=token, notion_version=set_notion_version)
        self.parent = {
            "database_id": self.database_id
        }
        self.relation_parent = {
            "database_id": self.relation_database_id
        }

    def get_page_id_from_database(self, page_name, relation_db_id) -> str:
        results = self.notion.databases.query(
            database_id=relation_db_id,
            filter={
                "property": "Name",
                "rich_text": {
                    "contains": page_name
                }
            }
        ).get("results")
        if results:
            # Get the page ID of the first result
            page_id = results[0]["id"]
            print(f"Page ID: {page_id}")
        else:
            print(f"No pages found with name '{page_name}'")
        return page_id

    def create_page(self, name, course, pdf_file_path):

        # Split the pdf into individual pages
        pages = self.pdf_to_images(pdf_file_path)
        children = []

        for page in pages:
            children.append(self.get_page_children(page))
        # Create the page in Notion with the images as children
        page = self.notion.pages.create(
            parent=self.parent,
            properties=self.get_page_properties(name, course),
            children=children,
        )

        if page:
            print("Page created successfully!")
        else:
            print("Error creating page")


    def get_page_properties(self, name, course):
        return {
                "Name": {
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": name
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": datetime.now().astimezone().isoformat()
                    }
                },
                "Course": {
                    "relation": [
                        {
                            "id": self.get_page_id_from_database(course, self.relation_database_id)
                        }
                    ]
                }
            }

    def pdf_to_images(self, pdf_file_path: str) -> List[str]:
        # Use TemporaryDirectory to create and manage a temporary directory
        with TemporaryDirectory() as temp_dir:
            # Use pdf2image to convert the PDF to images
            images = pdf2image.convert_from_path(pdf_file_path)

            # Save the images to the temp directory
            image_paths = []
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f"page_{i}.jpg")
                image.save(image_path, "JPEG")
                image_paths.append(image_path)

            return image_paths

    def get_page_children(self, image_path):
        # Upload the image and get the URL of the uploaded image
        uploaded_image_url = self.notion.options.upload_file(image_path)
        # Map the list of pages (image files) to a list of Notion blocks
        children = {
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": uploaded_image_url,
                    },
                },
            }
    
        return children