import hashlib

from config.database import Database
from mysql.connector import Error


class UserModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def autentikasi(self, username, password):
        if not self.conn:
            return None

        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)
            query = (
                f"SELECT id_user, username, role FROM {self.table_name} "
                "WHERE username = %s AND password = %s"
            )
            cursor.execute(query, (username, password_hash))
            return cursor.fetchone()

        except Error as e:
            print(f"Gagal memverifikasi pengguna: {e}")
            return None

        finally:
            if cursor:
                cursor.close()

    def register_user(self, username, password, role):
        if not self.conn:
            return False

        username = username.strip()
        role = role.strip().lower()

        if not username or not password or role not in ("admin", "anggota"):
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            query = (
                f"INSERT INTO {self.table_name} (username, password, role) "
                "VALUES (%s, %s, %s)"
            )
            cursor.execute(query, (username, password_hash, role))
            self.conn.commit()
            return True

        except Error as e:
            self.conn.rollback()
            print(f"Gagal mendaftarkan pengguna: {e}")
            return False

        finally:
            if cursor:
                cursor.close()