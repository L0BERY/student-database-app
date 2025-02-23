import sqlite3
import hashlib
import os

class Student():
    def authorize(user_app):
        if user_app == None or user_app[1] == 2: 
            print('У вас нет доступа, авторизуйтесь на главной странице меню')
            input('Нажмите для выхода')
            return 1
        return 0
    
    def error():
        print('Какие-то данные введены неверно')
        input('Нажмите для выхода')
        return 1
    
    def check_year(year):
        year = int(year) if year.isdigit() else 0
        if 2015 > year or year > 2025: 
            Student.error()
            return 1
        return 0
    
    def check_form(form):
        if not (form in ['дневная', 'вечерняя', 'заочная']):
            Student.error()
            return 1
        return 0
    
    def check_group(group):
        group = int(group) if group.isdigit() else -1
        if 0 > group or group > 10000: 
            Student.error()
            return 1
        return 0
        
    def find_user(cursor):
        name = input('Введите ФИО студента (для просмотра всех студентов нажмите Enter): ')
        cursor.execute(f'''SELECT * FROM Students WHERE full_name LIKE '%{name}%' ''')
        users = cursor.fetchall()
        if not len(users):
            UchPlan.not_found()
            return None
        print(f'Найденные пользователи ({len(users)}): ')
        for i, user in enumerate(users):
            print(f'{i}) {user[1]} | Год поступления: {user[2]} | Форма обучения: {user[3]} | Номер группы: {user[4]}')
        print()
        ch = input('Выберите нужного студента: ')
        ch = int(ch) if ch.isdigit() else -1
        if ch < 0 or ch >= len(users):
            input('Неверный ввод, нажмите для выхода')
            return None
        return users[ch]
        
    def addNewStudent(connection, user_app):
        os.system('cls')
        if Student.authorize(user_app): return
        cursor = connection.cursor()
        print()
        name = input('Введите ФИО студента: ')
        year = input('Введите год начала обучения студента (2015-2025): ')
        if Student.check_year(year): return
        form = input('Введите форму обучения (дневная/вечерняя/заочная): ')
        if Student.check_form(form): return
        group = input('Введите номер группы студента: ')
        if Student.check_group(group): return
        cursor.execute('INSERT INTO Students (full_name, year_of_admission, form_of_education, num_group) VALUES (?, ?, ?, ?)', (name, year, form, group))
        connection.commit()
        input(f'Студент {name} добавлен в базу, нажмите для выхода')
        return
    
    def delStudent(connection, user_app):
        os.system('cls')
        if Student.authorize(user_app): return
        cursor = connection.cursor()
        print()
        user = Student.find_user(cursor)
        if user is None: return
        cursor.execute('DELETE FROM Students WHERE id= ?', (user[0],))
        connection.commit()
        input(f'Студент {user[1]} удалён из базы, нажмите для выхода')
        return
    
    def updStudent(connection, user_app):
        os.system('cls')
        if Student.authorize(user_app): return
        cursor = connection.cursor()
        print()
        user = Student.find_user(cursor)
        if user is None: return
        print()
        print('Какие данные изменить?')
        print('1) ФИО')
        print('2) Год начала обучения')
        print('3) Форму обучения')
        print('4) Номер группы')
        print('5) Вернуться назад')
        print()
        v = input('Выберите вариант: ')
        v = int(v) if v.isdigit() else -1
        if v < 0 or v >= 5:
            input('Неверный ввод, нажмите для выхода')
            return
        match v:
            case 1:
                var = input('Введите новое ФИО студента: ')
                cursor.execute('UPDATE Students SET full_name= ? WHERE id= ?', (var, user[0]))
                connection.commit()
                return
            case 2:
                var = input('Введите новый год начала обучения студента: ')
                if Student.check_year(var): return
                cursor.execute('UPDATE Students SET year_of_admission= ? WHERE id= ?', (var, user[0]))
                connection.commit()
                return
            case 3:
                var = input('Введите новую форму обучения студента (дневная/вечерняя/заочная): ')
                if Student.check_form(var): return
                cursor.execute('UPDATE Students SET form_of_education= ? WHERE id= ?', (var, user[0]))
                connection.commit()
                return
            case 4:
                var = input('Введите новую группу студента: ')
                if Student.check_group(var): return
                cursor.execute('UPDATE Students SET num_group= ? WHERE id= ?', (var, user[0]))
                connection.commit()
                return
            case 5:
                return

    def spravka(connection):
        os.system('cls')
        cursor = connection.cursor()
        print()
        user = Student.find_user(cursor)
        if user is None: return
        cursor.execute(f'SELECT * FROM Uspevaemost WHERE studentID= ?', (user[0],))
        grades = cursor.fetchall()
        if not len(grades):
            print('У данного студента нет оценок')
            input('Нажмите для выхода')
            return None
        print(f'Найденные оценки ({len(grades)}): ')
        for i, grade in enumerate(grades):
            print(f'{i}) {grade[3]}: {grade[4]}')
        print()
        input('Нажмите для выхода')
        return
    
    def number_studens_form(connection):
        os.system('cls')
        cursor = connection.cursor()
        print()
        form = input('Введите форму обучения (дневная/вечерняя/заочная): ')
        if Student.check_form(form): return
        cursor.execute(f'SELECT COUNT(*) FROM Students WHERE form_of_education= ?', (form,))
        num = cursor.fetchall()
        print(f'Количество студентов: {num[0][0]}')
        print()
        input('Нажмите для выхода')
        
class UchPlan():
    def authorize(user_app):
        if user_app == None or user_app[1] == 2: 
            print('У вас нет доступа, авторизуйтесь на главной странице меню')
            input('Нажмите для выхода')
            return 1
        return 0
    
    def not_found():
        print('Ничего не найдено')
        input('Нажмите для выхода')
    
    def check_otchet(otchet):
        if not (otchet in ['экзамен', 'зачет']):
            Student.error()
            return 1
        return 0
    
    def find_disc(cursor):
        name = input('Введите название дисциплины (для просмотра всех дисциплин нажмите Enter): ')
        cursor.execute(f'''SELECT * FROM UchPlan WHERE discipline LIKE '%{name}%' ''')
        disciplines = cursor.fetchall()
        if not len(disciplines):
            UchPlan.not_found()
            return None
        print(f'Найденные дисциплины ({len(disciplines)}): ')
        for i, discipline in enumerate(disciplines):
            print(f'{i}) {discipline[2]} | Семестр: {discipline[3]}')
        print()
        ch = input('Выберите нужную дисциплину: ')
        ch = int(ch) if ch.isdigit() else -1
        if ch < 0 or ch >= len(disciplines):
            input('Неверный ввод, нажмите для выхода')
            return None
        return disciplines[ch]
    
    def addNewDisc(connection, user_app):
        os.system('cls')
        if UchPlan.authorize(user_app): return
        cursor = connection.cursor()
        print()
        name_spec = input('Введите название специальности: ')
        name_disc = input('Введите название дисциплины: ')
        sem = input('Введите семестр (1-12): ')
        if Uspev.check_sem(sem): return
        time = input('Введите количество часов: ')
        time = int(time) if time.isdigit() else 1000
        if 0 > time or time > 500: 
            Student.error()
            return
        otchet = input('Введите вид отчётности (экзамен/зачет): ')
        if UchPlan.check_otchet(otchet): return
        cursor.execute('INSERT INTO UchPlan (spec_name, discipline, semester, time, otchet) VALUES (?, ?, ?, ?, ?)', (name_spec, name_disc, sem, time, otchet, ))
        connection.commit()
        input(f'Дисциплина {name_disc} по специальности {name_spec} добавлена в базу, нажмите для выхода')
        return
    
    def updDisc(connection, user_app):
        os.system('cls')
        if UchPlan.authorize(user_app): return
        cursor = connection.cursor()
        print()
        discipline = UchPlan.find_disc(cursor)
        if discipline is None: return
        print()
        print('Какие данные изменить?')
        print('1) Название специальности')
        print('2) Название дисциплины')
        print('3) Семестр')
        print('4) Количество часов')
        print('5) Форма отчётности')
        print('6) Вернуться назад')
        print()
        v = input('Выберите вариант: ')
        v = int(v) if v.isdigit() else -1
        if v < 0 or v > 5:
            input('Неверный ввод, нажмите для выхода')
            return
        match v:
            case 1:
                var = input('Введите новое название специальности: ')
                cursor.execute('UPDATE UchPlan SET spec_name= ? WHERE courseID= ?', (var, discipline[0], ))
                connection.commit()
                return
            case 2:
                var = input('Введите новое название дисциплины: ')
                cursor.execute('UPDATE UchPlan SET discipline= ? WHERE courseID= ?', (var, discipline[0], ))
                connection.commit()
                return
            case 3:
                var = input('Введите семестр (1-12): ')
                if Uspev.check_sem(var): return
                cursor.execute('UPDATE UchPlan SET semester= ? WHERE courseID= ?', (var, discipline[0], ))
                connection.commit()
                return
            case 4:
                var = input('Введите количество часов: ')
                var = int(var) if var.isdigit() else 1000
                if 0 > var or var > 500: 
                    Student.error()
                    return
                cursor.execute('UPDATE UchPlan SET time= ? WHERE courseID= ?', (var, discipline[0], ))
                connection.commit()
                return
            case 5:
                var = input('Введите форму отчётности (экзамен/зачет): ')
                if UchPlan.check_otchet(var): return
                cursor.execute('UPDATE UchPlan SET otchet= ? WHERE courseID= ?', (var, discipline[0], ))
                connection.commit()
                return
            case 6:
                return
    
    def delDisc(connection, user_app):
        os.system('cls')
        if UchPlan.authorize(user_app): return
        cursor = connection.cursor()
        print()
        discipline = UchPlan.find_disc(cursor)
        if discipline is None: return
        cursor.execute('DELETE FROM UchPlan WHERE courseID= ?', (discipline[0],))
        connection.commit()
        input(f'Дисциплина {discipline[1]} удалёна из базы, нажмите для выхода')
        return

    def form_and_time(connection):
        os.system('cls')
        cursor = connection.cursor()
        discipline = UchPlan.find_disc(cursor)
        if discipline is None: return
        print()
        cursor.execute(f'SELECT time, otchet FROM UchPlan WHERE courseID= ?', (discipline[0],))
        data = cursor.fetchall()
        print(f'Количество часов: {data[0][0]} | Форма отчётности: {data[0][1]}')
        print()
        input('Нажмите для выхода')
        
class Uspev():
    def authorize(user_app):
        if user_app == None: 
            print('У вас нет доступа, авторизуйтесь на главной странице меню')
            input('Нажмите для выхода')
            return 1
        return 0
    
    def check_sem(sem):
        sem = int(sem) if sem.isdigit() else 0
        if 1 > sem or sem > 12: 
            Student.error()
            return 1
        return 0
    
    def check_grade(grade):
        grade = int(grade) if grade.isdigit() else 0
        if grade < 2 or grade > 5: 
            Student.error()
            return 1
        return 0
    
    def find_disc(cursor, sem):
        name = input('Введите название дисциплины (для просмотра всех дисциплин нажмите Enter): ')
        cursor.execute(f'''SELECT * FROM UchPlan WHERE discipline LIKE '%{name}%' AND semester= ?''', (sem,))
        disciplines = cursor.fetchall()
        if not len(disciplines):
            UchPlan.not_found()
            return None
        print(f'Найденные дисциплины ({len(disciplines)}) за {sem} семестр: ')
        for i, discipline in enumerate(disciplines):
            print(f'{i}) {discipline[2]}')
        print()
        ch = input('Выберите нужную дисциплину: ')
        ch = int(ch) if ch.isdigit() else -1
        if ch < 0 or ch >= len(disciplines):
            input('Неверный ввод, нажмите для выхода')
            return None
        return disciplines[ch]
    
    def find_grade(cursor, discipline, user):
        cursor.execute(f'SELECT * FROM Uspevaemost WHERE studentID= ? AND discipline= ?', (user[0], discipline[2],))
        grades = cursor.fetchall()
        if not len(grades):
            print('Оценки по этой дисциплине не найдены')
            input('Нажмите для выхода')
            return None
        print(f'Найденные оценки ({len(grades)}): ')
        for i, grade in enumerate(grades):
            print(f'{i}) {discipline[2]}: {grade[4]}')
        print()
        ch = input('Выберите оценку из списка, которую необходимо изменить: ')
        ch = int(ch) if ch.isdigit() else -1
        if ch < 0 or ch >= len(grades):
            input('Неверный ввод, нажмите для выхода')
            return None
        return grades[ch]
    
    def addNewGrade(connection, user_app):
        os.system('cls')
        if Uspev.authorize(user_app): return
        cursor = connection.cursor()
        print()
        user = Student.find_user(cursor)
        if user is None: return
        sem = input('Введите семестр: ')
        if Uspev.check_sem(sem): return
        discipline = Uspev.find_disc(cursor, sem)
        if discipline is None: return
        grade = input('Введите оценку (2-5): ')
        if Uspev.check_grade(grade): return
        grade = int(grade)
        cursor.execute('INSERT INTO Uspevaemost (semester, studentID, discipline, otmetka) VALUES (?, ?, ?, ?)', (sem, user[0], discipline[2], grade, ))
        connection.commit()
        input(f'Оценка {grade} поставлена студенту {user[1]}, нажмите для выхода')
        return
    
    def updGrade(connection, user_app):
        os.system('cls')
        if Uspev.authorize(user_app): return
        cursor = connection.cursor()
        print()
        user = Student.find_user(cursor)
        if user is None: return
        discipline = UchPlan.find_disc(cursor)
        if discipline is None: return
        grade = Uspev.find_grade(cursor, discipline, user)
        if grade is None: return
        print()
        new_grade = input('Введите новую оценку: ')
        if Uspev.check_grade(new_grade): return
        new_grade = int(new_grade)
        cursor.execute('UPDATE Uspevaemost SET otmetka= ? WHERE uspevID= ?', (new_grade, grade[0], ))
        connection.commit()
        print('Оценка изменена')
        return
    
    def delGrade(connection, user_app):
        os.system('cls')
        if Uspev.authorize(user_app): return
        cursor = connection.cursor()
        print()
        user = Student.find_user(cursor)
        if user is None: return
        discipline = UchPlan.find_disc(cursor)
        if discipline is None: return
        cursor.execute('DELETE FROM Uspevaemost WHERE studentID= ? AND discipline= ?', (user[0], discipline[2],))
        connection.commit()
        input(f'Запись об оценке по предмету {discipline[2]} удалёна из базы, нажмите для выхода')
        return

class MainApp():
    def __init__(self):
        self.connection = sqlite3.connect('student_database.db')
        self.cursor = self.connection.cursor()
        self.user = None
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
            id INTEGER PRIMARY KEY,
            full_name TEXT(40) NOT NULL,
            year_of_admission INT NOT NULL CHECK (year_of_admission BETWEEN 2015 AND 2025),
            form_of_education TEXT(10) NOT NULL,
            num_group INTEGER NOT NULL)
            ''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UchPlan (
            courseID INTEGER PRIMARY KEY,
            spec_name TEXT(50) NOT NULL,
            discipline TEXT(25) NOT NULL,
            semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 12),
            time INTEGER NOT NULL CHECK (time BETWEEN 0 AND 200),
            otchet TEXT(10) NOT NULL)
            ''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Uspevaemost (
            uspevID INTEGER PRIMARY KEY,
            semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 12),
            studentID INTEGER NOT NULL,
            discipline TEXT(25) NOT NULL,
            otmetka INTEGER NOT NULL CHECK (otmetka BETWEEN 2 AND 5),
            FOREIGN KEY (studentID) REFERENCES Students (id) ON UPDATE CASCADE,
            FOREIGN KEY (discipline) REFERENCES UchPlan (discipline) ON UPDATE CASCADE ON DELETE CASCADE)
            ''')
        self.application()
        self.connection.commit()
        self.connection.close()
    
    def studentApp(self):
        while True:
            os.system('cls')
            print()
            print('Выберите действие со студентами:')
            print('1) Добавить студента')
            print('2) Изменить данные о студенте')
            print('3) Удалить студента')
            print('4) Посчитать количество студентов по форме обучения')
            print('5) Вернуться в главное меню')
            ch = input('> ')
            ch = int(ch) if ch.isdigit() else 0
            match ch:
                case 1:
                    Student.addNewStudent(self.connection, self.user)
                case 2:
                    Student.updStudent(self.connection, self.user)
                case 3:
                    Student.delStudent(self.connection, self.user)
                case 4:
                    Student.number_studens_form(self.connection)
                case 5:
                    return
    
    def uchPlan(self):
        while True:
            os.system('cls')
            print()
            print('Выберите действие для изменения данных об учебном плане:')
            print('1) Добавить новую специальность')
            print('2) Изменить данные об учебном плане')
            print('3) Удалить специальность')
            print('4) Получить количество часов и форму отчётности дисциплины')
            print('5) Вернуться в главное меню')
            ch = input('> ')
            ch = int(ch) if ch.isdigit() else 0
            match ch:
                case 1:
                    UchPlan.addNewDisc(self.connection, self.user)
                case 2:
                    UchPlan.updDisc(self.connection, self.user)
                case 3:
                    UchPlan.delDisc(self.connection, self.user)
                case 4:
                    UchPlan.form_and_time(self.connection)
                case 5:
                    return
    
    def uspev(self):
        while True:
            os.system('cls')
            print()
            print('Выберите действие для изменения данных об успеваемости:')
            print('1) Добавить оценки')
            print('2) Изменить оценки')
            print('3) Удалить запись об оценке')
            print('4) Вернуться в главное меню')
            ch = input('> ')
            ch = int(ch) if ch.isdigit() else 0
            match ch:
                case 1:
                    Uspev.addNewGrade(self.connection, self.user)
                case 2:
                    Uspev.updGrade(self.connection, self.user)
                case 3:
                    Uspev.delGrade(self.connection, self.user)
                case 4:
                    return
    
    def authorization(self):
        hash_1 = '2c891fd730b1abcaf1a58afd89866d4becdc3e3891d006cffa700f9236cdd85a' # dekanat
        hash_2 = '14bce9479791909b37459677267f2f13894e6d77fc9d8f60a9f04edbe9c8ba8d' # prepodavatel
        os.system('cls')
        print()
        password = input('Введите пароль: ')
        b = hashlib.new('sha256')
        b.update(password.encode())
        ha = b.hexdigest()
        if hash_1 == ha: self.user = ['деканат', 1]
        elif hash_2 == ha: self.user = ['преподаватель', 2]
        else: self.user = None
        return
    
    def application(self):
        while True:
            os.system('cls')
            print()
            print('Вы не авторизованы' if self.user is None else f'Вы авторизованы как {self.user[0]}')
            print()
            print('Выберите действие:')
            print('1) Авторизоваться')
            print('2) Действия со студентами')
            print('3) Учебный план')
            print('4) Журнал успеваемости')
            print('5) Выдать справку об успеваемости студента')
            print('6) Завершить программу')
            ch = input('> ')
            ch = int(ch) if ch.isdigit() else 0
            match ch:
                case 1:
                    self.authorization()
                case 2:
                    self.studentApp()
                case 3:
                    self.uchPlan()
                case 4:
                    self.uspev()
                case 5:
                    Student.spravka(self.connection)
                case 6:
                    break

if __name__ == '__main__':
    MainApp()