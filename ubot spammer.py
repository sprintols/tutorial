from pyrogram.errors import *
from pyrogram import Client, filters
import os, json, asyncio

api_hash = ""
api_id = 1
ubot = Client("my_ubot",api_id,api_hash)

AFKMode = False
First = []
mutedList = []
Approved = []
spamEnabled = False

if os.path.exists("gruppigmex.json"):
   with open("gruppigmex.json", "r+") as f:
      Groups = json.load(f)
else:
   Groups = {}
   with open("gruppigmex.json", "w+") as f:
      json.dump(Groups, f)
   

async def updateGroups():
   global Groups
   with open("gruppigmex.json", "w+") as f:
      json.dump(Groups, f)
   return True

@ubot.on_message(filters.user("self") & filters.command("spam","."))
async def SpamFunction(client, message):
   global Groups, spamEnabled
   st = message.text.split(" ", 2)
   if len(st) == 3:
      if st[1].isnumeric():
         if len(Groups) > 0:
            if not spamEnabled:
               spamEnabled = True
               await message.edit("**✅ » Spam Avviato!**")
               while spamEnabled:
                  await asyncio.wait([client.send_message(int(chat), st[2]) for chat in Groups])
                  for i in range(int(st[1]) * 60):
                     if spamEnabled:
                        await asyncio.sleep(1)
                     else:
                        break
            else:
               await message.edit("**⚠️ Errore** » __Spam già avviato!__")
         else:
            await message.edit("**⚠️ Errore** » __Non ci sono gruppi in cui spammare!__")
      else:
         await message.edit("**⚠️ Errore** » __Tempo non valido!__")
   else:
      await message.edit("**⚠️ Errore** » __Specifica il tempo in minuti e il messaggio da spammare!__")
   

@ubot.on_message(filters.user("self") & filters.command("stop","."))
async def stopSpam(client, message):
   global spamEnabled
   if spamEnabled:
      spamEnabled = False
      await message.edit("**❌ » Spam Stoppato!**")
   else:
      await message.edit("**⚠️ Errore** » __Lo spam non è avviato!__")
   
@ubot.on_message(filters.user("self") & filters.command("block",".") & filters.private)
async def block_user(client, message):
   message.delete()
   ubot.send_message(message.chat.id, "❌Sei stato bloccato")
   time.sleep(2)
   ubot.block_user(message.chat.id)

@ubot.on_message(filters.user("self") & filters.command("archive",".") & filters.private)
async def archiveuser(client, message):
   message.delete()
   ubot.send_message(message.chat.id, "❌Sei stato archiviato")
   time.sleep(2)
   ubot.archive_chats(message.chat.id)

@ubot.on_message(filters.user("self") & filters.command("mute",".") & filters.private)
async def mute_user(client, message):
   global mutedList
   if message.chat.id in mutedList:
      message.edit("❌Utente già mutato❌")
   else:
      mutedList.append(message.chat.id)
      message.edit("❌Sei stato mutato❌")


@ubot.on_message(filters.user("self") & filters.command("unarchive",".") & filters.private)
async def unarchive_user(client, message):
   message.delete()
   ubot.send_message(message.chat.id, "✅Sei stato unarchiviato.   :)))")
   time.sleep(2)
   ubot.unarchive_chats(message.chat.id)

@ubot.on_message(filters.user("self") & filters.command("unmute",".") & filters.private)
def unmute_user(client, message):
   global mutedList
   if message.chat.id in mutedList:
      mutedList.remove(message.chat.id)
      message.edit("✅Sei stato smutato✅")
   else:
      message.edit("❌Utente non mutato❌")


@ubot.on_message(filters.incoming & filters.private)
async def doMute(client, message):
   global mutedList
   if message.chat.id in mutedList:
      message.delete()


@ubot.on_message(filters.command("riavvia",".") & filters.user("self"))
async def chat_info(client, message):
   msg = message
   chat_id = msg.chat.id
   try:
       ubot.send_message(chat_id = chat_id, text = "Riavvio in corso...")
       subprocess.call("systemctl restart userbot", shell=True)
   except:
       pass

   

@ubot.on_message(filters.user("self") & filters.command("addgroup","."))
async def addChat(client, message):
   global Groups
   st = message.text.split(" ", 1)
   if len(st) == 2:
      if st[1].isnumeric():
         mex = int(st[1])
      else:
         mex = st[1]
      try:
         group = await client.get_chat(mex)
      except:
         await message.edit(f"**⚠️ Errore** » __Chat non trovata, controlla di aver inserito l'username/ID corretto!__")
         return
      if group.type == "private":
         await message.edit("**⚠️ Errore** » __Puoi aggiungere solo gruppi o canali!__")
         return
      if not str(group.id) in Groups:
         Groups[str(group.id)] = group.title
         await updateGroups()
         await message.edit(f"**✅ » Chat** {group.title} **aggiunta con successo!**")
      else:
         await message.edit(f"**⚠️ Errore** » __Chat__ {group.title} __già presente nel database__")
   else:
      await message.edit("**⚠️ Errore** » __Specifica la chat da aggiungere!__")
   

@ubot.on_message(filters.user("self") & filters.command("approve",".") & filters.private & ~filters.bot)
def accept(client, message):
   global Approved
   if not message.chat.id in Approved:
      Approved.append(message.chat.id)
      message.edit("✅Utente Approvato✅")
   else:
      message.edit("❌Utente Già Approvato❌")


@ubot.on_message(filters.user("self") & filters.command("disapprove",".") & filters.private & ~filters.bot)
def disapprove(client, message):
   global Approved
   if message.chat.id in Approved:
      Approved.remove(message.chat.id)
      message.edit("❌Utente Disapprovato❌")
   else:
      message.edit("❌Utente Non Approvato❌")


@ubot.on_message(filters.user("self") & filters.command("afk","."))
def setAFK(client, message):
   global AFKMode, First
   if AFKMode:
      AFKMode, First = False, []
      message.edit("❌AFK Mode Disattivata❌")
   else:
      AFKMode = True
      message.edit("✅AFK Mode Attivata✅")



@ubot.on_message(filters.user("self") & filters.command("remgroup","."))
async def remChat(client, message):
   global Groups
   st = message.text.split(" ", 1)
   if len(st) == 2:
      if st[1].isnumeric():
         mex = int(st[1])
      else:
         mex = st[1]
      try:
         group = await client.get_chat(mex)
      except:
         await message.edit("**⚠️ Errore** »__Chat non trovata__ ")
         return
      if str(group.id) in Groups:
         del Groups[str(group.id)]
         await updateGroups()
         await message.edit(f"**🚫 » Chat** {group.title} **rimossa con successo!**")
      else:
         await message.edit(f"**⚠️ Errore** » __Chat__ {group.title} __non presente nel database__")
   else:
      await message.edit("**⚠️ Errore** » __Specifica la Chat da rimuovere!__")
   

@ubot.on_message(filters.user("self") & filters.command("grouplist","."))
async def chatsList(client, message):
   global Groups
   if len(Groups) > 0:
      msg = "**💬 LISTA CHAT 💬**\n"
      for id in Groups:
         msg += "\n" + Groups[id] + f" [`{id}`]"
         await message.edit(msg + "\n\n__📂 Chat Totali  »__ `" + str(len(Groups)) + "`")
   else:
      await message.edit("**⚠️ Nessuna Chat Aggiunta ⚠️**")
   

@ubot.on_message(filters.user("self") & filters.command("afk","."))
async def setAFK(client, message):
   global AFKMode, First
   if AFKMode:
      AFKMode, First = False, []
      await message.edit("❌AFK Mode Disattivata❌")
   else:
      AFKMode = True
      await message.edit("✅AFK Mode Attivata✅")
   

      
   

ubot.run()
