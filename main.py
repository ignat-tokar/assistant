# Функции для работы с речью
from voice import listen
from voice import talk
from voice import Microphone

# Функции для работы с базой данных
from data_base import create_table_db
from data_base import insert_variable_into_table
from data_base import get_variable_all
from data_base import get_variable_by_id
from data_base import delete_variable_by_id

# Модули для работы с графическим интерфейсом
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


Builder.load_string("""
<MainScreen>:
	command: command_text
	voice: voice_text
	microphone_status: status_label
	BoxLayout:
    	padding: 40
    	spacing: 20
    	orientation: 'vertical'
    	Label:
    		id: status_label
    		color: [0,0,0,1]
    		text: 'Микрофон выключен'
    	TextInput:
    		size_hint: 0.8, 0.5
    		pos_hint: {'center_x':0.5,'center_y': 0.5}
    		id: command_text
    		hint_text: 'Введите команду bash'
    	TextInput:
    		size_hint: 0.8, 0.5
    		pos_hint: {'center_x':0.5,'center_y': 0.5}
    		id: voice_text
    		hint_text: 'Введите голосовую команду для ассистента'
    	Button:
    		background_color: [0.6,0.6,0.6,1]
    		size_hint: 0.8, 0.5
    		pos_hint: {'center_x':0.5,'center_y': 0.5}    	
    		text: 'Сохранить'
    		on_press: root.save()
    	Button:
    		background_color: [0.6,0.6,0.6,1]
    		size_hint: 0.8, 0.5
    		pos_hint: {'center_x':0.5,'center_y': 0.5}   
    		text: 'Включить микрофон'
    		on_press: root.pressed()
    		on_release: root.start_microphone()
        Button:
        	background_color: [0.6,0.6,0.6,1]
    		size_hint: 0.8, 0.5
    		pos_hint: {'center_x':0.5,'center_y': 0.5}        
            text: 'Все сохраненные команды'
            on_press: root.manager.current = 'list'

<ListScreen>:
	commands: command_label
    BoxLayout:
    	padding: 40
    	spacing: 20
    	orientation: 'vertical'
    	Label:
    		size_hint: 1, 0.6
    		color: [0,0,0,1]    		
    		id: command_label
    		text: 'Все сохраненные команды:'
    	BoxLayout:
    		size_hint: 1, 0.4
    		orientation: 'vertical'
    		spacing: 20
    		Button:
    		    background_color: [0.6,0.6,0.6,1]
    			size_hint: 0.8, 1
    			pos_hint: {'center_x':0.5, 'center_y': 0.5}
    			text: 'Удалить последнюю команду'
    			on_press: root.delete_command()
	    	Button:
    		    background_color: [0.6,0.6,0.6,1]	    	
	    		size_hint: 0.8, 1
	    		pos_hint: {'center_x':0.5, 'center_y': 0.5}    	
	    		text: 'Вывести все сохраненные команды'
	    		on_press: root.all_commands()
	        Button:
    		    background_color: [0.6,0.6,0.6,1]	        
	    		size_hint: 0.8, 1
	    		pos_hint: {'center_x':0.5, 'center_y': 0.5}        
	            text: 'Вернуться на главный экран'
	            on_press: root.manager.current = 'main'
""")


# Класс для реализации функций кнопок главного экрана
class MainScreen(Screen):

	# Объект для работы с микрофоном
	microphone = Microphone()
	# Функция сохранения команд в базу данных (нажатие на кнопку "Сохранить")
	def save(self):
		# Определяем id новой команды
		command_id = len(get_variable_all())+1
		# Проверяем заполнены ли оба поля
		if self.command.text and self.voice.text:
			# Добавляем новый элемент в базу данных
			insert_variable_into_table(command_id,
				self.command.text,
				self.voice.text)

	# Функция, которая вызываеться после нажатия на кнопку "Включить микрофон"
	def pressed(self):
		# Изменение содержимового текстовой метки, которая сообщает о
		# статусе микрофона
		self.microphone_status.text = '''Микрофон включен

Чтобы выключить - скажите "Выключи микрофон"'''

	# Фукнкция, которая непосредственного запускает микрофн
	def start_microphone(self):
		# Запуск микрофона
		self.microphone.start_microphone()
		# Если микрофон был выключен меняем текст метки статуса
		self.microphone_status.text = 'Микрофон выключен'


# Класс для работы с содержимым экрана для вывода всех сохраненных команд
class ListScreen(Screen):

	# Функция вызываеться после нажатия на кнопку
	# "Вывести все сохраненные команды"
    def all_commands(self):
    	# Обнуление содержимого текстовой метки
    	self.commands.text = 'Все сохраненные команды:\n'
    	# Извлечение все элементов сохраненных в базе данных
    	for command in get_variable_all():
    		# Добавление текста голосовой команды к содержимому текстовой метки
    		self.commands.text = self.commands.text + '\n' + command[2]

    # Функция вызывается после нажатия на кнопку
    # "Удалить последнюю команду"
    def delete_command(self):
    	# Находим id последнего элемента в базе данных
    	size = len(get_variable_all())
    	# Удаляем элементы
    	delete_variable_by_id(size)
    	# Обновляем содержимое текстовой метки
    	self.all_commands()


class TestApp(App):

    def build(self):
    	# Создание менеджера экранов
        sm = ScreenManager()
        # Добавление экранов в базу менеджера экранов
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ListScreen(name='list'))
        # Установка белого цвета для окно приложения
        Window.clearcolor = (1,1,1,1)
        return sm


if __name__ == '__main__':
    TestApp().run()
