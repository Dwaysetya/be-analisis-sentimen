from database import DatabaseConnectionPool
from flask import make_response

class user_model():
    def __init__(self):
        self.connection_pool = DatabaseConnectionPool.get_instance().connection_pool

    def user_get_all(self):
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users')
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            if len(result) > 0:
                return make_response({"data": result, "message": "Here is your list of users"}, 200)
            else:
                return make_response({"message": "No Data Found"}, 404)
        except Exception as e:
            print("Error retrieving user data:", str(e))
            return make_response({"message": "An error occurred while retrieving user data"}, 500)
    def user_sign_up(self, data):
        if not data:
            return make_response({"message": "Invalid request"}, 500)

        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            values = (data['username'], data['password'])
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            return make_response({"message": "User registered successfully", "status": True}, 201)
        except Exception as e:
            print("Error registering user:", str(e))
            return make_response({"message": "An error occurred while registering the user", "status": False}, 500)
    def user_sign_in(self, data):
        if not data:
            return make_response({"message": "Invalid request"}, 500)

        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (data['username'], data['password'])
            cursor.execute(query, values)
            result = cursor.fetchone()
            cursor.close()
            connection.close()

            if result:
                return make_response({"message": "User authenticated successfully", "data": result, "status": True})
            else:
                return make_response({"message": "Invalid credentials", "status": False}, 401)
        except Exception as e:
            print("Error authenticating user:", str(e))
            return make_response({"message": "An error occurred while authenticating the user"}, 500)
    def user_update(self, user_id, data):
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "UPDATE users SET username = %s, password = %s WHERE id = %s"
            values = (data['username'], data['password'], user_id)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            return make_response({"message": "User updated successfully"})
        except Exception as e:
            print("Error updating user:", str(e))
            return make_response({"message": "An error occurred while updating the user"}, 500)
    def user_delete(self, user_id):
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = "DELETE FROM users WHERE id = %s"
            values = (user_id,)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()

            return make_response({"message": "User deleted successfully"})
        except Exception as e:
            print("Error deleting user:", str(e))
            return make_response({"message": "An error occurred while deleting the user"}, 500)
    def user_pagination(self, limit, page):
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor(dictionary=True)
            limit = int(limit)
            page = int(page)
            offset = (page - 1) * limit
            query = f"SELECT * FROM users LIMIT {limit} OFFSET {offset}"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

            if len(results) > 0:
                return make_response({"message": "Here is a list", "data": results}, 200)
            else:
                return make_response({"message": "Data not found"}, 404)
        except Exception as e:
            print("Error retrieving paginated user data:", str(e))
            return make_response({"message": "An error occurred while retrieving paginated user data"}, 500)
