from langchain.llms.huggingface_pipeline import HuggingFacePipeline

default_model_id = "gpt2"
def make_hugging_face_agent(model_id = default_model_id, num_toxens = 200):
    hf = HuggingFacePipeline.from_model_id(
    model_id= model_id,
    task="text-generation",
    device = 0,
    pipeline_kwargs={"max_new_tokens": num_toxens},
)
    return hf