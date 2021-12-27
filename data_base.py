# Импортирование модуля для работы с базой данных
import sqlite3


# Cоздание новой таблицы в базе данных
def create_table_db():
    try:
        # Попытка подключения к базе данных
        sqlite_connection = sqlite3.connect('commands.db')
        # Создание SQL-запроса для отправки в базу данных
        sqlite_create_table_query = '''CREATE TABLE commands_table (
                                    id INTEGER PRIMARY KEY,
                                    command TEXT NOT NULL,
                                    voice text NOT NULL UNIQUE);'''
        # Получение курсора для отправки данных в БД
        cursor = sqlite_connection.cursor()
        # Отправка SQL-запроса в БД
        cursor.execute(sqlite_create_table_query)
        # Сохранение данных в БД
        sqlite_connection.commit()
        # Отключение курсора
        cursor.close()
    except sqlite3.Error as error:
        # Вывод ошибки в случае нудачного подключения к БД
        print("Ошибка при подключении к sqlite", error)
    finally:
        # Если соеденение все еще работает
        if (sqlite_connection):
            # Отключаем соеденение
            sqlite_connection.close()


# Запись данных в БД
def insert_variable_into_table(command_id, command, voice):
    try:
        # Подключение к базе данных
        sqlite_connection = sqlite3.connect('commands.db')
        # Получение курсора для передачи SQL-запроса
        cursor = sqlite_connection.cursor()
        # Создание SQL-запроса
        sqlite_insert_with_param = """INSERT INTO commands_table
                              (id, command, voice)
                              VALUES (?, ?, ?);"""
        # Добавление данных для SQL-запроса
        data_tuple = (command_id, command, voice)
        # Отправка данных
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        # Отключение курсора
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        # Отключение соеденения с базой данных
        if sqlite_connection:
            sqlite_connection.close()


# Извлеченные полей из БД
def get_variable_all():
    # Создание переменной для хранения результата
    all_results = []
    try:
        # Подключение к БД
        sqlite_connection = sqlite3.connect('commands.db')
        cursor = sqlite_connection.cursor()
        # Создание SQL-запроса
        sqlite_get = """SELECT * FROM commands_table;"""
        # Передача SQL-запроса
        cursor.execute(sqlite_get)
        # Получение результата
        all_results = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        # Отключение соеденения
        if sqlite_connection:
            sqlite_connection.close()
    # Отправка резyльтата
    return all_results


# Извлечение поля из БД
def get_variable_by_id(command_id):
    # Создание переменной для отправки результата
    all_results = []
    try:
        # Подключение к БД
        sqlite_connection = sqlite3.connect('commands.db')
        cursor = sqlite_connection.cursor()
        # Извлечение из БД всех элементов с полученным id
        sqlite_get = "SELECT * FROM commands_table WHERE id=" + str(command_id) + ";"
        cursor.execute(sqlite_get)
        # Получение результата
        all_results = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        # Отключение соединения
        if sqlite_connection:
            sqlite_connection.close()
    # Отправка результата
    return all_results


# Удаление полей из БД
def delete_variable_by_id(command_id):
    try:
        # Подключение к БД
        sqlite_connection = sqlite3.connect('commands.db')
        cursor = sqlite_connection.cursor()
        # Формирование SQL-запроса
        sqlite_get = "DELETE FROM commands_table WHERE id=" + str(command_id) + ";"
        # Отправка SQL-запроса
        cursor.execute(sqlite_get)
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        # Отключение соеденения
        if sqlite_connection:
            sqlite_connection.close()
