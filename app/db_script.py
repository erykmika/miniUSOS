import psycopg2
from datetime import datetime
import json

def connect():
    # Wczytanie danych dostepowych do bazy danych
    login_data = None
    with open("database_creds.json", "r") as creds:
        login_data = json.loads(creds.read())
    # Polaczenie z baza danych PostgreSQL
    con = psycopg2.connect(
        database=login_data["database"],
        user=login_data["user"],
        password=login_data["password"],
        host=login_data["host"],
        port=login_data["port"]
    )
    print("Pomyslnie polaczono z baza danych PostgreSQL")
    return con


def build(con):
    # Cursor
    cur = con.cursor()
    # 1 Tabela kierunki
    cur.execute("""CREATE TABLE IF NOT EXISTS Kierunki_studiow
                (id SERIAL PRIMARY KEY,
                nazwa VARCHAR(50),
                stopien INTEGER);
                """)
    # 2 Tabela prowadzacy
    cur.execute("""CREATE TABLE IF NOT EXISTS Prowadzacy
                (id SERIAL PRIMARY KEY,
                imie VARCHAR(30),
                nazwisko VARCHAR(30),
                haslo VARCHAR(30),
                email VARCHAR(30) UNIQUE);
                """)
    # 3 Tabela komunikaty
    cur.execute("""CREATE TABLE IF NOT EXISTS Komunikaty
                (id SERIAL PRIMARY KEY,
                tytul VARCHAR(255),
                data timestamp,
                tresc VARCHAR(1500));
                """)
    # 4 Tabela studenci
    cur.execute("""CREATE TABLE IF NOT EXISTS Studenci
                (nr_albumu INTEGER PRIMARY KEY,
                imie VARCHAR(30),
                nazwisko VARCHAR(30),
                semestr INTEGER,
                adres VARCHAR(50),
                haslo VARCHAR(30),
                email VARCHAR(30) UNIQUE,
                id_kierunku INTEGER,
                FOREIGN KEY(id_kierunku) REFERENCES Kierunki_studiow(id));
                """)
    # 5 Tabela kursy
    cur.execute("""CREATE TABLE IF NOT EXISTS Kursy
                (id VARCHAR(10) PRIMARY KEY,
                nazwa VARCHAR(50),
                budynek_sala VARCHAR(30),
                termin TEXT,
                id_prowadzacego INTEGER,
                id_kierunku INTEGER,
                FOREIGN KEY(id_kierunku) REFERENCES Kierunki_studiow(id),
                FOREIGN KEY(id_prowadzacego) REFERENCES Prowadzacy(id));
                """)
    # 6 Tabela oceny
    cur.execute("""CREATE TABLE IF NOT EXISTS Oceny
                (id SERIAL PRIMARY KEY,
                ocena VARCHAR(3),
                data_wpisania timestamp,
                nr_albumu INTEGER,
                id_kursu VARCHAR(10),
                FOREIGN KEY(nr_albumu) REFERENCES Studenci(nr_albumu),
                FOREIGN KEY(id_kursu) REFERENCES Kursy(id));
                """)
    # 7 Tabela studenci-kursy
    cur.execute("""CREATE TABLE IF NOT EXISTS Studenci_Kursy
                (nr_albumu INTEGER,
                id_kursu VARCHAR(10),
                PRIMARY KEY(nr_albumu, id_kursu),
                FOREIGN KEY(nr_albumu) REFERENCES Studenci(nr_albumu),
                FOREIGN KEY (id_kursu) REFERENCES Kursy(id));
                """)
    # 8 Tabela komunikaty-kierunki
    cur.execute("""CREATE TABLE IF NOT EXISTS Komunikaty_kierunki_studiow
                (id_kierunku INTEGER,
                id_komunikatu INTEGER,
                PRIMARY KEY(id_kierunku, id_komunikatu),
                FOREIGN KEY(id_kierunku) REFERENCES Kierunki_studiow(id),
                FOREIGN KEY (id_komunikatu) REFERENCES Komunikaty(id));
                """)


def addMajor(conn, name, level):
    cursor = conn.cursor()
    level = 1 if level == 1 else 2
    cursor.execute(f"""INSERT INTO Kierunki_studiow (nazwa, stopien) VALUES ('{name}', {level});""")


def addLecturer(conn, name, secName, pswd, email):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Prowadzacy (imie, nazwisko, haslo, email)
                       VALUES ('{name}', '{secName}', '{pswd}', '{email}');""")


def addStudent(conn, number, name, secName, semester, address, majorId, pswd, email):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Studenci (nr_albumu, imie, nazwisko, semestr, adres, id_kierunku, haslo, email)
                       VALUES ({number}, '{name}', '{secName}', {semester}, '{address}', {majorId}, '{pswd}', '{email}');""")


def addMessage(conn, title, content):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Komunikaty (tytul, data, tresc)
                       VALUES ('{title}', '{datetime.now()}', '{content}');""")


def addCourse(conn, courseId, name, location, date, majorId, lecturerId):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Kursy (id, nazwa, budynek_sala, termin, id_kierunku, id_prowadzacego)
                       VALUES ('{courseId}', '{name}', '{location}', '{date}', {majorId}, {lecturerId});""")


def addGrade(conn, grade, studentNum, courseId):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Oceny (ocena, data_wpisania, nr_albumu, id_kursu)
                       VALUES ('{grade}', '{datetime.now()}', {studentNum}, '{courseId}');""")
    

def addStudentCourse(conn, studentNum, courseId):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Studenci_Kursy (nr_albumu, id_kursu)
                       VALUES ({studentNum}, '{courseId}');""")


def addMajorMessage(conn, majorId, messageId):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Komunikaty_kierunki_studiow (id_kierunku, id_komunikatu)
                       VALUES ({majorId}, {messageId});""")


def addMajors(conn, num):
    for i in range(num):
        name = input("Nazwa kierunku: ")
        level = int(input("Stopien (1/2): "))
        addMajor(conn, name, level)


def addLecturers(conn, num):
    for i in range(num):
        name = input("Imie: ")
        secName = input("Nazwisko: ")
        pswd = input("Haslo: ")
        email = input("Email: ")
        addLecturer(conn, name, secName, pswd, email)


def addMessages(conn, num):
    for i in range(num):
        title = input("Tytul: ")
        content = input("Tresc: ")
        addMessage(conn, title, content)


def addStudents(conn, num):
    for i in range(num):
        num = int(input("Nr albumu: "))
        name = input("Imie: ")
        secName = input("Nazwisko: ")
        pswd = input("Haslo: ")
        email = input("Email: ")
        semester = int(input("Semestr: "))
        addr = input("Adres: ")
        majorId = input("Kierunek studiow id: ")
        addStudent(conn, num, name, secName, semester, addr, majorId, pswd, email)


def addCourses(conn, num):
    for i in range(num):
        code = input("Kod kursu: ")
        name = input("Nazwa: ")
        location = input("Budynek/sala: ")
        date = input("Termin: ")
        majorId = input("ID kierunku: ")
        lecId = int(input("ID Prowadzacego: "))
        addCourse(conn, code, name, location, date, majorId, lecId)


def addGrades(conn, num):
    for i in range(num):
        grade = input("Ocena: ")
        studNum = int(input("Nr albumu: "))
        courseId = input("ID kursu: ")
        addGrade(conn, grade, studNum, courseId)


def addStudentCourses(conn, num):
    for i in range(num):
        studentNum = int(input("Nr albumu: "))
        courseId = input("ID kursu: ")
        addStudentCourse(conn, studentNum, courseId)


def addMajorMessages(conn, num):
    for i in range(num):
        majorId = int(input("ID kierunku: "))
        messageId = int(input("ID komunikatu: "))
        addMajorMessage(conn, majorId, messageId)


# wyswietlanie rekordow
def printAllRecords(conn, table):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    columns = [description[0] for description in cursor.description]
    
    for columnName in columns:
        print("{:<15}".format(columnName), end=" ")
    print()
    print("-" * 120)    
    for row in cursor.fetchall():
        for col in row:
            stripped = str(col).strip()
            print("{:<15}".format(stripped), end= " ")
        print()


# Operacje update/delete
def updateMajor(conn, majorId, newName, newLevel):
    cursor = conn.cursor()
    newLevel = 1 if newLevel == 1 else 2
    cursor.execute(f"""UPDATE Kierunki_studiow SET nazwa = '{newName}', stopien = {newLevel} WHERE id = {majorId};""")


def deleteMajor(conn, majorId):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Kierunki_studiow WHERE id = {majorId};""")


def updateLecturer(conn, lecturerId, newName, newSecName, newPswd, newEmail):
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE Prowadzacy SET imie = '{newName}', nazwisko = '{newSecName}', haslo = '{newPswd}', email = '{newEmail}' WHERE id = {lecturerId};""")


def deleteLecturer(conn, lecturerId):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Prowadzacy WHERE id = {lecturerId};""")


def updateStudent(conn, studentNum, newName, newSecName, newSemester, newAddress, newMajorId, newPswd, newEmail):
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE Studenci SET imie = '{newName}', nazwisko = '{newSecName}', semestr = {newSemester},
                       adres = '{newAddress}', id_kierunku = {newMajorId}, haslo = '{newPswd}', email = '{newEmail}'
                       WHERE nr_albumu = {studentNum};""")


def deleteStudent(conn, studentNum):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Studenci WHERE nr_albumu = {studentNum};""")


def updateMessage(conn, msgId, title, date, content):
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE Komunikaty SET tytul = '{title}', data = '{date}', tresc = '{content}'
                       WHERE id = {msgId};""")


def deleteMessage(conn, msgId):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Komunikaty WHERE id = {msgId};""")


def updateCourse(conn, courseId, newName, newLocation, newDate, newMajorId, newLecturerId):
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE Kursy SET nazwa = '{newName}', budynek_sala = '{newLocation}', termin = '{newDate}',
                       id_kierunku = {newMajorId}, id_prowadzacego = {newLecturerId} WHERE id = '{courseId}';""")

def deleteCourse(conn, courseId):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Kursy WHERE id = '{courseId}';""")


def updateGrade(conn, gradeId, newGrade, newDate, newStudentNum, newCourseId):
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE Oceny SET ocena = '{newGrade}', data_wpisania = '{newDate}',
                       nr_albumu = {newStudentNum}, id_kursu = '{newCourseId}' WHERE id = {gradeId};""")


def deleteGrade(conn, gradeId):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Oceny WHERE id = {gradeId};""")


def deleteStudentCourse(conn, studentNum, courseId):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Studenci_Kursy WHERE nr_albumu = {studentNum} AND id_kursu = '{courseId}';""")


def deleteMajorMessage(conn, majorId, messageId):
    cursor = conn.cursor()
    cursor.execute(f"""DELETE FROM Komunikaty_kierunki_studiow WHERE id_kierunku = {majorId} AND id_komunikatu = {messageId};""")


def main():
    conn = connect()
    while True:
        print("Wybierz opcje: ")
        print("0. Zakoncz")
        print("1. Buduj baze danych")
        print("2. Wyswietl rekordy")
        print("3. Dodaj rekordy")
        print("4. Usun rekordy")
        print("5. Aktualizuj rekordy")
        choice = int(input("Wybor > "))
        if choice == 0:
            break
        elif choice == 1:
            build(conn)
        elif choice == 2:
            print("1. Kierunki")
            print("2. Prowadzacy")
            print("3. Komunikaty")
            print("4. Studenci")
            print("5. Kursy")
            print("6. Oceny")
            print("7. Kursy-studenci")
            print("8. Komunikaty-kierunki")
            choice = int(input("Wybor > "))
            if choice == 1:
                printAllRecords(conn, 'Kierunki_studiow')
            elif choice == 2:
                printAllRecords(conn, 'Prowadzacy')
            elif choice == 3:
                printAllRecords(conn, 'Komunikaty')
            elif choice == 4:
                printAllRecords(conn, 'Studenci')
            elif choice == 5:
                printAllRecords(conn, 'Kursy')
            elif choice == 6:
                printAllRecords(conn, 'Oceny')
            elif choice == 7:
                printAllRecords(conn, 'Studenci_Kursy')
            elif choice == 8:
                printAllRecords(conn, 'Komunikaty_kierunki_studiow')
        elif choice == 3:
            print("1. Dodaj kierunki")
            print("2. Dodaj prowadzacych")
            print("3. Dodaj komunikaty")
            print("4. Dodaj studentow")
            print("5. Dodaj kursy")
            print("6. Dodaj oceny")
            print("7. Dodaj kursy do studentow")
            print("8. Dodaj komunikaty do kierunkow")
            choice = int(input("Wybor > "))
            num = int(input("Ile dodac? "))
            if choice == 1:
                addMajors(conn, num)
            elif choice == 2:
                addLecturers(conn, num)
            elif choice == 3:
                addMessages(conn, num)
            elif choice == 4:
                addStudents(conn, num)
            elif choice == 5:
                addCourses(conn, num)
            elif choice == 6:
                addGrades(conn, num)
            elif choice == 7:
                addStudentCourses(conn, num)
            elif choice == 8:
                addMajorMessages(conn, num)
        elif choice == 4:
            print("1. Usun kierunek")
            print("2. Usun prowadzacego")
            print("3. Usun komunikat")
            print("4. Usun studenta")
            print("5. Usun kurs")
            print("6. Usun ocene")
            print("7. Usun kurs-student")
            print("8. Usun komunikat-kierunek")
            choice = int(input("Wybor > "))
            if choice <= 6:
                id = input("ID do usuniecia: ")
                if choice == 1:
                    deleteMajor(conn, int(id))
                elif choice == 2:
                    deleteLecturer(conn, int(id))
                elif choice == 3:
                    deleteMessage(conn, int(id))
                elif choice == 4:
                    deleteStudent(conn, int(id))
                elif choice == 5:
                    deleteCourse(conn, id)
                elif choice == 6:
                    deleteGrade(conn, int(id))
            elif choice == 7:
                studNum = int(input("Nr albumu: "))
                courseId = input("Kod kursu: ")
                deleteStudentCourse(conn, studNum, courseId)
            elif choice == 8:
                msgId = int(input("ID komunikatu: "))
                majorId = int(input("ID kierunku: "))
                deleteMajorMessage(conn, majorId, msgId)
        elif choice == 5:
            print("1. Aktualizuj dane kierunku")
            print("2. Aktualizuj dane prowadzacego")
            print("3. Aktualizuj dane komunikatu")
            print("4. Aktualizuj dane studenta")
            print("5. Aktualizuj dane kursu")
            print("6. Aktualizuj dane oceny")
            choice = int(input("Wybor > "))
            if choice == 1:
                id = int(input("ID kierunku: "))
                name = input("Nazwa: ")
                level = int(input("Stopien: "))
                updateMajor(conn, id, name, level)
            elif choice == 2:
                id = int(input("ID kierunku: "))
                name = input("Imie: ")
                secName = input("Nazwisko: ")
                pswd = input("Haslo: ")
                email = input("E-mail: ")
                updateLecturer(conn, id, name, secName, pswd, email)
            elif choice == 3:
                id = int(input("ID komunikatu: "))
                title = input("Tytul: ")
                date = input("Data: ")
                content = input("Tresc: ")
                updateMessage(conn, id, title, date, content)
            elif choice == 4:
                num = int(input("Nr albumu: "))
                name = input("Imie: ")
                secName = input("Nazwisko: ")
                semester = int(input("Semestr: "))
                addr = input("Adres: ")
                majorId = int(input("ID kierunku: "))
                pswd = input("Haslo: ")
                email = input("E-mail: ")
                updateStudent(conn, num, name, secName, semester, addr, majorId, pswd, email)
            elif choice == 5:
                courseId = input("Kod kursu: ")
                name = input("Nazwa: ")
                location = input("Budynek/sala: ")
                date = input("Termin: ")
                majorId = int(input("ID kierunku: "))
                lecturerId = int(input("ID prowadzacego: "))
                updateCourse(conn, courseId, name, location, date, majorId, lecturerId)
            elif choice == 6:
                id = int(input("ID oceny: "))
                grade = input("Ocena: ")
                date = input("Data: ")
                studNum = int(input("Nr albumu: "))
                courseId = input("Kod kursu: ")
                updateGrade(conn, id, grade, date, studNum, courseId)
        else:
            print("Niezaimplementowane!")
        conn.commit()


if __name__ == '__main__':
    main()
