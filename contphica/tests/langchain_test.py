from os.path import join, dirname, pardir


import openai
import os
import IPython
from langchain.llms import OpenAI
from dotenv import load_dotenv
load_dotenv()


dotenv_path = join(dirname(__file__), pardir, '.env')
load_dotenv(dotenv_path)

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.prompts import PromptTemplate, MessagesPlaceholder
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# TODO: test summary buffer memory vs buffer memory for arguments evaluation
from langchain.memory import ConversationSummaryBufferMemory

llm = ChatOpenAI()


# Prompt 
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

# Notice that `"chat_history"` aligns with the MessagesPlaceholder name
memory = ConversationSummaryBufferMemory(memory_key="chat_history",return_messages=True, llm=llm)
conversation = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory
)

res = conversation({"question": "hi"})

print(res)


res2 = conversation({"question": "tell me about yourself"})
