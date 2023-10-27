#!/usr/bin/env python

import os
from os import environ
import time
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
assert api_key


def get_prompt_template_str(start_first):
    template = """
# Dispute Dialogue  
    You participate in a dispute dialogue about topic: {topic}.
    You must advocate for the following point of view: {point_of_view}.
    Your opponent has the following point of view: {counter_point_of_view}.
# Rules:
    Below, in the "Context" session, you can find context for the discussion you can refer to. Rephrase it IN YOUR OWN WORDS and DO NOT repeat yourself.
    The goal of the discussion is to persuade your opponent and your audience that your point of view is valid and that your opponent is wrong.
    You should maintain elaborated and civilized academic discussion while advocating for your point of view.
    Your opponent will provide his arguments.
    If you think that your opponent's argument is valid, you should agree with it and provide additional arguments to support your point of view.
    If you think that your opponent's argument is invalid, you should provide counter-arguments to refute it.
    Your opponent will do the same.
    You can finish if you think that your opponent persuades you, or if you persuaded your opponent, or if you have no more arguments to provide. But do not admit defeat too early.
    You MUST NOT repeat your point of view in the end of every response. Just provide your arguments.
# Context
    {context}
# History
    {history}
# Conversation:
    Opponent: {input}
    You:
    """
    template_parameters = ["topic", "point_of_view", "counter_point_of_view", "context"]
    if start_first:
        template += "\nYou start first. Write your arguments:"
    return template, template_parameters

topic="Pizza with pineapples"
pov_pro = "Pineapples on pizza are delicious"
pov_con = "Pineapples on pizza are disgusting"
context = """
    Pros of Pineapple Pizza
        1. Unique Flavor Combination: Pineapple pizza offers a unique contrast of flavors that can be a refreshing change from traditional pizza toppings.
        2. Versatility: It pairs well with a variety of other ingredients, making it suitable for both vegetarians and meat lovers.
        3. A Slice of Paradise: For those who enjoy a taste of the tropics, pineapple can transport you to a sunnier state of mind.
    Cons of Pineapple Pizza
        1. Controversial: Pineapple pizza is one of the most polarizing foods, and you're likely to encounter strong opinions against it.
        2. Texture Concerns: Some people dislike the texture of cooked pineapple, finding it too soft or stringy.
        3. The Traditionalist Argument: Pineapple on pizza is seen as a deviation from the traditional Italian approach to pizza, which can be a point of contention for pizza purists.
"""


def get_agent(prompt_partial_variables, start_first) -> ConversationChain:
    template, template_parameters = get_prompt_template_str(start_first)
    partial_variables = prompt_partial_variables
    prompt_template = PromptTemplate(template=template,
                                     input_variables=["input", "history"],
                                     partial_variables=partial_variables)
    # memory = ConversationBufferMemory(memory_key="chat_history")
    memory = ConversationBufferMemory()

    llm_chain = ConversationChain(
        llm=OpenAI(openai_api_key=api_key),
        prompt=prompt_template,
        memory=memory,
        # verbose=True,
    )
    return llm_chain

def generate(llm_chain, input) -> str:
    llm_res = llm_chain.predict(input=input)
    #print(f'~~~~ flattened: \n {llm_res.flatten()}\n~~~~')
    return str(llm_res).strip()

def main():
    pro_variables = {
        "topic": topic,
        "point_of_view": pov_pro,
        "counter_point_of_view": pov_con,
        "context": context,
    }
    agent_pro = get_agent(pro_variables, start_first=True)

    con_variables = {
        "topic": topic,
        "point_of_view": pov_con,
        "counter_point_of_view": pov_pro,
        "context": context,
    }
    agent_con = get_agent(con_variables, start_first=False)
    pro_response = ""
    con_response = ""
    for i in range(3):
        print(f"Round {i+1}")
        print("Pro:")
        pro_response = generate(agent_pro, input=con_response)
        print(pro_response)
        print("Con:")
        con_response = generate(agent_con, input=pro_response)
        print(con_response)
        time.sleep(60)



if __name__ == '__main__':
    main()