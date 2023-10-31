from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from .forms import PromptForm
from .models import ChatGptBot, UserPromptTemplate, UsersGeneratedImages
from .utils import DefaultTemplate

import requests
import os
import openai
from playsound import playsound

from PIL import Image
import io
from django.core.files.images import ImageFile
import json

## Imports for chatbot
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory


##Hugging Face
from langchain import HuggingFaceHub, PromptTemplate, LLMChain


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")


class Home(View):
    def get(self, request):
        """If user is authenticated directs to home page with previus chat history,
        else directed to sign-up page."""
        if request.user.is_authenticated:
            get_history = ChatGptBot.objects.filter(user=request.user)
            if "bot_name" in request.session:
                return render(request, "home.html", {"history": get_history})
            # Set bot name to default if not in session
            return render(
                request,
                "home.html",
                {"history": get_history, "bot_name": DefaultTemplate.bot_name},
            )
        else:
            messages.info(request, "Sign-up or Login required.")
            return redirect("sign-up")

    def post(self, request):
        """If bot is in session the function uses that bot name,
        else we use default bot_name. If you want to get response from OPENAI,
        uncomment the response using load_chain(). If you do not have access to OPENAI KEY,
        you can use the free API from hugging face to generate response. Only use one response
        at a time."""
        if "bot_name" in request.session:
            bot_name = request.session["bot_name"]
        else:
            bot_name = DefaultTemplate.bot_name
        user_input = request.POST.get('user_input')
        # response = load_chain(request).predict(human_input=user_input) # Requires OPENAI KEY
        response = get_response_from_hf(request, user_input)  # Hugging Face
        ChatGptBot.objects.create(
            user=request.user,
            messageInput=user_input,
            bot_response=response,
            bot_name=bot_name,
        )
        context = {"response": response, "user_input": user_input, "name": bot_name}
        return JsonResponse(context)


def get_response_from_hf(request, u_input):
    """Set up your Hugging Face API token in .env file and use it here to generate response.
    If a user_template is already set in session , that is used for generating response,
    else a default template set up in utils.py is used. The returned bot response is saved in model."""
    if "user_template" in request.session:
        user_template = request.session["user_template"]
        bot_name = request.session["bot_name"]
    else:
        user_template = DefaultTemplate.template
        bot_name = DefaultTemplate.bot_name
    d_template = """
                {history}
                Boyfriend: {human_input}
                """
    temp = user_template + d_template + f"{bot_name}: "
    model_id = "gpt2-medium"
    conv_model = HuggingFaceHub(
        huggingfacehub_api_token=HF_TOKEN, 
        repo_id=model_id,
        model_kwargs={"temperature": 0.8, "max_new_tokens": 200},
    )
    prompt = PromptTemplate(template=temp, input_variables={"history", "human_input"})
    memory = ConversationBufferWindowMemory(memory_key="history", k=4)
    conv_chain = LLMChain(llm=conv_model, prompt=prompt, memory=memory, verbose=True)
    response = conv_chain.run(human_input=u_input)
    return response


def load_chain(request):
    """Set up your OpenAI Key in .env file and use it here to generate response.
    If a user_template is already set in session , that is used for generating response,
    else a default template set up in utils.py is used. The returned bot response is saved in model."""
    if "user_template" in request.session:
        user_template = request.session["user_template"]
        bot_name = request.session["bot_name"]
    else:
        user_template = DefaultTemplate.template
        bot_name = DefaultTemplate.bot_name

    d_template = """
    {history}
    Boyfriend: {human_input}
    """
    template = user_template + d_template + f"{bot_name} :"
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


def get_voicemessage(message):
    """ To play response as a voice message, set up ELEVEN_LABS_API_KEY in .env file."""
    payload = {
        "text": message,
        "model_id": "eleven_multilingual_v2",
    }
    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/KrEZECov9cOksj4FqRsO?optimize_streaming_latency=0&output_format=mp3_44100_128",
        json=payload,
        headers=headers,
    )
    if response.status_code == 200 and response.content:
        with open("audio.mp3", "wb") as f:
            f.write(response.content)
        playsound("audio.mp3")
        return response.content


class CreateEditTemplate(View):
    """This is for Adding and Editing prompt Templates.
    Errors will be displayed on Modal itself."""
    def post(self, request, id=None):
        if id is not None:
            obj = UserPromptTemplate.objects.filter(id=id).first()
            form = PromptForm(request.POST, instance=obj)
            if form.is_valid():
                user = form.save(commit=False)
                ChatGptBot.objects.filter(
                    user=request.user, bot_name=obj.bot_name
                ).update(bot_name=request.POST["bot_name"])

                user.user = request.user
                user.save()
                return JsonResponse({})
            else:
                return JsonResponse({"errors": form.errors})
        else:
            form = PromptForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.user = request.user
                user.save()
                return JsonResponse({})
            else:
                return JsonResponse({"errors": form.errors})


def get_prompt_data(request, id=None):
    """On click of edit button prompt id is sent here through ajax.
    This sends the previous prompt data to edit prompt modal."""
    if id is None:
        return JsonResponse(
            {"template": DefaultTemplate.template, "bot_name": DefaultTemplate.bot_name}
        )

    obj = UserPromptTemplate.objects.filter(id=id).first()
    data = {
        "bot_name": obj.bot_name,
        "title": obj.title,
        "description": obj.description,
    }
    return JsonResponse(data, safe=False)


def switch_prompt(request, id=None):
    """Prompt Id is sent through AJAX request, to switch from one prompt to another. 
    The new prompt template and bot name is saved in session."""
    if id is None:
        request.session["user_template"] = DefaultTemplate.template
        request.session["bot_name"] = DefaultTemplate.bot_name
        return JsonResponse({"bot_name": request.session["bot_name"]})
    prompt = UserPromptTemplate.objects.filter(id=id).first()
    request.session["user_template"] = prompt.description
    request.session["bot_name"] = prompt.bot_name
    data = {"bot_name": prompt.bot_name}
    return JsonResponse(data, safe=False)


def delete(request, id=None):
    """ To delete Prompt."""
    if id:
        obj = UserPromptTemplate.objects.filter(id=id).first()
        if obj:
            obj.delete()
            messages.info(request, "Prompt deleted!!!!!")
            return redirect("chat:home")
        else:
            messages.error(request, "Prompt Not Found")
            return redirect("chat:home")


class Gallery(View):
    """
    The GET method displays all the images of that user on Gallery Page.
    The post method uses Hugging Face API to generate Image from Text.
    """

    def get(self, request):
        images = UsersGeneratedImages.objects.filter(user=request.user)
        context = {"data": images}
        return render(request, "gallery.html", context)

    def post(self, request):
        headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
        prompt = request.POST.get("image_prompt")
        title = request.POST.get("image_title")
        payload = {"inputs": prompt}
        response = requests.request(
            "POST", os.getenv("API_URL"), headers=headers, json=payload
        )
        if response.status_code == 200:
            img_obj = ImageFile(io.BytesIO(response.content), name="file.jpeg")
            UsersGeneratedImages.objects.create(
                user=request.user, image=img_obj, image_title=title, prompt=prompt
            )
            get_all_user_images = UsersGeneratedImages.objects.filter(user=request.user)
            context = {"data": get_all_user_images}
            return redirect("chat:gallery")
        else:
            print("Error:", response.status_code, response.text)
            return redirect("chat:home")


def delete_image(request, id):
    """This method deletes the image object."""
    try:
        obj = UsersGeneratedImages.objects.filter(id=id).first()
        if obj:
            obj.delete()
    except Exception as e:
        messages.warning(request, "Image does not exists")
    finally:
        return redirect("chat:gallery")
