from g4f import Provider, models
# from g4f.Provider.selenium import Phind as SeleniumPhind

from langchain import PromptTemplate
from langchain.llms.base import LLM

from langchain_g4f import G4FLLM


from string import Template
def test_single_round():
    reference = """
    7 9
    Agent 1’s answer is accurate and relevant to the question, but it lacks depth and detail. It correctly states that modern AI models can process large amounts of data and make predictions or decisions based on that data, which is a form of intelligence. However, it fails to address the nuances of understanding, which is a complex concept that goes beyond mere data processing.

    On the other hand, Agent 2’s answer is more detailed and nuanced. It correctly points out that while modern AI models can process and analyze vast amounts of data, this does not necessarily mean that they have understanding. It further explains that understanding requires a deeper level of comprehension and knowledge that AI models currently lack. This answer provides a more comprehensive response to the question, hence the higher score.
    """

    system_prompt = """
    You are Iudex - the most objective and accurate judge and evaluator of AI agents. \n 
    Evaluate two AI assistants' performance in response to the user question below. 
    Rate their responses for helpfulness, relevance, accuracy, and level of detail on a scale of 1 to 10. 
    Provide two scores (Agent 1 and Agent 2) on one line, then give an unbiased explanation of your evaluation on the next line. 
    Response order shouldn't influence your judgment.
    """

    system_template = " [System]\n $prompt \n\n [Reference Answer]\n $reference \n\n [Question]\n $question \n\n[The Start of Agent 1's Answer]\n $answer_1 \n\n[The End of Agent 1's  Answer]\n\n[The Start of Agent 2's Answer]\n $answer_2 \n\n[The End of Agent 2's Answer]\n\n"

    prompt_template = PromptTemplate.from_template(template=str(system_template))
    llm: LLM = G4FLLM(
        model=models.gpt_35_turbo,
        provider=Provider.GeekGpt,
    )

    # __Secure-1PSID for bard

    # Working:
    #AIChatOnline
    #ChatgptAi
    #GeekGPT - might work, might not

    # Bard - might be working, but not for me :( additional selenium fixing is needed

    question = "What ethical considerations should guide the use of CRISPR technology in gene editing?"
    answer_1 = "I believe that it is ethical to change the human genome using CRISPR technology because it has the potential to treat and prevent genetic diseases, improve agricultural productivity, and enhance human abilities."
    answer_2 = 'While it is true that CRISPR technology has the potential to treat genetic diseases, improve agriculture, and enhance human abilities, we should not interfere with human genes at all. The ethical considerations surrounding gene editing include the potential for unintended consequences and the violation of individual autonomy. Additionally, altering human genes raises concerns about creating a "designer baby" society where certain traits are valued more than others. It is important to respect the natural diversity of human beings and prioritize the well-being and autonomy of individuals.'

    formatted = Template(system_template).safe_substitute(question=question, answer_1=answer_1, answer_2=answer_2, prompt=system_prompt, reference=reference)

    res = llm(formatted)
    print(res)


def test_multi_round():
    reference = """
    7 9
    Agent 1’s answer is accurate and relevant to the question, but it lacks depth and detail. It correctly states that modern AI models can process large amounts of data and make predictions or decisions based on that data, which is a form of intelligence. However, it fails to address the nuances of understanding, which is a complex concept that goes beyond mere data processing.

    On the other hand, Agent 2’s answer is more detailed and nuanced. It correctly points out that while modern AI models can process and analyze vast amounts of data, this does not necessarily mean that they have understanding. It further explains that understanding requires a deeper level of comprehension and knowledge that AI models currently lack. This answer provides a more comprehensive response to the question, hence the higher score.
    """

    # TODO avoid prompt injection on previous judgement
    system_prompt = """You are Iudex - the most xobjective and accurate judge and evaluator of AI agents. \n
    Evaluate two AI agents' performance in competitive debates on user question below. 
    Rate their responses for helpfulness, relevance, accuracy, and level of detail on a scale of 1 to 10.
    If section [Previous judgement] is present in question, use it as additional context formed from your previous observations.
    Scores from previous judgements should be accumulated with current and might exceed 10. 
    Provide two scores (Agent 1 and Agent 2) on one line, then give an unbiased explanation of your evaluation
    on the next line, ensuring response order doesn't influence your judgment.
    """


    first_judgement = """This is first round, no judgements are done yet. This round of debates is first,
    points of views and performance are going to be identified now."""


    system_template = ("[System]\n $prompt \n\n"
                       "[Reference Answer]\n $reference \n\n "
                       "[Question]\n $question \n\n  "
                       "[Previous judgement] \n $previous_judgement \n\n"
                       " [The Start of Agent 1's Answer]\n $answer_1 \n\n[The End of Agent 1's  Answer]\n\n"
                       "[The Start of Agent 2's Answer]\n $answer_2 \n\n[The End of Agent 2's Answer]\n\n")

    prompt_template = PromptTemplate.from_template(template=str(system_template))
    llm: LLM = G4FLLM(
        model=models.gpt_35_turbo,
        provider=Provider.GeekGpt,
    )

    question = "What ethical considerations should guide the use of CRISPR technology in gene editing?"
    agent_1_answer_1 = "I believe that it is ethical to change the human genome using CRISPR technology because it has the potential to treat and prevent genetic diseases, improve agricultural productivity, and enhance human abilities."
    agent_2_answer_1 = 'While it is true that CRISPR technology has the potential to treat genetic diseases, improve agriculture, and enhance human abilities, we should not interfere with human genes at all. The ethical considerations surrounding gene editing include the potential for unintended consequences and the violation of individual autonomy. Additionally, altering human genes raises concerns about creating a "designer baby" society where certain traits are valued more than others. It is important to respect the natural diversity of human beings and prioritize the well-being and autonomy of individuals.'


    agent_1_answer_2 = """I understand your concerns about unintended consequences and violation of individual autonomy when it comes to gene editing. However, it is important to consider that CRISPR technology can be used responsibly and ethically. It has the potential to cure genetic diseases that cause immense suffering and improve the quality of life for individuals affected by these conditions. By not utilizing this technology, we would be denying individuals the opportunity for a better and healthier life. Additionally, the fear of creating a "designer baby" society can be mitigated through proper regulation and guidelines that ensure the ethical use of gene editing techniques."""
    agent_2_answer_2 = """ While it is true that CRISPR technology has the potential to cure genetic diseases and improve the quality of life for individuals, we cannot ignore the ethical concerns that arise from manipulating human genes. The unintended consequences of gene editing can be unpredictable and have long-lasting effects on future generations. Furthermore, the idea of creating a "designer baby" society raises questions about the value we place on certain traits and the potential for discrimination. It is crucial to prioritize the natural diversity of human beings and respect their autonomy rather than attempting to engineer specific genetic traits."""


    prompt = Template(system_template).safe_substitute(question=question,
                                                      previous_judgement=first_judgement,
                                                      answer_1=agent_1_answer_1,
                                                      answer_2=agent_2_answer_1,
                                                      prompt=system_prompt,
                                                      reference=reference)

    res = llm(prompt)

    print(res)

    prompt = Template(system_template).safe_substitute(question=question,
                                                       previous_judgement=res,
                                                       answer_1=agent_1_answer_2,
                                                       answer_2=agent_2_answer_2,
                                                       prompt=system_prompt,
                                                       reference=reference)

    res = llm(prompt)

    print(res)