import datetime
from dhooks import Webhook

import config

_hook = Webhook.Async(config.LOG_WEBHOOK_URL)


async def log(message):
    current_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    log_message = f'[{current_time}]: {message}'
    
    await _hook.send(log_message)
