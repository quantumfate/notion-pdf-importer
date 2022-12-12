import sys
import os
import readinglist
import fileuploader
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('SECRET_ID')
database = os.getenv('DATABASE')
relation_database = os.getenv('RELATION_DATABASE')

client = readinglist.NotionReadingListClient(database, relation_database, token, '2022-06-28')
client.create_page("Test", "RN")

page_id = client.get_page_id_from_database("Test", database)
uploader = fileuploader.PdfUploader("/home/leonch/projects/notion/pdfimporter/RN_HBN_Kap_1_Die_Struktur_des_Internets.pdf", token)
uploader.upload_pdf()