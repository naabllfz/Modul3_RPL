from config.database import Database
from mysql.connector import Error


class AnggotaModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "anggota"

    def get_all_anggota(self):
        if not self.conn:
            return []

        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            return cursor.fetchall()

        except Error as e:
            print(f"Gagal mengambil data anggota: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

    def create_anggota(self, nama, alamat):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            query = (
                f"INSERT INTO {self.table_name} (nama, alamat) "
                "VALUES (%s, %s)"
            )
            cursor.execute(query, (nama, alamat))
            self.conn.commit()
            return True

        except Error as e:
            self.conn.rollback()
            print(f"Gagal menambahkan anggota: {e}")
            return False

        finally:
            if cursor:
                cursor.close()