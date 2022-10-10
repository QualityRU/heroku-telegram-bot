# -*- coding: utf-8 -*-

import os

PARSE_MODE = 'HTML'  # MarkdownV2, HTML, None

API_TOKEN = os.getenv('BOT_TOKEN')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
PAYMENTS_PROVIDER_TOKEN = os.getenv('PAYMENTS_PROVIDER_TOKEN')

WEBHOOK_URL = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

LOG_LEVEL = 'DEBUG' #INFO
LOG_STYLE = {'critical': {'bold': True, 'color': 'red'},
             'debug': {'color': 'magenta'},
             'error': {'color': 'red'},
             'info': {'bold': True, 'color': 'green'},
             'notice': {'color': 'magenta'},
             'spam': {'color': 'green', 'faint': True},
             'success': {'bold': True, 'color': 'green'},
             'verbose': {'color': 'blue'},
             'warning': {'color': 'yellow'}}
LOG_FORMAT = '%(asctime)s,%(msecs)03d %(filename)+13s (%(name)s) [ LINE:%(lineno)-4s] %(levelname)s %(message)s'
