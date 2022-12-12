from notion_client import Client
from datetime import datetime


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

    def create_page(self, name, course):
        page = self.notion.pages.create(
            parent=self.parent,
            properties={
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
        )

        if page:
            print("Page created successfully!")
        else:
            print("Error creating page")
