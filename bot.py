import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

anlik_calisan = []

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global anlik_calisan
  anlik_calisan.remove(event.chat_id)


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("**Rowlyn Tagger Bot**,💸 Grub Veya Kalanınızdaki İstifadeçileri Tag Ede Bilersiniz ★\nDaha Çox Melumat Üçün **/help**'emrini yazın.",
                    buttons=(
                      [Button.url('🎭 Meni Bir Gruba Elave Et', 'https://t.me/RowlynTagBot?startgroup=a'),
                      Button.url('🚀 Sahibim', 'https://t.me/amciROWLYN')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**RowLynTagger bot'un Yardım Menyusu**\n\nKomut: /herkesitaget \n  Bu Emr-i, başqalarına cavablamağ istediyiniz mesajla birlikte işlede bilersiniz. \n`Meselen: /herkesitaget Salam!`  \nBu emr-i cavab olarağ işlede bilersiniz. cavablanan reply-e istifadeçileri tag edecek"
  await event.reply(helptext,
                    buttons=(
                      [Button.url('🎭 Meni Bir Gruba Elave Et', 'https://t.me/loungetaggerbot?startgroup=a'),
                      Button.url('🚀 Sahibim', 'https://t.me/amciROWLYN')]
                    ),
                    link_preview=False
                   )


@client.on(events.NewMessage(pattern="^/herkesitaget ?(.*)"))
async def mentionall(event):
  global anlik_calisan
  if event.is_private:
    return await event.respond("__Bu Emr Sadece Grub Ve Kanallarda İşledile Biler.!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__Sadece Yetkililer Bu Emr Den İstifade Ede Biler!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__Evvelki İstifadeçileri Tag Ede Bilmerem (gruba elave etmeden evvel olan mesajlar)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__ Mene Bir Komut Ver! __")
  else:
    return await event.respond("__Bir Mesaja Yanıt Verin Veya Çalışmam Üçün Mene Mesaj Verin__")
    
  if mode == "text_on_cmd":
    anlik_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tag Etmek Uğurlu Şekilde Durduruldu ❌")
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    anlik_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if event.chat_id not in anlik_calisan:
        await event.respond("Tag Etmek Uğurlu Şekilde Durduruldu ❌")
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""


print(">> Bot işleyir narahat olmayın 🚀 @amciROWLYN melumat ala bilersen <<")
client.run_until_disconnected()
