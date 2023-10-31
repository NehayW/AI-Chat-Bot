# AI-Chat-Bot

## Project Setup:

python version = 3.11

1. First you have to create virtual-environment 
    - If you have install virtualenv then follow command
        - virtualenv -p python(your python version) environment-name
    - If you don't have install virtualenv then install first

2. Activate Virtualenv
    - source environment-name/bin/activate

3. Install requirements.txt
    - pip3 install -r requirements.txt

4. Run migration and migrate command:
    - python manage.py makemigrations
    - python manage.py migrate
    - Create super user for admin panel by filling required details
        - python manage.py createsuperuser

5. Run Project Using - `python manage.py runserver`

[Video_Link](https://drive.google.com/file/d/1EMwVXubFS0-kucvuibBOuf13FPzSeud7/view?usp=sharing "Demo Video")


## Whatsapp Bot Setup:

- Setup an application account on Twilio. Create an Application for Whatsapp and
set the environment variables for account_sid and auth token.

- Setup URL in Sanbox settings to test working of the project.


## Telegram Bot Setup:

- This file runs independtly from the rest of the project.
- Create a Telegram Bot using BotFather.
- Set the Token generated in .env file along with openai key and eleven labs.
- To run the file - `python telegrambot.py`


## Generate Tokens

1. OpenAI
    - Create an account on Openai.
    - Go to Profile Icon > View API Keys > Create a new secret key
    - After creating the key add it in the .env file.
    - Link: [OPENAI](https://openai.com/ "OpenAI")

2. ElevenLabs
    - Create an account on ElevenLabs
    - Go to Profile Icon > Profile > API KEY
    - Copy this key and set up in .env file.
    - Link: [ELEVEN_LABS](https://elevenlabs.io/ "ElevenLabs")

3. Hugging Face
    - Create an account on Hugging Face.
    - Go to Settings > Access Token
    - Copy this Token and set up in .env file.
    - Link: [HUGGING_FACE](https://huggingface.co/ "HUGGING_FACE")

4. Twilio
    - Create an account on Twilio.
    - Create an application for Whatsapp.
    - Copy the account_sid and auth token and add it in .env file.
    - Link: [Twilio](https://www.twilio.com/en-us "Twilio")

5. Telegram
    - Create a telegram bot using BotFather.
    - After successful creation of Telegram Bot you will recieve a Token.
    - Copy this Token and set up in .env file.
    - Link: [Telegram](https://web.telegram.org/k/ "Telegram")