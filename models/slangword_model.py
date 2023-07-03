from database import DatabaseConnectionPool
from flask import make_response, json, jsonify
import pandas as pd
import datetime

class slangword_model():
    def __init__(self):
        self.connection_pool = DatabaseConnectionPool.get_instance().connection_pool
    def getall_slangword(self):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT id, kata_baku, kata_slang FROM slangwords")
            slangwords = cursor.fetchall()

            slangword_list = []
            for row in slangwords:
                slangword_list.append({
                    'id': row[0],
                    'kata_baku': row[1],
                    'kata_slang': row[2],
                })

            return slangword_list
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
    def import_slangwords(self, file):
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file, sep=';')

            if df.empty:
                return 'Dataset file is empty'

            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            for _, row in df.iterrows():
                kata_baku = row['kata_baku']
                kata_slang = row['kata_slang']

                cursor.execute(
                    "INSERT INTO slangwords (kata_baku, kata_slang) VALUES (%s, %s)",
                    (kata_baku, kata_slang, )
                )
                connection.commit()

            cursor.close()
            connection.close()

            return 'Slangwords file imported successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(jsonify(error_message), 500)
    def add_slangword(self, data):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            # Insert the slangword into the table
            query = "INSERT INTO slangwords (kata_baku, kata_slang) VALUES (%s, %s)"
            cursor.execute(query, (data['kata_baku'], data['kata_slang']))
            connection.commit()
            return 'Slangword added successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
    def update_slangword(self, id, data):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            # Update the slangword in the table
            query = "UPDATE slangwords SET kata_baku = %s, kata_slang = %s WHERE id = %s"
            cursor.execute(query, (data['kata_baku'], data['kata_slang'], id))
            connection.commit()
            return f'Slangword with ID {id} updated successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
    def delete_slangword(self, id):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()
        try:
            # Delete the slangword from the table
            query = "DELETE FROM slangwords WHERE id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            return f'Slangword with ID {id} deleted successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
