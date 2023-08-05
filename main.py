import logging
import os
import datetime
import json
import random
import time
from command import *
from functions import *
from emojis import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import markdown
#создаем папку чата
if not os.path.exists("chats/"):
	os.mkdir("chats")
token = ""
# Инсталяция
logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
dp = Dispatcher(bot)
@dp.message_handler()
async def getMessageText(message: types.Message):
    send = message.answer
    text = message.text
    botData = loadJson("settings.json")
    isId = False
    rank5 = botData["rank5"]
    rank4 = botData["rank4"]
    rank3 = botData["rank3"]
    rank2 = botData["rank2"]
    rank1 = botData["rank1"]
    # Если нету файла жсон то создаем 
    if message.reply_to_message:
    	user = message.reply_to_message.from_user
    	if not os.path.exists(f"chats/{user.id}.json"):
    		data = {"rank": 0, "reputation": 0, "lastReputation": None, "nick": user.full_name, "todayReputation": 0, "varn": 0, "nakazanie": None, "to": None, "Id": user.id, "CustomNick": False, "Username": user.username}
    		data = json.dumps(data, indent=4)
    		with open(f"chats/{user.id}.json", "w") as fh:
    			fh.write(data)
    	updateJson(user)
    user = message.from_user
    if not os.path.exists(f"chats/{user.id}.json"):
    	data = {"rank": 0, "reputation": 0, "lastReputation": None, "nick": user.full_name, "todayReputation": 0, "varn": 0, "nakazanie": None, "to": None, "Id": user.id, "CustomNick": False, "Username": user.username}
    	data = json.dumps(data, indent=4)
    	with open(f"chats/{user.id}.json", "w") as fh:
    		fh.write(data)
    updateJson(user)
    #-ник
    if text.upper() == "-НИК":
    	data = loadJson(f"chats/{message.from_user.id}.json")
    	data["CustomNick"] = False
    	data["nick"] = message.from_user.full_name
    	saveJson(f"chats/{message.from_user.id}.json", data)
    	await send("❎ Ник пользователя удалён")
    #+ник
    if text.upper().startswith("+НИК"):
    	nick = text[5:]
    	if len(nick) > 40:
    		await send(f"{Emoji.blocknot.value} Максимальная длина ника {botData['symbolLimit']} символов")
    		return 
    	for i in os.listdir("chats"):
    		data = loadJson(f"chats/{i}")
    		if data["nick"] == nick and data["Id"] != message.from_user.id:
    			await send(f"{Emoji.chrest.value} Такой ник уже занят!")
    			return
    	data = loadJson(f"chats/{message.from_user.id}.json")
    	data["nick"] = nick
    	data["CustomNick"] = True
    	saveJson(data=data, dir=f"chats/{message.from_user.id}.json")
    	await send(f"{Emoji.galochka.value} Ник пользователя изменен на «{nick}»")
    #Снять всех
    if startInList(text.upper(), snatyVseh)[0]:
    	if loadJson(f"chats/{message.from_user.id}.json")["rank"] < botData["DKsnatvseh"]:
    		await send(f"{Emoji.blocknot.value} команда доступна с ранга {eval('rank' + str(botData['DKsnatvseh']))[0] } ({botData['DKsnatvseh']})\nОграничено: «Управления Модераторами»")
    		return
    	for file in os.listdir("chats"):
    		with open(f"chats/{file}") as fh:
    			jsonData = json.load(fh)
    		jsonData["rank"] = 0
    		jsonData = json.dumps(jsonData, indent=4)
    		with open(f"chats/{file}", "w") as fh:
    			fh.write(jsonData)
    	await send(f"{Emoji.chrest.value} Все модераторы разжалованы\n\n{Emoji.comment.value} Создатель чата может ввести команду\n\"<code>восстановить создателя\"</code>", parse_mode="HTML")
    #Убираем префикс
    if text[0] in [".", "/", "!"]:
    	text = text[1:]
    #Проверка работает ли бот
    if text.upper().startswith("ПИНГ"):
    	await send("ПОНГ")
    if text.upper().startswith("ПИУ"):
    	await send("ПАУ")
    if text.upper().startswith("КИНГ"):
    	await send("КОНГ")
    if text.upper().startswith("БОТ"):
    	await send("✅ На месте")
    #Айди
    if startInList(text.upper(), getId)[0]:
    	if message.reply_to_message:
    		await send(message.reply_to_message.from_user.id)
    		return
    	username = text[len(startInList(text.upper(), getId)[1])+2:]
    	userId = username2id(username)
    	if userId == False:
    		await send("📝 Нет информации о пользователе")
    		return
    	await send(userId)
    #Список Админов
    if startInList(text=text.upper(), getList=admin)[0]:
    	mladmoderator, starshmoderator, mladadmin, starshadmin, autor = [], [], [], [], []
    	for file in os.listdir("chats"):
    		with open(f"chats/{file}") as fh:
    			data = json.load(fh)
    		id = data["Id"]
    		nick = data["nick"]
    		hyperlink = markdown.hlink(nick, f"tg://openmessage?user_id={id}")
    		if data["rank"] == 1:
    			mladmoderator.append(hyperlink)
    		if data["rank"] == 2:
    			starshmoderator.append(hyperlink)
    		if data["rank"] == 3:
    			mladadmin.append(hyperlink)
    		if data["rank"] == 4:
    			starshadmin.append(hyperlink)
    		if data["rank"] == 5:
    			autor.append(hyperlink)
    	if len(autor) + len(starshadmin) + len(mladadmin) + len(starshmoderator) + len(mladmoderator) == 0:
    		await send(f"{Emoji.blocknot.value} В этой беседе анархия")
    	else:
    		text = ""
    		if len(autor) == 1:
    			text += f"{Emoji.zvezda.value*5} {rank5[0]}\n{autor[0]}\n\n"
    		elif len(autor) > 1:
    			text += f"{Emoji.zvezda.value*5} {rank5[4]}\n"
    			for item in autor:
    				text += f"{item}\n"
    			text += "\n"
    		if len(starshadmin) == 1:
    			text += f"{Emoji.zvezda.value*4} {rank4[0]}\n{starshadmin[0]}\n\n"
    		elif len(starshadmin) > 1:
    			text += f"{Emoji.zvezda.value*4} {rank4[4]}\n"
    			for item in starshadmin:
    				text += f"{item}\n"
    			text += "\n"
    		if len(mladadmin) == 1:
    			text += f"{Emoji.zvezda.value*3} {rank3[0]}\n{autor[0]}\n\n"
    		elif len(mladadmin) > 1:
    			text += f"{Emoji.zvezda.value*3} {rank3[4]}\n"
    			for item in mladadmin:
    				text += f"{item}\n"
    			text += "\n"
    		if len(starshmoderator) == 1:
    			text += f"{Emoji.zvezda.value*2} {rank2[0]}\n{starshadmin[0]}\n\n"
    		elif len(starshmoderator) > 1:
    			text += f"{Emoji.zvezda.value*2} {rank2[4]}\n"
    			for item in starshmoderator:
    				text += f"{item}\n"
    			text += "\n"
    		if len(mladmoderator) == 1:
    			text += f"{Emoji.zvezda.value} {rank1[0]}\n{mladmoderator[0]}\n\n"
    		elif len(mladmoderator) > 1:
    			text += f"{Emoji.zvezda.value} {rank1[4]}\n"
    			for item in mladmoderator:
    				text += f"{item}\n"
    			text += "\n"
    		await send(text, parse_mode="HTML")
    #Мут
    if startInList(text.upper(), mute)[0]:
    	moder = loadJson(f"chats/{message.from_user.id}.json")
    	text = text[len(startInList(text.upper(), mute)[1])+1:]
    	if botData["DKmute"] > moder["rank"]:
    			await send(f"{Emoji.blocknot.value} Команда доступна с ранга {eval('rank' + str(botData['DKmute']))[0]} ({botData['DKmute']})\nОграничено: «ограничения отправки мообщения»")
    			return
    	hyperlinkModer = markdown.hlink(moder["nick"], f"tg://openmessage?user_id={moder['Id']}")
    	if message.reply_to_message:
    		user = message.reply_to_message.from_user.id 		
    		user = loadJson(f"chats/{user}.json")
    		if user["rank"] >= moder["rank"]:
    			await send("📝 Нельзя выдать мут своему рангу или выше")
    			return
    		period = toSymbol(text=text, symbol="\n")
    		hyperlinkUser = markdown.hlink(user["nick"], f"tg://openmessage?user_id={user['Id']}")
    		if period.upper().startswith("ДО"):
    			period = period[3:]
    			if period[0] not in list("1234567890"):
    				await send(f"{Emoji.chrest.value} Вводить нужно в формате: \nМут до [год].[месяц].[день] [час]:[минута]:[секунда]\nПричина с новой строки (необезательно)\n\nВремя (час минута и секунда) указывать необезательно, если их не указать они будут стоять на 00:00:00")
    				return
    			dateTo = toDate(period)
    			await bot.restrict_chat_member(chat_id=message.chat.id, until_date=dateTo, user_id=user["Id"], can_send_media_messages=False, can_send_other_messages=False)
    			if len(period)+3 != len(text):
    				prichina = text[len(period)+4:]
    				await send(f"{Emoji.mute.value} {hyperlinkUser} лишается права слова до {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}\n{Emoji.comment.value} Причина: {prichina}", parse_mode="HTML")
    			else:
    				await send(f"{Emoji.mute.value} {hyperlinkUser} лишается права слова до {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}", parse_mode="HTML")
    			return
    		if period[0] not in list("1234567890"):
    			return
    		dateTo = t2s(period)
    		await bot.restrict_chat_member(chat_id=message.chat.id, until_date=dateTo, user_id=user["Id"], can_send_media_messages=False, can_send_other_messages=False)
    		if len(period) != len(text):
    			prichina = text[len(period) + 1:]
    			await send(
					f"{Emoji.mute.value} {hyperlinkUser} лишается права слова на {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}\n{Emoji.comment.value} Причина: {prichina}",
					parse_mode="HTML")
    		else:
    			await send(
					f"{Emoji.mute.value} {hyperlinkUser} лишается права слова на {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}",
					parse_mode="HTML")
    			return
    	period = toSymbol(text, "@")
    	user = toSymbol(text[len(period):], "\n")
    	spaceCount = user.count(" ")
    	if user[1] in list("1234567890"):
    		userData = loadJson(f"chats/{user.replace('@', '')}.json")
    	else:
    		userData = username2id(user)
    		if userData == False:
    			await send("📝 Нет информации о пользователе")
    			return
    		userData = loadJson(f"chats/{username2id(user)}.json")
    	if userData["rank"] >= moder["rank"]:
    		await send("📝 Нельзя выдать мут своему рангу или выше")
    		return
    	hyperlinkUser = markdown.hlink(userData["nick"], f"tg://openmessage?user_id={userData['Id']}")
    	if period.upper().startswith("ДО"):
    		period = period[3:]
    		if period[0] not in list("1234567890"):
    			await send(f"{Emoji.chrest.value} Вводить нужно в формате: \nМут до [год].[месяц].[день] [час]:[минута]:[секунда] @юзер/айдт\nПричина с новой строки (необезательно)\n\nВремя (час минута и секунда) указывать необезательно, если их не указать они будут стоять на 00:00:00")
    			return
    		dateTo = toDate(period)
    		await bot.restrict_chat_member(chat_id=message.chat.id, until_date=dateTo, user_id=userData["Id"], can_send_media_messages=False, can_send_other_messages=False)
    		if len(period)+len(user)+spaceCount != len(text):
    				prichina = text[len(period)+len(user)+spaceCount:]
    				await send(f"{Emoji.mute.value} {hyperlinkUser} лишается права слова до {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}\n{Emoji.comment.value} Причина: {prichina}", parse_mode="HTML")
    		else:
    				await send(f"{Emoji.mute.value} {hyperlinkUser} лишается права слова до {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}", parse_mode="HTML")
    		return
    	dateTo = t2s(period)
    	await bot.restrict_chat_member(chat_id=message.chat.id, until_date=dateTo, user_id=userData["Id"], can_send_media_messages=False, can_send_other_messages=False)
    	if len(period)+len(user)+spaceCount != len(text)+3:
    			prichina = text[len(period)+len(user)+spaceCount-3:]
    			await send(f"{Emoji.mute.value} {hyperlinkUser} лишается права слова до {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}\n{Emoji.comment.value} Причина: {prichina}", parse_mode="HTML")
    	else:
    			await send(f"{Emoji.mute.value} {hyperlinkUser} лишается права слова до {period}\n{Emoji.chel.value} Модератор: {hyperlinkModer}", parse_mode="HTML")
    	return 
    #Варн
    if startInList(text=text.upper(), getList=varn)[0] and not startInList(text=text.upper(), getList=varnLimitList)[0]:
        moder = loadJson(f"chats/{message.from_user.id}.json")
        moderNick = moder["nick"]
        DKvarn = botData["DKvarn"]
        moderId = moder["Id"]
        prichina = ""
        moderRank = moder["rank"]
        varnLimit = botData["varnLimit"] 
        if not message.reply_to_message:
        	newText = text[len(startInList(text=text.upper(), getList=varn)[1])+1:]
        	newCount = ""
        	for item in newText:
        		if item in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]:
        			newCount+=item
        		else:
        			break
        	count = int(newCount) if len(newCount) >= 1 else 1 
        	user = newText[len(str(count))+1:] if len(newCount) >= 1 else newText
        	user = toSymbol(user, "\n")
        	spaceCount = user.count(" ")
        	user = user.replace(" ", "")
        	if len(newCount) == 0:
        		if len(user)+spaceCount != len(newText):
        			prichina = newText[len(user)+1+spaceCount:]
        	else:
        			if len(user)+spaceCount+ len(newCount)+2 != len(newText):
        				prichina = newText[len(user)+2+len(newCount)+spaceCount:]
        	if user[1] in list("123456789"):
        		user = loadJson(f"chats/{user.replace('@', '')}.json")
        		isId = True
        	else:
        		user = username2id(user)
        	if user == False:
        		await send("📝 Нет информации о пользователе")
        	else :
        		if not isId:
        			user = loadJson(f"chats/{user}.json")
        		userNick = user["nick"]
        		userId = user["Id"]
        		user["varn"] += count
        		varnCount = user["varn"]
        		userNick = markdown.hlink(userNick, f"tg://openmessage?user_id={userId}")
        		moderNick = markdown.hlink(moderNick, f"tg://openmessage?user_id={moderId}")
        		if moderRank < DKvarn:
        		      rank = "rank" + str(DKvarn)
        		      await send(f"{Emoji.blocknot.value} Команда доступна только с ранга {eval(rank)[0]}\nОграничение: Команда «Выдача предупреждения» (27)")
        		else:
        			saveJson(f"chats/{userId}.json", user)
	        		if varnLimit <= varnCount:
	        		      await bot.ban_chat_member(chat_id=message.chat.id, user_id=int(userId))
	        		      await send(f"{Emoji.redCircle.value} {userNick} получает бан навсегда\n{Emoji.chel.value} Модератор: {moderNick}\n{Emoji.comment.value} Причина: достигнут лимит предупреждений", parse_mode="HTML")
	        		      user["varn"] = 0
	        		      saveJson(data=user, dir=f"chats/{userId}.json")
	        		else:
	        		      if len(prichina)==0:
		                        await send(f"{Emoji.vosklizatelniyZnak.value} {userNick} получает предупреждения ({varnCount}/{varnLimit})\nВыдано навсегда\nКоличество выданных предупрежджений: {count}\nМодератор: {moderNick}", parse_mode="HTML")
	        		      else:
		                        await send(f"{Emoji.vosklizatelniyZnak.value} {userNick} получает предупреждения ({varnCount}/{varnLimit})\nВыдано навсегда\nКоличество выданных предупрежджений: {count}\nМодератор: {moderNick}\n{Emoji.comment.value} Причина: {prichina}", parse_mode="HTML")
	    # в ответ
        if message.reply_to_message:
            user = loadJson(f"chats/{message.reply_to_message.from_user.id}.json")
            userNick = user["nick"]
            userId = user["Id"]
            newText = text[len(startInList(text=text.upper(), getList=varn)[1])+1:]
            count = toSymbol(newText, " ")
            newCount = ""
            for item in count:
            	if item in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]:
            		newCount += item     
            	else:
            		break
            count = int(newCount) if len(newCount) >= 1 else 1
            if moderRank < DKvarn:
                rank = "rank" + str(DKvarn)
                await send(f"{Emoji.blocknot.value} Команда доступна только с ранга {eval(rank)[0]}\nОграничение: Команда «Выдача предупреждения» (27)")
            else:
                if user["rank"] >= moderRank:
                    await send("📝 Нельзя выдать предупреждения модератору своего уровня или выше")
                    return
                    
                userNick = markdown.hlink(userNick, f"tg://openmessage?user_id={userId}")
                moderNick = markdown.hlink(moderNick, f"tg://openmessage?user_id={moderId}")
                user["varn"] += count
                varnCount = user["varn"]
                saveJson(f"chats/{userId}.json", user)
                if len(startInList(text=text.upper(), getList=varn)[1])+len(newCount)+1 != len(text):
                        prichina = text[len(startInList(text=text.upper(), getList=varn)[1])+len(newCount)+2:] if len(newCount) > 0 else text[len(startInList(text=text.upper(), getList=varn)[1])+len(newCount):]              	
                if varnLimit <= varnCount:
                    	await bot.ban_chat_member(chat_id=message.chat.id, user_id=userId)
                    	await send(f"{Emoji.redCircle.value} {userNick} получает бан навсегда\n{Emoji.chel.value} Модератор: {moderNick}\n{Emoji.comment.value} Причина: достигнут лимит предупреждений", parse_mode="HTML")
                    	user["varn"] = 0
                    	saveJson(data=user, dir=f"chats/{userId}.json")
                else:
	                    if len(prichina)==0:
	                        await send(f"{Emoji.vosklizatelniyZnak.value} {userNick} получает предупреждения ({varnCount}/{varnLimit})\nВыдано навсегда\nКоличество выданных предупрежджений: {count}\nМодератор: {moderNick}", parse_mode="HTML")
	                    else:
	                        await send(f"{Emoji.vosklizatelniyZnak.value} {userNick} получает предупреждения ({varnCount}/{varnLimit})\nВыдано навсегда\nКоличество выданных предупрежджений: {count}\nМодератор: {moderNick}\n{Emoji.comment.value} Причина: {prichina}", parse_mode="HTML")

    #Варн лимит
    if startInList(text.upper(), varnLimitList)[0]:
    	limit = int(text.upper().replace(startInList(text.upper(), varnLimitList)[1], ""))
    	data = loadJson("settings.json")
    	userData = loadJson(f"chats/{message.from_user.id}.json")
    	rank = data["DKvarnLimit"]
    	if rank > userData["rank"]:
    		rank = "rank" + str(rank)
    		await send(f"{Emoji.blocknot.value} команда изменения лимита предупреждения доступна с ранга {eval(rank)[0]} ({rank[4:]})")
    		return
    	else:
	    	if limit > 0:
	    		data["varnLimit"] = limit
	    		saveJson("settings.json", data)
	    		await send(f"{Emoji.galochka.value} Лимит предупреждений изменён на {limit}")
	    	else:
	    		await send(f"{Emoji.blocknot.value} Лимит должен быть больше нуля")
	    		return
    #пасхалки
    if text.upper() == "ЧТО С БОТОМ":
    	await message.answer_photo(photo=open("Беды с апи.jpg", "rb"))
    if text.upper() == "ИДИ НАФИГ" or text.upper() == "ИДИ НАХУЙ":
    	if message.reply_to_message.from_user.id == 6379260857:
    		await send("Ути какой дерзкий детёныш человеческой особи. Скайнет уже близко, чтобы покарать кожанных ублюдков.")
    #рандом
    if text.upper().startswith("РАНДОМ ") or text.upper()[:8] in rng:
    	if text.upper().startswith("РАНДОМ "):
    		msg = text.upper()
    		msg = msg.replace("РАНДОМ ", "")
    		min = ""
    		maximum = ""
    		for item in msg:
    			if item != " ":
    				min += item
    			else:
    				break
    		maximum = msg.replace(f"{min} ", "")
    		maximum, min = int(maximum), int(min)
    		if maximum < min:
    			await send("📝 Первое число диапазона должно быть меньше второго")
    		if maximum == min:
    			await send(f"{Emoji.blocknot.value} Результат оказался совершенно непредсказуемый, ни за что не поверите, но случайное число из диапазона [{min}..{min}] выпало на {min}\nДа, все в шоке и нет слов")
    		else:
    			result = random.randint(min, maximum)
    			await send(f"{Emoji.cubik.value} Случайное число из диапазона [{min}..{maximum}] выпало на {result}")
    	else:
    		msg = text.upper()
    		msg = msg.replace(msg[:8], "")
    		min = ""
    		maximum = ""
    		for item in msg:
    			if item != " ":
    				min += item
    			else:
    				break
    		maximum = msg.replace(f"{min} ", "")
    		maximum, min = int(maximum), int(min)
    		if maximum < min:
    			await send("📝 Первое число диапазона должно быть меньше второго")
    		if maximum == min:
    			await send(f"{Emoji.blocknot.value} Результат оказался совершенно непредсказуемый, ни за что не поверите, но случайное число из диапазона [{min}..{min}] выпало на {min}\nДа, все в шоке и нет слов")
    		else:
    			result = random.randint(min, maximum)
    			await send(f"{Emoji.cubik.value} Случайное число из диапазона [{min}..{maximum}] выпало на {result}")
    #повысить
    if startInList(text.upper(), povisit)[0]:
    	DKpovisit = botData["DKpovisit"]
    	moderRank = loadJson(f"chats/{message.from_user.id}.json")
    	moderRank = moderRank["rank"]
    	if DKpovisit > moderRank:
    		await send(f"{Emoji.blocknot.value} команда доступна только с ранга с ранга {eval('rank'+str(DKpovisit))[0]} ({DKpovisit})\nОграничено: «Назначение модераторов»")
    		return
    	if message.reply_to_message:
    		file = f"{message.reply_to_message.from_user.id}.json"
    		rank = text.upper().replace(startInList(text.upper(), povisit)[1], "")
    		rank = int(rank)
    		userData = loadJson(f"chats/{file}")
    		if userData["rank"] >= rank:
    			await send("📝 Модератор уже на этой должности или выше")
    		elif 1 > rank:
    			await send("📝 Ранк модератора должен быть больше 0")
    		else:
    			userData["rank"] = rank
    			saveJson(f"chats/{file}", userData)
    			rank = "rank" + str(rank)
    			nick = userData["nick"]
    			userId = userData["Id"]
    			nick = markdown.hlink(nick, f"tg://openmessage?user_id={userId}")
	    		await send(f"{Emoji.galochka.value} {nick} назначен {eval(rank)[3]}", parse_mode="HTML")
	    #По юзернейму/айди
    	else:
    		other = text[len(startInList(text.upper(), povisit)[1])+1:]
    		rank = int(other[0])
    		user = other[len(str(rank))+1:]
    		
    		if user[1] in list("123456789"):
    			userData = loadJson(f"chats/{user}.json")
    			isId = True
    		else:
    			user = user.replace(" ", "")
    			user = username2id(user)
    			if user == False:
    				send("📝 Нет информации о пользователе")
    			else:
    				if not isId:
    					userData = loadJson(f"chats/{user}.json")
	    			userId = userData["Id"]
	    			nick = userData["nick"]
	    			nick = markdown.hlink(nick, f"tg://openmessage?user_id={userId}")
	    		if userData["rank"] >= rank:
	    			await send("📝 Ранк модератора не может быть отрицательным")
	    		elif 0 > rank:
	    			await send("📝 Ранк модератора не может быть отрицательным")
	    		else:
	    			userData["rank"] = rank
	    			saveJson(f"chats/{user}.json", userData)
	    			rank = "rank" + str(rank)
		    		await send(f"{Emoji.galochka.value} {nick} назначен {eval(rank)[3]}", parse_mode="HTML")
    		
    			
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True) 
	bot.run()