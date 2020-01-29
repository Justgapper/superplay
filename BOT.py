# -*- coding: utf-8 -*-
import telebot
from sqlite3 import *
from telebot import types
from random import randint
from time import sleep
 
playersDB = "db\\players.db"
itemsDB = "db\\items.db"
deniedWords = "хуила,архипиздрит,басран,бздение,бздеть,бздех,бзднуть,бздун,бздунья,бздюха,бикса,блежник,блудилище,бляд,блябу,блябуду,блядун,блядунья,блядь,блядюга,взьебка,волосянка,взьебывать,взебывать,выблядок,выблядыш,выебать,выеть,выпердеть,высраться,выссаться,говенка,говенный,говешка,говназия,говнецо,говно,говноед,говночист,говнюк,говнюха,говнядина,говняк,говняный,говнять,гондон,дермо,долбоеб,дрисня,дрист,дристать,дристануть,дристун,дристуха,дрочена,дрочила,дрочилка,дрочить,дрочка,ебало,ебальник,ебануть,ебаный,ебарь,ебатория,ебать,ебаться,ебец,ебливый,ебля,ебнуть,ебнуться,ебня,ебун,елда,елдак,елдачить,заговнять,задристать,задрока,заеба,заебанец,заебать,заебаться,заебываться,заеть,залупа,залупаться,залупить,залупиться,замудохаться,засерун,засеря,засерать,засирать,засранец,засрун,захуячить,злоебучий,изговнять,изговняться,кляпыжиться,курва,курвенок,курвин,курвяжник,курвяжница,курвяжный,манда,мандавошка,мандей,мандеть,мандища,мандюк,минет,минетчик,минетчица,мокрохвостка,мокрощелка,мудак,муде,мудеть,мудила,мудистый,мудня,мудоеб,мудозвон,муйня,набздеть,наговнять,надристать,надрочить,наебать,наебнуться,наебывать,нассать,нахезать,нахуйник,насцать,обдристаться,обдристаться,обосранец,обосрать,обосцать,обосцаться,обсирать,опизде,отпиздячить,отпороть,отъеть,охуевательский,охуевать,охуевающий,охуеть,охуительный,охуячивать,охуячить,педрик,пердеж,пердение,пердеть,пердильник,перднуть,пердун,пердунец,пердунина,пердунья,пердуха,пердь,передок,пернуть,пидор,пизда,пиздануть,пизденка,пиздеть,пиздить,пиздища,пиздобратия,пиздоватый,пиздорванец,пиздорванка,пиздострадатель,пиздун,пиздюга,пиздюк,пиздячить,писять,питишка,плеха,подговнять,подъебнуться,поебать,поеть,попысать,посрать,поставить,поцоватый,презерватив,проблядь,проебать,промандеть,промудеть,пропиздеть,пропиздячить,пысать,разъеба,разъебай,распиздай,распиздеться,распиздяй,распроеть,растыка,сговнять,секель,серун,серька,сика,сикать,сикель,сирать,сирывать,скурвиться,скуреха,скурея,скуряга,скуряжничать,спиздить,срака,сраный,сранье,срать,срун,ссака,ссаки,ссать,старпер,струк,суходрочка,сцавинье,сцака,сцаки,сцание,сцать,сциха,сцуль,сцыха,сыкун,титечка,титечный,титка,титочка,титька,трипер,триппер,уеть,усраться,усцаться,фик,фуй,хезать,хер,херня,херовина,херовый,хитрожопый,хлюха,хуевина,хуевый,хуек,хуепромышленник,хуерик,хуесос,хуище,хуй,хуйня,хуйрик,хуякать,хуякнуть,целка,шлюха".split(",")
token = "937508396:AAGLapcfG5X4I8IzZwVKqRM4H48PPd8ZnLw"
bot = telebot.TeleBot(token)

id = 0 
minNameLen = 3
maxNameLen = 20
 
playersDBConnection = connect(playersDB, check_same_thread=False)
playersDBCursor = playersDBConnection.cursor()
"""
class Quest:
	def __init__(self,id,reward,complete_options):
		self.id = id
		self.reward = reward
		self.complete_options = complete_options
	def start(self, hero_id):
		launched_quests = (cursor.execute("SELECT launched_quests FROM players WHERE id=?",(hero_id,))).fetchone()[0] + " " + self.id
		playersDBCursor.execute("UPDATE players SET launched_quests=? WHERE id=?", (launched_quests, hero_id,))
	def complete(self, hero_id, reward):
"""



@bot.message_handler(commands=['start'])
def register_user(message):
	if str(message.chat.id) in [x for y in playersDBCursor.execute("SELECT id FROM players") for x in y]:
		bot.send_message(message.chat.id, "Вы уже зарегистрированы")
	else:
		bot.send_message(message.chat.id, "Начинаем регистрацию...")
		sleep(3)
		playersDBCursor.execute("INSERT INTO players (id,name,status,level,completed_quests,launched_quests) VALUES (?,?,?,?,?,?)", (message.chat.id, "unnamed", "not_registered", 1,"",""))
		bot.send_message(message.chat.id, "Для завершения регистрации напишите /setname и ваш ник. \nНапример: /setname Кактус")
		playersDBConnection.commit()

@bot.message_handler(commands=['setname'])
def setname(message):

	name = (message.text+" "+"unnamed").split()[1]

	if playersDBCursor.execute("SELECT status FROM players WHERE id=?",(message.chat.id,)).fetchone()[0] != "rest" and playersDBCursor.execute("SELECT status FROM players WHERE id=?",(message.chat.id,)).fetchone()[0] != "not_registered":
		bot.send_message(message.chat.id,"Вы не можете использовать это сейчас")

	elif name == "unnamed":
		bot.send_message(message.chat.id, "Пожалуйста, напишите желаемое имя после команды\nНапример: /setname Кактус")

	elif len(str(name)) >= minNameLen and name not in deniedWords and len(str(name)) <= maxNameLen:
		playersDBCursor.execute("UPDATE players SET name=? WHERE id=?", (name, message.chat.id))
		playersDBCursor.execute("UPDATE players SET status=? WHERE id=?", ("rest", message.chat.id))
		playersDBConnection.commit()
		bot.send_message(message.chat.id, "Имя сохранено!", reply_markup=defaultKB())

	else:
		bot.send_message(message.chat.id, f"Некорректное имя, проверьте, что:\nВаше имя не содержит пробелов\nИмя содержит более 3 символов\nИмя не содержит нецензурную брань(мат, оскорбления)\nИмя содержит менее 20 символов")
 
@bot.message_handler(commands=['deleteuser'])
def deleteuser(message):

	bot.send_message(message.chat.id,"Пользователь удален", reply_markup=RemoveKB())
	playersDBCursor.execute("DELETE FROM players WHERE id=? ", (message.chat.id,))
	playersDBConnection.commit()
 
@bot.message_handler(commands=['myname'])
def myname(message):
	if str(message.chat.id) in [x for y in playersDBCursor.execute("SELECT id FROM players") for x in y]:
		bot.send_message(message.chat.id,"Ваш ник:"+playersDBCursor.execute("SELECT name FROM players WHERE id=?",(message.chat.id,)).fetchone()[0])
	else:
		bot.send_message(message.chat.id, "Вы ещё не зарегистрированы")
@bot.message_handler(commands=['kbd'])
def myname(message):
	bot.send_message(message.chat.id, "Удалено", reply_markup=RemoveKB())

@bot.message_handler(commands=['kba'])
def myname(message):
	bot.send_message(message.chat.id, "Добавленно", reply_markup=defaultKB())

@bot.message_handler(content_types=["text"])
def take_message(message):
	try:
		msg = message.text
		if str(message.chat.id) not in [x for y in playersDBCursor.execute("SELECT id FROM players") for x in y]:
			bot.send_message(message.chat.id, "Вы ещё не зарегистрировавны, напишите /start")
		elif playersDBCursor.execute("SELECT status FROM players WHERE id=?",(message.chat.id,)).fetchone()[0] == "rest":

			if msg == 'Герой':
				level = playersDBCursor.execute("SELECT level FROM players WHERE id=?",(message.chat.id,)).fetchone()[0]
				name = playersDBCursor.execute("SELECT name FROM players WHERE id=?",(message.chat.id,)).fetchone()[0]
				bot.send_message(message.chat.id,f"Информация о герое\nбла бла бла\n{name}\nУровень:{level}", reply_markup=defaultKB())

			elif msg == 'Локации':
				bot.send_message(message.chat.id,"Перемещение между локациями", reply_markup=defaultKB())

			elif msg == 'Инвентарь':
				bot.send_message(message.chat.id,"Инвентарь", reply_markup=defaultKB())

			elif msg == 'PVP':
				bot.send_message(message.chat.id,"Вход в режим пвп", reply_markup=pvpKB())
				playersDBCursor.execute("UPDATE players SET status=? WHERE id=?", ("pvp", message.chat.id))

			else:
				bot.send_message(message.chat.id,"Вы не можете использовать это сейчас")

		elif playersDBCursor.execute("SELECT status FROM players WHERE id=?",(message.chat.id,)).fetchone()[0] == "pvp":
			if msg == "Покинуть пвп":
				bot.send_message(message.chat.id,"Вы покинули пвп", reply_markup=defaultKB())
				playersDBCursor.execute("UPDATE players SET status=? WHERE id=?", ("rest", message.chat.id))

			else:
				bot.send_message(message.chat.id,"Вы не можете использовать это сейчас, сначала выйдите из пвп")

	except:
		try:
			bot.send_message(message.chat.id, f"Сообщение '{msg}' вызвало ошибку, пожалуйста, сообщите администрации")
		except:
			pass


def defaultKB():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	markup.row(types.KeyboardButton('Герой'), types.KeyboardButton('Локации'))
	markup.row(types.KeyboardButton('Инвентарь'), types.KeyboardButton('PVP'))
	return markup

def pvpKB():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	markup.row(types.KeyboardButton('Покинуть пвп'))
	return markup

def RemoveKB():
	return types.ReplyKeyboardRemove()



bot.polling(none_stop=True)