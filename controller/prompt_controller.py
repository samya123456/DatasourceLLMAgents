
from fastapi import APIRouter
from services.pdfservice.pdf_promt import PdfPrompt
from services.databaseservice.database_prompt import DatabaseBotPrompt
from model.query import Query


router = APIRouter(prefix='/prompt')


class PromptController():
    def __init__(self):
        print("loading PromptController.....")
        self.router = router

    @router.post("/db", response_model=Query)
    async def promptQueryDatabase(query: Query):
        print(query)
        chatbot = DatabaseBotPrompt()
        query = chatbot.get_answer(query)
        return query

    @router.post(
        "/pdf", summary="pdf read from s3 storage",
        response_model=Query
    )
    async def promptQueryPdf(query: Query):
        pdfPrompt = PdfPrompt()
        return pdfPrompt.get_answer_pdf_source(query)
