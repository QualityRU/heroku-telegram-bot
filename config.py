import os

API_TOKEN = os.getenv('BOT_TOKEN')

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '127.0.0.1'
#WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8081
#WEBAPP_PORT = os.getenv('PORT', default=8000)