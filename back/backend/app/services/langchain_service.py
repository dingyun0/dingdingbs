

from langchain_openai import ChatOpenAI, OpenAI
from matplotlib.pylab import cla

from backend.app.core.conf import Settings


class LangChainService:
    chatModel: ChatOpenAI

    def __init__(self):
        self.openai = OpenAI(
            open_api_key=Settings.OPENAI_API_KEY,
            model=Settings.OPENAI_BASE_MODEL,
            base_url=Settings.OPENAI_BASE_URL,
            temperature=0.7,
            streaming=True,
        )
