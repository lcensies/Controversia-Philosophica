from contphica.debate.debate import Debate
import os

# this replicates the example from the example.ipynb notebook

openai_token = os.getenv("OPENAI_API_TOKEN")

topic = "Pizza with pineapples"
opinion_pro = "Pineapples on pizza are delicious"
opinion_con = "Pineapples on pizza are disgusting"
dispute_knowledge = """
Pros of Pineapple Pizza
    1. Unique Flavor Combination: Pineapple pizza offers a unique contrast of flavors that can be a refreshing change from traditional pizza toppings.
    2. Versatility: It pairs well with a variety of other ingredients, making it suitable for both vegetarians and meat lovers.
    3. A Slice of Paradise: For those who enjoy a taste of the tropics, pineapple can transport you to a sunnier state of mind.
Cons of Pineapple Pizza
    1. Controversial: Pineapple pizza is one of the most polarizing foods, and you're likely to encounter strong opinions against it.
    2. Texture Concerns: Some people dislike the texture of cooked pineapple, finding it too soft or stringy.
    3. The Traditionalist Argument: Pineapple on pizza is seen as a deviation from the traditional Italian approach to pizza, which can be a point of contention for pizza purists.
"""

def main():
    debate = (Debate(topic)
              .with_knowledge(dispute_knowledge)
              .with_opinions(pro=opinion_pro, con=opinion_con)
              .with_prompt("dispute_default")
              .with_gpt_agents(token=openai_token)
              .with_limit(2)
              .with_debater_names("Pineapple Pizza Lover", "Pineapple Pizza Hater"))
    debate.start()

if __name__ == "__main__":
    main()