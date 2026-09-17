from langchain.chat_models import BaseChatModel,init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_aws import ChatBedrockConverse
from dotenv import load_dotenv
import os



def get_model(model:str, **args:dict) -> BaseChatModel:
    return init_chat_model(
        model=model,
        **args
    )

def get_model_from_gcp()->ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=os.getenv('MODEL_NAME','gemini-3.5-flash-lite'),
        project = os.getenv('PROJECT_ID')
    )

def get_model_from_aws()->ChatBedrockConverse:
    return ChatBedrockConverse(
        model=os.getenv('AWS_MODEL_NAME','amazon.nova-micro-v1:0'),
        location = os.getenv('AWS_REGION')
    )


if __name__ == '__main__':
    load_dotenv()
    # llm = get_model(
    #     model=os.getenv('MODEL_NAME','gemini-3.5-flash-lite'),
    #     model_provider = 'google-genai',
    #     project = os.getenv('PROJECT_ID')
    # )

    llm = get_model_from_aws()
    result = llm.invoke('What is the capital of France ?')
    result.pretty_print()
