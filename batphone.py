import time, json, urllib.request, pickle

lastread = 0

events = {"Aether Flares Around",
	"Rikenfriez Blizzard!",
	"Dairuchi Celebrations",
	"The Mountain Wars and the Undervault Struggles",
	"Hemp Wars",
	"Orc-Furrikin Wars",
	"Aslaran-Krokani Feud",
	"Political Upheaval",}

def get_politics():
	global lastread
	with urllib.request.urlopen("https://api.lusternia.com/news/politics.json?page=100000") as url:
		data = json.loads(url.read().decode())
		
	post = data["news"][0]
	timesince = time.time()-post["date"]
	
	isevent = False
	for x in events:
		if x in post["subject"]:
			isevent = True
	
	if post["id"] > lastread and isevent and timesince < 600:
		print(post["subject"])
		lastread = post["id"]