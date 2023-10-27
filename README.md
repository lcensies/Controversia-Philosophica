# Controversia philosophica

Welcome to the Controversia philosophica repository! This project aim is to create a discussion between two agents based on user’s prompt so the resulting conversation give a better answers to the initial topic question. 

# 🚀 Getting Started

1. Clone this repository to your local machine:
    
    ```bash
    git clone <https://github.com/lcensies/Controversia-Philosophica/tree/langchain>
    
    ```
    
2. Import Example.ipynb into Jupyter Notebook or Google Colab.
3. [add OPENAI_API_KEY to your environment](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)
4. Run all cells

# Repository structure

## Contphica

This folder contains the base class for debating agent, the base class for controlling the debates. All current types of agent implementations can be found in the corresponding folder.

## Prompts

This repo contains different initial prompts to prepare the agents. In order to run your own prompt using [main.py](http://main.py) file - save a .txt file there containing the prompt to prepare the agents.

WARNING! this promts are not meant to start a specific discussion or introduce a context to the main topic. Their purpose to initiate agents in such way that they hold a meaningful conversation.

# How to run your own discussions

To change the initial topic of discussion - change the question.txt file with the text that you would like to use as the initial prompt for debates.

# Project Aim

Our proposal is based on [1], where authors propose multi-agent scenario which was shown to improve overall performance on complex problem-solving tasks. We propose a scheme where two LLM agents debate over a user’s question, giving arguments in favor of and against a given topic according to their roles, performing additional verification of each other’s responses with use of background context from a trusted source.

Study [2] shows that extracting k key sentences from the sources for a context gives better result than just using opens_source LLMs to summarize the information. Therefore, the next stage for upgrading our project is to implement this method and pass the context to the agent, so that the speed of discussion is increased and the context given to the debates is better.

# References

1. [“Improving Factuality and](arXiv preprint arXiv:2305.14325) [Reasoning](https://arxiv.org/abs/2305.14325) [in Language Models through Multiagent Debate”](arXiv preprint arXiv:2305.14325) by Du, Yilun and Li, Shuang and Torralba, Antonio and Tenenbaum, Joshua B and Mordatch, Igor.