import settings

import logging
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon import functions, types
from telethon.utils import pack_bot_file_id

download_root = settings.download_root

logging.basicConfig(level=logging.INFO)
logging.getLogger('telethon').setLevel(logging.CRITICAL)

api_id = settings.tg_sec['api_id']
api_hash = settings.tg_sec['api_hash']
client = TelegramClient('tgparse', api_id, api_hash)


# Printing download progress
def progress_callback(current, total):
    print('Downloaded', current, 'out of', total, 'bytes: {:.2%}'.format(current / total))

async def Main():
    channels_ids = settings.channels    
    for channel_id in channels_ids:
        channel_entity = await client.get_entity(PeerChannel(channel_id))
        dialog = await client(functions.messages.GetPeerDialogsRequest(
            peers=[channel_id]
        ))
        dialog = dialog.dialogs[0]
        unread_messages = []
        count=1
        async for message in client.iter_messages(channel_id):
            if count > dialog.unread_count:
                break
            unread_messages.append(message)
            count+=1
        if len(unread_messages) > 0: # Is unread messages
            for msg in unread_messages[::-1]:
                if not msg.media == None:
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
                    filename = '{}{}'.format(download_root, timestamp)
                    path = None
                    if getattr(msg.media, 'photo', None):
                        path = await msg.download_media(filename, progress_callback=progress_callback, thumb=-1)
                    elif getattr(msg.media, 'document', None):
                        path = await msg.download_media(download_root+timestamp, progress_callback=progress_callback)
                    logging.info(f'[DOWNLOAD] media from {channel_entity.username} to ' + path)
                await msg.mark_read()
        

with client:
    client.loop.run_until_complete(Main())