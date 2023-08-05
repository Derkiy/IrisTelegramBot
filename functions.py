import json, os, datetime
def startInList(text: str, getList: list):
	done = False
	for item in getList:
		if text.startswith(item):
			return True, item
			done = True
	if not done:
		return False, "0"

def toSymbol(text: str, symbol: str):
	newText = ""
	for item in text:
		if item == symbol:
			break
		else:
			newText+=item
	return newText

def loadJson(dir: str):
		with open(dir) as fh:
			data = json.load(fh)
		return data

def saveJson(dir: str, data):
	data = json.dumps(data, indent=4)
	with open(dir, "w") as fh:
		fh.write(data)

def username2id(username: int or str):
	userId = "" if type(username) == str else 1
	if type(username) == str:
		username = username.replace(" ", "")
		username = username.replace("@", "")
	if type(username) == str:
		for file in os.listdir("chats"):
			data = loadJson(f"chats/{file}")
			if data["Username"] == username:
				userId = data["Id"]
		if type(userId) == str:
			return False
		else:
			return userId
	else:
		for file in os.listdir("chats"):
			data = loadJson(file)
			if data["Id"] == username:
				userId = data["Username"]
		if type(userId) == int:
			return False
		else:
			return userId

def updateJson(user):
	data = loadJson(f"chats/{user.id}.json")
	if user.username != data["Username"]:
		data["Username"] = user.username
	if data["nick"] != user.full_name and not data["CustomNick"]:
		data["nick"] = user.full_name
	saveJson(dir=f"chats/{user.id}.json", data=data)
	
def toDate(text: str):
	text = text.replace(":", " ").replace(".", " ")
	dateList = list(text.split(" "))
	for i in dateList:
		if i == " " or i == "":
			dateList.remove(i)
	newList = []
	for i in dateList:
		newList.append(int(i))
	while len(newList) != 6:
		newList.append(0)
	return datetime.datetime(newList[0], newList[1], newList[2], newList[3], newList[4], newList[5])

def t2s(time):
    time_str = time.lower().strip()
    time_units = {
        "минута": 60,
        "минут": 60,
		"мн": 60,
        "час": 3600,
        "ч": 3600,
        "часов": 3600,
        "часа": 3600,
        "день": 86400,
        "дней": 86400,
		"дн": 86400,
		"дня": 86400,
        "неделя": 604800,
        "недели": 604800,
        "недель": 604800,
		"нд": 604800,
        "месяц": 2629800,
        "месяцев": 2629800,
        "месяца": 2629800,
    }

    try:
        value, unit = time_str.split()
        value = int(value)
        if unit not in time_units:
            raise ValueError
        return datetime.datetime.now() + datetime.timedelta(seconds=value * time_units[unit])
    except (ValueError, KeyError):
        raise ValueError("Ошибка!")