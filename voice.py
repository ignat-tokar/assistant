# Импорт модулей для работы с системой и распознования речи
import speech_recognition as sr
import os
import sys

# Импорт модулей для озвучивания речи
from gtts import gTTS
import pyttsx3

# Импорт функций для работы с базой данных
from data_base import create_table_db
from data_base import insert_variable_into_table
from data_base import get_variable_all
from data_base import get_variable_by_id
from data_base import delete_variable_by_id

# Функция для озвучивания текста
def talk(words):
	os.system('echo ' + words + ' | RHVoice-client -s Anna+CLB -r 0.1  | aplay')
	print(words)


# Функция, которая будеть осуществлять слушание голоса пользователя
def listen():
	# Объэкт для настроек считывания
	r = sr.Recognizer()
	# Получение записи из микрофона
	with sr.Microphone() as source:
		talk("Говорите я слушаю:")
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration = 1)
		audio = r.listen(source)
	# Попытка считать данные из того, что получили
	try:
		text = r.recognize_google(audio, language = 'ru-RU').lower()
	# Обработка ошибки, если пользователь произнес что-то непонятное
	except sr.UnknownValueError:
		talk("Я вас не поняла, пожалуйста повторите:")
		# Перезапуск функции
		text = listen()

	return text


# Объект для работы с микрофоном
class Microphone():

	# Функции, которая выполняе полученную команду
	def makeSomething(self, said):
		# Сбор все элементов из базы данных
		commands = get_variable_all()
		for command in commands:
			# Проверка на совпадение сказанного и команды из базы данных
			if said in command[2]:
				# Если совпадение обнаружено - осуществляеться команда,
				# которая соответствует голосовому запросу
				os.system(command[1])
				return True
			# Проверка не хочет ли пользователь выключить телефон
			elif 'выключи микрофон' in said:
				talk('Выключаю микрофон')
				return False	

	# Функция, которая запускает процесс "слушания" пользователя
	def start_microphone(self):
		# Переключатель, для выключения микрофона в случае необходимости
		on_off = True
		while on_off:
			on_off = self.makeSomething(listen())