import sqlite3


class DbContext:
    def __init__(self, conn_string):
        self.conn = sqlite3.connect(conn_string)

    def create_database(self):
        cursor = self.conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Questions (
                            question_id INTEGER PRIMARY KEY,
                            question_text TEXT
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Responses (
                            response_id INTEGER PRIMARY KEY,
                            question_id INTEGER,
                            response_text TEXT,
                            score INTEGER,
                            FOREIGN KEY(question_id) REFERENCES Questions(question_id)
                        )''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def get_question_by_name(self, text):
        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM Questions WHERE question_text = ?', (text,))
        question = cursor.fetchone()

        return question

    def get_response_by_question_id_and_text(self, question_id, response_text):
        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM Responses WHERE question_id = ? AND response_text = ?',
                       (question_id, response_text))
        response = cursor.fetchone()

        return response

    def get_responses_by_question_id(self, question_id):
        cursor = self.conn.cursor()

        cursor.execute('SELECT * FROM Responses WHERE question_id = ?', (question_id,))
        responses = cursor.fetchall()

        return responses

    def add_question(self, question_text):
        cursor = self.conn.cursor()

        cursor.execute('INSERT INTO Questions (question_text) VALUES (?)', (question_text,))
        question_id = cursor.lastrowid

        self.conn.commit()

        return question_id

    def add_response(self, question_id, response_text, score):
        cursor = self.conn.cursor()

        cursor.execute('INSERT INTO Responses (question_id, response_text, score) VALUES (?, ?, ?)',
                       (question_id, response_text, score))
        response_id = cursor.lastrowid

        self.conn.commit()
        return response_id

    def update_response_score(self, response_id, new_score):
        cursor = self.conn.cursor()

        cursor.execute('UPDATE Responses SET score = ? WHERE response_id = ?', (new_score, response_id))
        self.conn.commit()


## creat si testat db ul aici !!

# db = DbContext("ResponseScoresDb.sqlite")
# # db.create_database()
# # question_id = db.add_question("Ce mai faci?")
# response_id = db.add_response(2, "Rau", -1)
# response_id = db.add_response(2, "Bine", -1)
# db.close_connection()
