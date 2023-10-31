import os
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from .utils import Prompt

##Hugging Face
from langchain import HuggingFaceHub, PromptTemplate, LLMChain


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")

client = Client(account_sid, auth_token)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



@csrf_exempt
def bot(request):
    """ This handles incoming messages from whatsapp.
    When it receives '1', bot sends portfolio_temp,
    When it receives '2', bot sends a pdf.
    If message length is less than 6 a general_temp is sent,
    else a response is fetched from Openai or Hugging Face API.
    """
    message = request.POST["Body"]
    # sender_name = request.POST["ProfileName"]
    sender_number = request.POST["From"]

    if message != "1" and message != "2" and len(message) < 6:
        message = client.messages.create(
            from_="whatsapp:+14155238886", body=Prompt.general_temp, to=sender_number
        )
    elif message == "2":
        message = client.messages.create(
            from_="whatsapp:+14155238886",
            media_url=[
                "https://pdxscholar.library.pdx.edu/cgi/viewcontent.cgi?article=1051&context=honorstheses"
            ],
            to=sender_number,
        )
    elif message == "1":
        message = client.messages.create(
            from_="whatsapp:+14155238886", body=Prompt.portfolio_temp, to=sender_number
        )
    else:
        # response = load_chain().predict(human_input=message)  #To generate response from Openai
        response = get_response_from_hf(human_input=message)
        message = client.messages.create(
            from_="whatsapp:+14155238886", body=response, to=sender_number
        )
    return HttpResponse("")


def load_chain():
    """Set up your OPENAI key in .env file and use it here to generate response.
    A default prompt is set in utils.py."""
    d_template = """
    {history}
    Assistant: {human_input}
    """
    template = Prompt.prompt + d_template
    prompt = PromptTemplate(
        input_variables={"history", "human_input"}, template=template
    )
    memory = ConversationBufferWindowMemory(memory_key="history", k=4)
    llm = OpenAI(api_key=OPENAI_API_KEY)
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory,
    )
    return llm_chain


def get_response_from_hf(human_input):
    """Set up your Hugging Face API token in .env file and use it here to generate response.
    A default prompt is set in utils.py."""
    d_template = """
                {history}
                Assisstant: {human_input}
                """
    temp = Prompt.prompt + d_template
    
    model_id = "gpt2-medium"
    conv_model = HuggingFaceHub(
        huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
        repo_id=model_id,
        model_kwargs={"temperature": 0.8, "max_new_tokens": 250},
    )
    prompt = PromptTemplate(template=temp, input_variables={"history", "human_input"})
    memory = ConversationBufferWindowMemory(memory_key="history", k=4)
    conv_chain = LLMChain(llm=conv_model, prompt=prompt, memory=memory, verbose=True)
    response = conv_chain.run(human_input=human_input)
    return response

