import sys
import os
import src.readinglist
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('SECRET_ID')
database = os.getenv('DATABASE')
relation_database = os.getenv('RELATION_DATABASE')
pdf_path = os.getenv('PDF_PATH')

client = src.readinglist.NotionReadingListClient(database, relation_database, token, '2022-06-28')
client.create_page("Test", "RN", pdf_path)
