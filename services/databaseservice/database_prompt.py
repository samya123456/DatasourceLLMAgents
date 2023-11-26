from langchain.agents import AgentExecutor
from langchain.llms.openai import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent
from model.query import Query
import os
from dotenv import load_dotenv
load_dotenv()

QUERY = """
        Given an input question, first create a syntactically correct database query to run add your thought and return your answer. if there is any double
        quote in the question the run the query the donot use LIKE in the query , otherwise LIKE can be used.

        
        {question}
        """


class DatabaseBotPrompt:
    db_url_local = os.getenv('DB_URL')

    def __init__(self):
        print("loading database.....")
        db = SQLDatabase.from_uri(self.db_url_local)
        toolkit = SQLDatabaseToolkit(db=db,  llm=OpenAI(temperature=0))

        agent_executor = create_sql_agent(
            llm=OpenAI(temperature=0),
            toolkit=toolkit,
            verbose=True,
            top_k=100
        )
        self.agent_executor = agent_executor
        self.QUERY = QUERY

    def get_answer(self, query: Query):
        print("inside get answer.....")
        question = self.QUERY.format(question=query.question)
        query.answer = self.agent_executor.run(question)
        # query.answer = "This is from Api....Commenting out openai call"
        print("Answer is =", query.answer)
        return query
