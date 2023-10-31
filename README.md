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

[Video_Link](https://drive.google.com/file/d/1EMwVXubFS0-kucvuibBOuf13FPzSeud7/view?usp=sharing)


## Whatsapp Bot Setup:

- Setup an application account on Twilio. Create an Application for Whatsapp and
set the environment variables for account_sid and auth token.

- Setup URL in Sanbox settings to test working of the project.


## Telegram Bot Setup:

- This file runs independtly from the rest of the project.
- Create a Telegram Bot using BotFather.
- Set the Token generated in .env file along with openai key and eleven labs.
- To run the file - `python telegrambot.py`
