from flask import Flask, request, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)

db_endpoint = open('/home/ec2-user/dbserver.endpoint', 'r', encoding='UTF-8')

# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] = db_endpoint.readline().strip()
# app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_URL_2')
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'henry_1'
app.config['MYSQL_DATABASE_DB'] = 'phonebook'
app.config['MYSQL_DATABASE_PORT'] = 3306

db_endpoint.close()

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()


def init_phonebook_db():
    drop_table = 'DROP TABLE IF EXISTS phonebook.phonebook;'
    phonebook_table = """
    CREATE TABLE phonebook(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    number VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """

    data = """
    INSERT INTO phonebook.phonebook (name, number)
    VALUES
        ('Henry, "1234567890"),
        ("Sergio Taco", "67854"),
        ("Vincenzo Altobelli", "876543554");
    """

    cursor.execute(drop_table)
    cursor.execute(phonebook_table)
    cursor.execute(data)


def find_persons(keyword):
    query = f"""
    SELECT * FROM phonebook WHERE name like '%{keyword.strip().lower()}%';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    persons = [{'id': row[0], 'name':row[1].strip().title(), 'number':row[2]}
               for row in result]
    return persons


def insert_person(name, number):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """
    cursor.execute(query)
    row = cursor.fetchone()

    if row is not None:
        return f'Person with name {row[1].title()} already exits.'

    insert = f"""
    INSERT INTO phonebook (name, number)
    VALUES ('{name.strip().lower()}', '{number}');
    """

    cursor.execute(insert)
    result = cursor.fetchall()

    return f'Person {name.strip().title()} added to Phonebook successfully'


def update_person(name, number):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """

    cursor.execute(query)
    row = cursor.fetchone()

    if row is None:
        return f'Person with name {name.strip().title()} does not exits.'

    update = f"""
    UPDATE phonebook
    SET name='{row[1]}', number = '{number}'
    WHERE id= {row[0]};
    """

    cursor.execute(update)

    return f'Phone record of {name.strip().title()} is updated successfully '


def delete_person(name):
    query = f"""
    SELECT * FROM phonebook WHERE name like '{name.strip().lower()}';
    """

    cursor.execute(query)
    row = cursor.fetchone()

    if row is None:
        return f'Person with name {name.strip().title()} does not exist, no need to delete.'

    delete = f"""
    DELETE FROM phonebook
    WHERE id= {row[0]};
    """

    cursor.execute(delete)
    return f'Phone record of {name.strip().title()} is deleted from the phonebook successfully.'


@app.route('/', methods=['GET', 'POST'])
def find_records():
    if request.method == 'POST':
        keyword = request.form['username']
        persons = find_persons(keyword)
        return render_template('index.html', persons=persons, keyword=keyword, show_result=True, developer_name='Henry)
    else:
        return render_template('index.html', show_result=False, developer_name='Henry)


@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == '':
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name can not be empty.', show_result=False, action_name='save', developer_name='Henry)
        elif name.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name can not be number.', show_result=False, action_name='save', developer_name='Henry)

        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip() == '':
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number can not be empty.', show_result=False, action_name='save', developer_name='Henry)
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format.', show_result=False, action_name='save', developer_name='Henry)

        result = insert_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='save', developer_name='Henry)
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='save', developer_name='Henry)


@app.route('/update', methods=['GET', 'POST'])
def update_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, action_name='update', developer_name='Henry)
        phone_number = request.form['phonenumber']
        if phone_number is None or phone_number.strip() == "":
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number can not be empty', show_result=False, action_name='update', developer_name='Henry)
        elif not phone_number.isdecimal():
            return render_template('add-update.html', not_valid=True, message='Invalid input: Phone number should be in numeric format', show_result=False, action_name='update', developer_name='Henry)

        result = update_person(name, phone_number)
        return render_template('add-update.html', show_result=True, result=result, not_valid=False, action_name='update', developer_name='Henry)
    else:
        return render_template('add-update.html', show_result=False, not_valid=False, action_name='update', developer_name='Henry)


@app.route('/delete', methods=['GET', 'POST'])
def delete_record():
    if request.method == 'POST':
        name = request.form['username']
        if name is None or name.strip() == "":
            return render_template('delete.html', not_valid=True, message='Invalid input: Name can not be empty', show_result=False, developer_name='Henry)
        result = delete_person(name)
        return render_template('delete.html', show_result=True, result=result, not_valid=False, developer_name='Henry)
    else:
        return render_template('delete.html', show_result=False, not_valid=False, developer_name='Henry)


if __name__ == '__main__':
    init_phonebook_db()
    app.run(host='0.0.0.0', port=80)
