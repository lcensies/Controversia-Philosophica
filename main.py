from contphica.debate import Debate
import os 

PROMPTS_DIR = "prompts"


def fetch_last_prompt() -> str:

    prompts = [f for f in os.listdir(PROMPTS_DIR) if os.path.isfile(os.path.join(PROMPTS_DIR, f))]
    prompts.sort(key=lambda x: os.path.getmtime(os.path.join(PROMPTS_DIR, x)), reverse=True)
    last_prompt_file: str = prompts[0]

    last_prompt: str = None
    try:
        with open(os.path.join(PROMPTS_DIR, last_prompt_file), "r") as f:
            last_prompt = f.read()
    except FileNotFoundError:
        pass

    return last_prompt

if __name__ == "__main__":
    question: str = "Is it possible to create an AI LLM that is completely free from decision fallacies, and what challenges exist in achieving this goal?"

    Debate(question) \
        .with_prompt(fetch_last_prompt()) \
        .with_limit(2) \
        .with_gpt_agents() \
        .with_names("Socratease", "Confuncius").start()
    
    