# GAI Project: Controversia-Philosophica

Welcome to the Controversia Philosophica repository!

This project aims to improve reasoning and question-answering capabilities of language models through a dispute between two agents based on user’s prompt.

Our proposal is based on [1], where authors propose multi-agent scenario which was shown to improve overall performance on complex problem-solving tasks. We propose a scheme where two LLM agents debate over a user’s question, giving arguments in favor of and against a given topic according to their roles, performing additional verification of each other’s responses with use of background context from a trusted source.

# 🚀 Getting Started

1. Clone this repository to your local machine:
    
    ```bash
    git clone -b langchain git@github.com:lcensies/Controversia-Philosophica.git
    ```

2. Install requirements:

   ```
   pip3 install -r requirements.txt
   ```
    
3. Open and run `example.ipynb` which contains a comprehensive example. 

# Usage

From the user perspective, the main entrypoint to Controversia Philosophica is `contphica.debate.Debate` class.
Users need to provide following parameters:
* Dispute topics
* Agents' opinions
* Agents' names (for user convenience)
* Agents' backend (currently OpenAI only)
* Initial prompt for agents (you can resort to a quite reasonable built-in `"dispute_default"`) 
* Background knowledge agents can refer to

`Debate` is set up in a Builder-like fashion:
```python
    debate = (Debate(topic)
              .with_knowledge(dispute_knowledge)
              .with_opinions(pro=opinion_pro, con=opinion_con)
              .with_prompt("dispute_default")
              .with_gpt_agents(token=openai_token)
              .with_limit(2)
              .with_debater_names("Pineapple Pizza Lover", "Pineapple Pizza Hater"))
```

# Overall architecture

By now we have finished a proof-of-concept stage, employing OpenAI generative models to conduct a conversation between two models.
Our final goal is employ LLaMa model fine-tuned for argumented disputes.
To be able to quickly switch between models in plug-and-play fashion, we have implemented an object-oriented hierarchy of classes corresponding to certain language model aspects.
The implementation is based on `langchain` framework for creating and interacting with Large Language Models.
Our goal is to make transition to LLaMa as seamless as possible.

# Repository structure

## `contphica/`

This folder contains the classes for debating agent and debate control. All current types of agent implementations can be found in the corresponding folder.

## `prompts/`

This repo contains different initial prompts to prepare the agents.
WARNING! this promts are not meant to start a specific discussion or introduce a context to the main topic. Their purpose to initiate agents in such way that they hold a meaningful conversation.

# References

1. [“Improving Factuality and](arXiv preprint arXiv:2305.14325) [Reasoning](https://arxiv.org/abs/2305.14325) [in Language Models through Multiagent Debate”](arXiv preprint arXiv:2305.14325) by Du, Yilun and Li, Shuang and Torralba, Antonio and Tenenbaum, Joshua B and Mordatch, Igor.
