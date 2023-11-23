from contphica.agents.debate_agent import DebateAgent
from contphica.agents.hf_initiator import hugging_face_initiator
from os import environ

# from langchain.schema import BaseLanguageModel
from langchain.memory import ConversationSummaryBufferMemory


model_id = "DebateLabKIT/cript-medium"

class CriptDebateAgent(DebateAgent):

    def __init__(self, prompt: str = None):
        llm = hugging_face_initiator(model_id = model_id)
        # llm = GPT4OpenAI(token=environ.get("OPENAPI_SESSION_TOKEN"))
        memory = ConversationSummaryBufferMemory(memory_key="chat_history",return_messages=True, llm=llm)
        super().__init__(llm=llm, memory=memory, prompt=prompt)