from database import DatabaseConnectionPool
from flask import make_response, json
import pandas as pd

class stopword_model():
    def __init__(self):
        self.connection_pool = DatabaseConnectionPool.get_instance().connection_pool
    def getall_stopword(self):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM stopwords")

            stopword = cursor.fetchall()

            stopword_list = []
            for row in stopword:
                stopword_list.append({
                    'id': row[0],
                    'kata_stop': row[1],
                })

            return stopword_list
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
    def import_stopwords(self, file):
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file)

            if df.empty:
                return 'Dataset file is empty'

            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            for _, row in df.iterrows():
                kata_stop = row['kata_stop']

                cursor.execute(
                    "INSERT INTO stopwords (kata_stop) VALUES (%s)",
                    (kata_stop,)
                )
                connection.commit()

            cursor.close()
            connection.close()

            return 'Stopwords file imported successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
    def add_stopword(self, data):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            # Insert the stopword into the table
            query = "INSERT INTO stopwords (kata_stop) VALUES (%s)"
            cursor.execute(query, (data['kata_stop'],))
            connection.commit()
            return 'Stopword added successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response({ "message": error_message }, 500)
        finally:
            cursor.close()
            connection.close()
    def update_stopword(self, id, data):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            # Update the stopword in the table
            query = "UPDATE stopwords SET kata_stop = %s WHERE id = %s"
            cursor.execute(query, (data['kata_stop'], id))
            connection.commit()
            return f'Stopword with ID {id} updated successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
    def delete_stopword(self, id):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            # Delete the stopword from the table
            query = "DELETE FROM stopwords WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            return f'Stopword with ID {id} deleted successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()

