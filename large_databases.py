import os
import re
from urllib.parse import quote_plus
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

class DatabaseConnector:
    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self.host = host
        self.database = database

    def connect(self):
        encoded_password = quote_plus(self.password)
        mysql_uri = f"mysql+mysqlconnector://{self.username}:{encoded_password}@{self.host}/{self.database}"
        return SQLDatabase.from_uri(mysql_uri)

class DocumentExtractor:
    def __init__(self, table_info):
        self.table_info = table_info

    def extract_documents(self):
        table_definitions = re.split(r'(?=CREATE TABLE)', self.table_info)
        return [Document(page_content=temp) for temp in table_definitions]

class LangChainSystem:
    def __init__(self):
        load_dotenv()

        self.database_connector = DatabaseConnector(
            os.getenv('username'),
            os.getenv('password'),
            os.getenv('host'),
            os.getenv('database')
        )

        self.database = self.database_connector.connect()

        self.document_extractor = DocumentExtractor(self.database.get_table_info())

        self.embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        self.vector_store = None
        self.retriever = None

    def create_vector_store(self):
        docs = self.document_extractor.extract_documents()
        self.vector_store = Chroma.from_documents(docs, self.embeddings_model)

    def create_retriever(self):
        if self.vector_store:
            self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})
        else:
            print("Vector store is not initialized.")

    def retrieve_documents(self, query):
        if self.retriever:
            return self.retriever.invoke(query)
        else:
            print("Retriever is not initialized.")

if __name__ == "__main__":
    langchain_system = LangChainSystem()
    langchain_system.create_vector_store()
    langchain_system.create_retriever()
    # retrieved_docs = langchain_system.retrieve_documents("Retrieve information of all transactions and customers.")
    # print(retrieved_docs)
