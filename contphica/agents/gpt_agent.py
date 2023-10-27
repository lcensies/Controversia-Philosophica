from contphica.agents.debate_agent import DebateAgent
from os import environ

# from langchain.schema import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
# from gpt4_openai import GPT4OpenAI
from langchain.memory import ConversationSummaryBufferMemory

class GptDebateAgent(DebateAgent):

    def __init__(self, prompt: str = None):
        llm: BaseLanguageModel = ChatOpenAI()
        # llm = GPT4OpenAI(token=environ.get("OPENAPI_SESSION_TOKEN"))
        memory = ConversationSummaryBufferMemory(memory_key="chat_history",return_messages=True, llm=llm)
        super().__init__(llm=llm, memory=memory, prompt=prompt)