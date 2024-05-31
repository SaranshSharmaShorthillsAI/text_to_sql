from langchain import OpenAI, SQLDatabase
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
import mysql.connector
from large_databases import LangChainSystem

class CventDemo:
    def __init__(self):
        load_dotenv()

        try:
            azure_openai_endpoint = os.getenv('OPENAI_API_BASE')
            os.environ["OPENAI_API_TYPE"] = os.getenv('OPENAI_API_TYPE')
            os.environ["OPENAI_API_VERSION"] = os.getenv('OPENAI_API_VERSION')
            os.environ["OPENAI_API_BASE"] = azure_openai_endpoint[:-1] if azure_openai_endpoint.endswith('/') else azure_openai_endpoint
            os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
            self.deployment_name = os.getenv('DEPLOYMENT_NAME')

            self.llm = AzureChatOpenAI(
                model_kwargs={
                    "headers": {"User-Id": os.getenv("USER_ID")}
                },
                deployment_name=self.deployment_name,
                model=os.getenv('MODEL_NAME'),
                temperature=0.0,
            )

            self.username= os.getenv('username')
            self.password=os.getenv('password')
            self.host= os.getenv('host')
            self.database=os.getenv('database')
            self.encoded_password=quote_plus(self.password)

            self.mysql_uri = f"mysql+mysqlconnector://{self.username}:{self.encoded_password}@{self.host}/{self.database}"
            self.db = SQLDatabase.from_uri(self.mysql_uri)

           
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                print("Connected to MySQL database")

            

        except Exception as e:
            print("An error occurred during initialization:", str(e))
            exit()

    def run_query(self, question):
        try:
            template=""""Write a SQL query for the given task by following the listed steps:

                        Task: {question}
                    
                        Follow these steps:

                        First, create your definition of the problem. And the understood meaning.
                        Then, prepare the logic that you will be using to solve the task using SQL. Do not make any assumption for any new column to solve the given task. If there is no direct way find the indirect way from existing tables and columns to find the data. Think step by step and build the logic. The logic should be built based on the given column names of all existing tables. Once the logic is built, list the steps you will follow to execute your logic.
                        Mention the tables you will be using to write the query. If there are multiple tables. make sure you understand how the tables are related with their following columns
                        Among the listed tables, list the names of columns you will use to execute your logic.
                        Give the final SQL query to solve the task.
                       

                        {table_info}.

                        AI resp (with SQL query):"

                        """
            
            prompt = ChatPromptTemplate.from_template(template=template)
            chain = prompt | self.llm
            langchain_system = LangChainSystem()
            langchain_system.create_vector_store()
            langchain_system.create_retriever()
            retrieved_docs = langchain_system.retrieve_documents(query=question)
            table_info=""

            for retrived_doc in retrieved_docs:
                table_info=table_info+retrived_doc.page_content+"\n"
                
        
            response=chain.invoke({"question":question, "table_info":table_info})
            
    
            index_sql_query = response.content.find("SQL query:")

            if index_sql_query != -1:
                sql_query = response.content[index_sql_query + len("SQL query:"):]
                print("Extracted SQL query:")
                print(sql_query.strip())
               
            else:
                print("SQL query not found.") 
                    

            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            headers = [i[0] for i in cursor.description]
            
            return (self.db.run(sql_query), sql_query,headers)
        
        except Exception as e:
            print("An error occurred during query execution:", str(e))
            return None,None

if __name__ == "__main__":
    try:
        demo = CventDemo()
        question = input("Enter your query: ")
        response = demo.run_query(question)
        if response:
            print(f"RESPONSE ::::::  {response}")
        else:
            print("Query execution failed.")
    except KeyboardInterrupt:
        print("\nExiting...")

