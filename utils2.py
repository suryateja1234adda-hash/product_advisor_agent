from langchain.chat_models import init_chat_model, BaseChatModel
from dotenv import load_dotenv
import os


def get_model(model:str,**args:dict)->BaseChatModel:
    return init_chat_model(
        model = model,
        **args
    )

if __name__ == '__main__':
    load_dotenv()
    llm = get_model(
        model = os.getenv('MODEL_NAME','gemini-3.5-flash-lite'),
        model_provider = 'google-genai',
        project = os.getenv('PROJECT_ID')
    )

    result = llm.invoke(
        'What is the capital of France ?'
    )

    result.pretty_print()
