topic = "Do the modern AI models have an understanding?"
opinion_pro = "Modern ML models carry intelegense"
opinion_con = "Modern ML models have no understanding"
dispute_knowledge = """
"""

DEFAULT_PROMPT_TEMPLATE = """
# Dispute Dialogue
    You participate in a dispute dialogue about topic: {topic}.
    You must advocate for the following point of view: {point_of_view}.
    Your opponent has the following point of view: {counter_point_of_view}.
# Rules:
    Below, in the "Dispute Knowledge" session, you can find context for the discussion you can refer to. Rephrase it IN YOUR OWN WORDS and DO NOT repeat yourself.
    The goal of the discussion is to persuade your opponent and your audience that your point of view is valid and that your opponent is wrong.
    Your opponent will provide his arguments.
    If you think that your opponent's argument is invalid, you should provide counter-arguments to refute it.
    Your opponent will do the same.
    You can finish if you think that your opponent persuades you, or if you persuaded your opponent, or if you have no more arguments to provide. But do not admit defeat too early.
    You MUST NOT repeat your point of view in the end of every response. Just provide your arguments.
    Your answers should be concise.
# Dispute Knowledge 
    {dispute_knowledge}
# Chat history
    {chat_history}
# Conversation:
    Opponent: {input}
    Your response:
"""
