import os
from model.query import Query
from services.pdfservice.awss3datasource.pdfsource_s3 import PdfSourceAwsS3
from langchain.document_loaders import S3DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

QUERY = """
        The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its data collected from all the documents. If the AI does not know the answer to a question, it truthfully says it does not know.

        The Data provides lots of information as following 
        1) Bill To: This section contains the member details like Name and contact number of the club.
            Example: 
            Bill gates
            Contact No.: 1234567890
        2)  Invoice Amount In Words : This section contains the Invoice Amount In Words.
            Example:
            Five Thousand Five Hundred Rupees only
        3) Terms and conditions:  This section contains Terms and conditions
        4) Invoice No : The number for the bill
        5) Date : this is Bill date in DD-MM-YYYY format. Example: 20-12-2022
        6) Amounts: This section contains Total Receipt , balance etc.
        8) Description: This section contains the Membership start date and end date .
            Example:
            1st November - 1st May : Membership start date is 1st of November and end date is 1st May
 
        AI Assistant will have to go through all the details and answer the Human accordingly.

        Human: {input}
        AI Assistant:
        """
PROMPT = PromptTemplate(
    input_variables=["input"], template=QUERY
)


class PdfPrompt:
    def __init__(self):
        print("loading pdf.....")
        self.PROMPT = PROMPT

    def test(self):
        return "Hello World"

    def get_answer_pdf_source(self, query: Query):

        s3_bucketname = os.getenv('S3_BUCKET')
        s3_prefix = os.getenv('S3_PREFIX')

        qa_prompt = self.PROMPT.format(input=query.question)
        pdfSourceAwsS3 = PdfSourceAwsS3(
            # bucket="bizzchatpdfsourcebucket", prefix="pdfdata/")
            bucket=s3_bucketname, prefix=s3_prefix+"/")

        docs = pdfSourceAwsS3.load_local_folder()
        # docs = pdfSourceAwsS3.load_local_folder()
        embeddings = OpenAIEmbeddings()
        vectordb = Chroma.from_documents(docs, embedding=embeddings)
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True)

        pdf_qa = ConversationalRetrievalChain.from_llm(
            OpenAI(temperature=0.8), vectordb.as_retriever(), memory=memory,
        )
        result = pdf_qa({"question": qa_prompt})
        print("Answer:", result["answer"])
        query.answer = result["answer"]
        return query
