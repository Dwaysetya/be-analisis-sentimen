from database import DatabaseConnectionPool
from flask import make_response, jsonify
import pandas as pd
import json
import datetime

class database_model():
    def __init__(self):
        self.connection_pool = DatabaseConnectionPool.get_instance().connection_pool
    def get_dataset(self):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM dataset ORDER BY created_at DESC")

            dataset = cursor.fetchall()

            dataset_list = []
            for row in dataset:
                dataset_list.append({
                    'id': row[0],
                    'raw_tweet': row[1],
                    'username': row[2],
                    'created_at': row[3],
                })

            return dataset_list
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
        finally:
            cursor.close()
            connection.close()
    def get_dataset_count(self):
        connection = self.connection_pool.get_connection()
        cursor = connection.cursor()

        try:
            query = "SELECT COUNT(*) FROM dataset"
            cursor.execute(query)

            count = cursor.fetchone()[0]

            return {"count": count}
        except Exception as e:
            raise Exception("Failed to get dataset count: " + str(e))
        finally:
            cursor.close()
            connection.close()

    def handle_dataset(self, file):
        try:
            # Read the CSV file using pandas
            df = pd.read_csv(file)

            if df.empty:
                return 'Dataset file is empty'

            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            for _, row in df.iterrows():
                date_str = row['created_at']
                tweet = row['raw_tweet']
                username = row['username']

                # Parse the date string into a datetime object
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S%z")

                cursor.execute(
                    "INSERT INTO dataset (created_at, raw_tweet, username) VALUES (%s, %s, %s)",
                    (date_str, tweet, username)
                )
                connection.commit()

            cursor.close()
            connection.close()

            return 'Dataset file imported successfully'
        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)
    def get_data_labelled(self):
        try:
            # Connect to MySQL database
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()

            # Query to retrieve data from the tables
            query = """
                SELECT dataset.id AS id, dataset.created_at AS created_at, dataset.username AS username, dataset.raw_tweet AS raw_tweet, label.label AS label
                FROM dataset
                JOIN label ON dataset.id = label.id
            """
            cursor.execute(query)
            results = cursor.fetchall()

            # Close the database connection
            cursor.close()
            connection.close()

            # Create the JSON response
            dataset_list = []
            for row in results:
                dataset_list.append({
                    'id': row[0],
                    'created_at': str(row[1]),
                    'username': row[2],
                    'raw_tweet': row[3],
                    'label': row[4]
                })

            return jsonify(dataset_list)

        except Exception as e:
            error_message = {"status": 500, "message": str(e)}
            return make_response(json.dumps(error_message), 500)