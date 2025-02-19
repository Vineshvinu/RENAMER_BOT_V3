from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import (  InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find , dateupdate
import os
from PIL import Image
import time

log_channel = int(os.environ.get("LOG_CHANNEL", ""))

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

STRING = os.environ.get("STRING", "")

app = Client("test", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

@Client.on_callback_query(filters.regex('cancel'))
async def cancel(bot,update):
	try:
		await update.message.delete()
	except:
		return
		
		
@Client.on_callback_query(filters.regex('rename'))
async def rename(bot,update):
	date_fa = str(update.message.date)
	pattern = '%Y-%m-%d %H:%M:%S'
	date = int(time.mktime(time.strptime(date_fa, pattern)))
	chat_id = update.message.chat.id
	id = update.message.reply_to_message_id
	await update.message.delete()
	await update.message.reply_text(f"__Please enter the new filename...__\n\nNote:- Extension Not Required",reply_to_message_id = id,
	reply_markup=ForceReply(True) )
	dateupdate(chat_id,date)
	
	
	
@Client.on_callback_query(filters.regex("doc"))
async def doc(bot,update):
     new_name = update.message.text
     name = new_name.split(":-")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
     value = 2099999999
     if value < file.file_size:
     	ms = await update.message.edit("``` Trying To Download...```")
     	c_time = time.time()
     	try:
     		path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     		
     	except Exception as e:
     		await ms.edit(e)
     		return
     	splitpath = path.split("/downloads/")
     	dow_file_name = splitpath[1]
     	old_file_name =f"downloads/{dow_file_name}"
     	os.rename(old_file_name,file_path)
     	user_id = int(update.message.chat.id)
     	thumb = find(user_id)
     	if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 320))
     		img.save(ph_path, "JPEG")
     		c_time = time.time()
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			filw = await app.send_document(log_channel,document = file_path,thumb=ph_path,caption = f"**{new_filename}**",progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			from_chat = filw.chat.id
     			mg_id = filw.id
     			time.sleep(2)
     			await bot.copy_message(update.from_user.id,from_chat,mg_id)
     			    			
     			await ms.delete()
     			os.remove(file_path)
     			os.remove(ph_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			os.remove(ph_path)
     			return
     	else:
     		
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			filw = await app.send_document(log_channel,document = file_path,caption = f"**{new_filename}**",progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			from_chat = filw.chat.id
     			mg_id = filw.id
     			time.sleep(2)
     			await bot.copy_message(update.from_user.id,from_chat,mg_id)
     			
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			return
     		
     ms = await update.message.edit("``` Trying To Download...```")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return
     	
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     user_id = int(update.message.chat.id)
     thumb = find(user_id)
     if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 320))
     		img.save(ph_path, "JPEG")
     		c_time = time.time()
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_document(update.message.chat.id,document = file_path,thumb=ph_path,caption = f"**{new_filename}**",progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     			os.remove(ph_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			os.remove(ph_path)
     			return
     			     		     		
     else:
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_document(update.message.chat.id,document = file_path,caption = f"**{new_filename}**",progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			return
     			     		   		
     		
@Client.on_callback_query(filters.regex("vid"))
async def vid(bot,update):
     new_name = update.message.text
     name = new_name.split(":-")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     message = update.message.reply_to_message
     file = message.document or message.video or message.audio
     value = 2099999999
     if value < file.file_size:
     	ms = await update.message.edit("``` Trying To Download...```")
     	c_time = time.time()
     	try:
     		path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     		
     	except Exception as e:
     		await ms.edit(e)
     		return
     	splitpath = path.split("/downloads/")
     	dow_file_name = splitpath[1]
     	old_file_name =f"downloads/{dow_file_name}"
     	os.rename(old_file_name,file_path)
     	user_id = int(update.message.chat.id)
     	thumb = find(user_id)
     	duration = 0
     	metadata = extractMetadata(createParser(file_path))
     	if metadata.has("duration"):
     		duration = metadata.get('duration').seconds
     	if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 320))
     		img.save(ph_path, "JPEG")
     		c_time = time.time()
     		
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			filw = await app.send_video(log_channel,video= file_path,thumb=ph_path,caption = f"**{new_filename}**",duration =duration,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			from_chat = filw.chat.id
     			mg_id = filw.id
     			time.sleep(2)
     			await bot.copy_message(update.from_user.id,from_chat,mg_id)
     			await ms.delete()
     			os.remove(file_path)
     			os.remove(ph_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			os.remove(ph_path)
     			return
     	else:
     		
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			filw = await app.send_video(log_channel,video = file_path,caption = f"**{new_filename}**",duration = duration,progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			from_chat = filw.chat.id
     			mg_id = filw.id
     			time.sleep(2)
     			await bot.copy_message(update.from_user.id,from_chat,mg_id)
     			
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			return
     			
     	     	
     	
     ms = await update.message.edit("``` Trying To Download...```")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return
     
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     metadata = extractMetadata(createParser(file_path))
     if metadata.has("duration"):
     		duration = metadata.get('duration').seconds
     user_id = int(update.message.chat.id)
     thumb = find(user_id)
     if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 320))
     		img.save(ph_path, "JPEG")
     		c_time = time.time()
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			filw = await bot.send_video(update.message.chat.id,video = file_path,caption = f"**{new_filename}**",thumb=ph_path,duration =duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			
     			await ms.delete()
     			os.remove(file_path)   				
     		except Exception as e:
     				await ms.edit(e)
     				os.remove(file_path)
     				
     else:
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_video(update.message.chat.id,video = file_path,caption = f"**{new_filename}**",duration = duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			return
   
     			     		     		
@Client.on_callback_query(filters.regex("aud"))
async def aud(bot,update):
     new_name = update.message.text
     name = new_name.split(":-")
     new_filename = name[1]
     file_path = f"downloads/{new_filename}"
     file = update.message.reply_to_message
     ms = await update.message.edit("``` Trying To Download...```")
     c_time = time.time()
     try:
     	path = await bot.download_media(message = file , progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
     except Exception as e:
     	await ms.edit(e)
     	return
     splitpath = path.split("/downloads/")
     dow_file_name = splitpath[1]
     old_file_name =f"downloads/{dow_file_name}"
     os.rename(old_file_name,file_path)
     duration = 0
     metadata = extractMetadata(createParser(file_path))
     if metadata.has("duration"):
     	duration = metadata.get('duration').seconds
     user_id = int(update.message.chat.id)
     thumb = find(user_id)
     if thumb:
     		ph_path = await bot.download_media(thumb)
     		Image.open(ph_path).convert("RGB").save(ph_path)
     		img = Image.open(ph_path)
     		img.resize((320, 320))
     		img.save(ph_path, "JPEG")
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_audio(update.message.chat.id,audio = file_path,caption = f"**{new_filename}**",thumb=ph_path,duration =duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     			os.remove(ph_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
     			os.remove(ph_path)
     else:
     		await ms.edit("```Trying To Upload```")
     		c_time = time.time()
     		try:
     			await bot.send_audio(update.message.chat.id,audio = file_path,caption = f"**{new_filename}**",duration = duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
     			await ms.delete()
     			os.remove(file_path)
     		except Exception as e:
     			await ms.edit(e)
     			os.remove(file_path)
