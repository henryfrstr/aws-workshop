from flask import Flask, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
from configDB import ConfigDB
config = ConfigDB()
app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = "db_endpoint"
app.config['MYSQL_DATABASE_USER'] = "admin"
app.config['MYSQL_DATABASE_PASSWORD'] = "henry_1"
app.config['MYSQL_DATABASE_DB'] = "phonebook"
app.config['MYSQL_DATABASE_PORT'] = 3306

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()


def init_phonebook_db():

    drop_table = 'DROP TABLE IF EXISTS persons;'
    phone_table = """
    CREATE TABLE phonebook(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        number VARCHAR(100) NOT NULL )
    ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """
    data = """
    INSERTT INTO phonebook.phonebook(name,number) 
    VALUES("Henry", 505050050),("Bruce",0090505343434)
    """


cursor.execute(drop_table)
cursor.execute(phone_table)
cursor.execute(data)


def find_person(keyword):
    query = f"SELECT * FROM phonebook WHERE name like '%{keyword.strip().lower()}%';"
    cursor.execute(query)
    result = cursor.fetchall()
    person = [("id":row[0], "name":row[1].strip().title(), "number":row[2]) for row in result]
    if not any(person):
        person = [('Not found.', 'Not Found.')]
    return person


def insert_person(name, num):
    query = f"SELECT * FROM phonebook WHERE name like '{word.strip().lower()}';"
    cursor.execute(query)
    row = cursor.fetchone()

    if row is not None:
        return f"Person with name {row[1].strip().title()} already exists."

    insert = f"""
    INSERT INT phonebook (name, number)
    VALUES('{name.strip().lower()}', '{num}');
    """

    cursor.execute(insert)
    result = cursor.fetchall()

    return f'Person {name.strip().title()} added to Phonebook successfully'


def update_person(name, num):
    query = f"SELECT * FROM phonebook WHERE name like '{word.strip().lower()}';"
    cursor.execute(query)
    row = cursor.fetchone()

    if row is None:
        return f"Person with name {row[1].strip().title()} does not exists."
    update = f"""
    UPDATE phonebook
    SET name='{row[1]}', number = '{num}'
    WHERE id='{row[0]}';
    """
    cursor.execute(update)

    return f'Phone record of {name.strip().title()} is updated successfully'


def delete_person(name):
    query = f"SELECT * FROM phonebook WHERE name like '{word.strip().lower()}';"

    cursor.execute(query)
    row = cursor.fetchone()
    if row is None:
        return f"Person with name {row[1].strip().title()} does not exists, nı need to delete"

    delete = f"""
    DELETE FROM phonebook
    WHERE id='{row[0]}';
    """

    cursor.execute(delete)
    return f'Phone record of {name.strip().title()} is deleted successfully'


@app.route("/", methods=['GET', 'POST'])
def find_records():
    if request.method == 'POST':
        keyword = request.form['username']
        persons = find_person(keyword)
        return render_template('index.html', person=person, keyword=keyword, show_result=True, developer_name='Henry')
    else:
        return render_template('index.html', show_result=False, developer_name='Henry')


@app.route("/add", methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message="Invalid Input: Name can not be empty.", show_result=False, action_name="Save", developer_name="Henry")
        elif name.isdecimal():
            return render_template('add-update.html', not_valid=True, message="Invalid Input: Name can not be number.", show_result=False, action_name="Save", developer_name="Henry")

        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message="Invalid Input: Phone number can not be empty.", show_result=False, action_name="Save", developer_name="Henry")

        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message="Invalid Input: Phone number should be in numeric format.", show_result=False, action_name="Save", developer_name="Henry")

        result = insert_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name="Save", developer_name="Henry")
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name="Save", developer_name="Henry")


@app.route('/update', methods=['GET', 'POST'])
def update_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message="Invalid Input: Name can not be empty.", show_result=False, action_name="Update", developer_name="Henry")
        # elif name.isdecimal():
        #     return render_template('add-update.html', not_valid=True, message="Invalid Input: Name can not be number.", show_result=False, action_name="Update", developer_name="Henry")
        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message="Invalid Input: Phone number can not be empty.", show_result=False, action_name="Update", developer_name="Henry")

        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message="Invalid Input: Phone number should be in numeric format.", show_result=False, action_name="Update", developer_name="Henry")

        result = update_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name="Save", developer_name="Henry")
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name="Update", developer_name="Henry")

    @app.route('/delete', methods=['GET', 'POST'])
    def delete_record():
        if request.method == 'POST':
            name = request.form['username']
            if name is None or name.strip() == "":
                return render_template('delete.html', not_valid=True, message="Invalid Input: Name can not be empty.", show_result=False, action_name="Update", developer_name="Henry")
            result = delete_person(name)
            return render_template('delete.html', show_result=True, result=result, not_valid=False, developer_name="Henry")
        else:
            return render_template('delete.html', show_result=False, not_valid=False, developer_name="Henry")


if __name__ == "__main__":
    init_phonebook_db()
    app.run(host='0.0.0.0', port=80)
