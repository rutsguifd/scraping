from json import dump
from requests import get
from bs4 import BeautifulSoup
from sqlite3 import connect

connection = connect("C:/Users/VIKTOR/Desktop/bd.db")
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS faculty (id int , name TEXT,url TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS departments (id int, name TEXT,url TEXT , faculty_id int)")
cursor.execute("CREATE TABLE IF NOT EXISTS staff (id int , name TEXT)")
connection.commit()

BASE_URL = 'https://lnam.edu.ua/'
URL = f"{BASE_URL}uk/faculty.html"
result = get(URL)
university = BeautifulSoup(result.content, "html.parser")
faculties = []
fac_list = university.find(class_='mod_article')

for facult in fac_list.find_all(class_='faculty'):
    facult_name = facult.figure.a['original-title']
    facult_url = facult.figure.a['href']
    faculty = {
        "name": facult_name,
        "url": facult_url,
        "departments": []
    }
    for f in cursor.execute(
        "SELECT id FROM faculty WHERE name=? AND url=?",
        [faculty["name"], faculty["url"]]
    ):
        faculty["id"] = f[0]

    if not faculty.get("id"):
        cursor.execute(
            "INSERT INTO faculty (name, url) VALUES (?,?)",
            [faculty["name"], faculty["url"]]
        )
        connection.commit()
        for f in cursor.execute(
            "SELECT id FROM faculty WHERE name=? AND url=?",
            [faculty["name"], faculty["url"]]
        ):
            faculty["id"] = f[0]

    for depart in facult.find_all('li'):
        depart_url = BASE_URL + depart.a['href']
        depart_name = depart.a.getText()
        depart_res = get(depart_url)
        department_page = BeautifulSoup(depart_res.content, "html.parser")
        staff_link = BASE_URL + \
            department_page.find('a', title="Колектив кафедри")['href']
        staff_res = get(staff_link)
        staff_page = BeautifulSoup(staff_res.content, "html.parser")
        department = {
            "name": depart_name,
            "url": depart_url,
            "staff": []
        }
        for d in cursor.execute(
            "SELECT id FROM departments WHERE name=? AND url=?",
            [department["name"], department["url"]]
        ):
            department["id"] = d[0]

        if not department.get("id"):
            cursor.execute(
                "INSERT INTO departments (name, url, faculty_id) VALUES (?,?,?)",
                [department["name"], department["url"], faculty["id"]]
            )
            connection.commit()
            for d in cursor.execute(
                "SELECT id FROM departments WHERE name=? AND url=?",
                [department["name"], department["url"]]
            ):
                department["id"] = d[0]

        for teacher in staff_page.find_all('h4'):
            department["staff"].append(teacher.a.getText())
            cursor.execute(
                "INSERT INTO staff (name) VALUES (?)",
                [teacher.a.getText()]
            )
            connection.commit()
        faculty["departments"].append(department)
    faculties.append(faculty)

with open("lnam.json", "w", encoding="utf-8") as json_file:
    dump(faculties, json_file, ensure_ascii=False, indent=4)