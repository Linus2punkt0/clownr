# -*- coding: utf-8 -*-
from twython import Twython, TwythonError
from datetime import date, datetime, timedelta
from django.http import HttpResponse
from random import choice
from codecs import lookup
import pandas as pd
import random, time, os
import json
import re

APP_KEY = ""
APP_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

myAccount = ""
targets= []

incoming = pd.DataFrame(columns = ["user", "tweetid", "timestamp"])
outgoing = pd.DataFrame(columns = ["user", "timestamp"])

logpath = "logs/"
imagepath = r"images/"
listpath = "lastUsed"
spongebob = "Mocking-Spongebob.jpg"

def getImageName():
	random_filename = random.choice([
		x for x in os.listdir(imagepath)
		if os.path.isfile(os.path.join(imagepath, x))
	])
	return random_filename


def getImage():
	img_count = 0
	for path in os.listdir(imagepath):
		if os.path.isfile(os.path.join(imagepath, path)):
			img_count += 1
	with open(listpath, 'r+') as file:
		lines = len(file.readlines())
		if img_count <= lines:
			file.truncate(0)
	random_filename = getImageName()
	with open(listpath, 'r') as file:
		content = file.read()
		while random_filename in content:
			random_filename = getImageName()
	dst = open(listpath, 'a')
	dst.write(random_filename + '\n')
	dst.close()
	return imagepath + random_filename

def sendReply(tweetid, text):
	status = ''
	x = random.randint(0,5)
	if len(text) > 10 and len(text) < 80 and x < 2:
		photo = open(spongebob, 'rb')
		text = " ".join(filter(lambda x:x[0]!='@', text.split()))
		status = ''.join(char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(text, 1))
	else:
		photo = getImage()
		photo = open(photo, 'rb')
	response = twitter.upload_media(media=photo)
	try:
		a = twitter.update_status(status=status, media_ids=[ response['media_id']], in_reply_to_status_id=tweetid, auto_populate_reply_metadata=True)
		return "Success!"
	except TwythonError as e:
		return "Error!" + e

def writeLog(message):
	now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	date = datetime.now().strftime("%y%m%d")
	message = str(now) + ": " + message + "\n"
	log = logpath + date + ".log"
	if os.path.exists(log):
		append_write = 'a'
	else:
		append_write = 'w'
	dst = open(log, append_write)
	dst.write(message)
	dst.close()


yday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
for user in targets:
	tweets = twitter.cursor(twitter.search, q='from:' + user + ' to:' + myAccount + ' since:' + yday)
	for tweet in tweets:
		tweetid = tweet["id"]
		user = (tweet["user"])["screen_name"]
		text = re.sub(r'http\S+', '', (tweet["text"].replace(myAccount + ' ', '')))
		timestamp = tweet["created_at"].replace("+0000 ", "")
		timestamp = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
		if user in targets and user not in incoming.values and (datetime.utcnow() - timestamp < timedelta(hours=2)):
			row = {"user": user, "tweetid": tweetid, "timestamp": timestamp, "text": text}
			incoming = incoming.append(row, ignore_index = True)

if not incoming.empty:

	sent = twitter.get_user_timeline();
	for tweet in sent:
		if tweet["retweeted"] == False:
			user = (tweet["entities"])["user_mentions"]
			if user:
				user = user[0]["screen_name"]
				timestamp = tweet["created_at"].replace("+0000 ", "")
				timestamp = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
				if user in incoming.values and  user not in outgoing.values and (datetime.utcnow() - timestamp < timedelta(hours=2)):
					row = {"user": user, "timestamp": timestamp}
					outgoing = outgoing.append(row, ignore_index = True)

	for idx, row in incoming.iterrows():
		user = row["user"]
		timestamp = row["timestamp"]
		tweetid = row["tweetid"]
		text = row["text"]
		replytime = outgoing.loc[outgoing["user"] == user, "timestamp"]
		if not replytime.empty:
			if replytime.iloc[0] < timestamp:
				response = sendReply(tweetid, text)
				print("Reply sent to " + user + " (" + str(tweetid) + ")")
				writeLog("Reply sent to " + user + " (" + str(tweetid) + ")")
				writeLog(response)
			else:
				print("Found tweet by " + user + " (" + str(tweetid) + "), but it had already been replied to.")
				writeLog("Found tweet by " + user + " (" + str(tweetid) + "), but it had already been replied to.")
		else:
			response = sendReply(tweetid, text)
			print("Reply sent to " + user + " (" + str(tweetid) + ")")
			writeLog("Reply sent to " + user + " (" + str(tweetid) + ")")
			writeLog(response)
else:
	print("No replies from selected users found.")
	writeLog("No replies from selected users found.")
