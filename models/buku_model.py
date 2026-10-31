from config.database import Database
from mysql.connector import Error


class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "books"

    def get_all_buku(self):
        if not self.conn:
            return []

        cursor = None
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            return cursor.fetchall()

        except Error as e:
            print(f"Gagal mengambil data buku: {e}")
            return []

        finally:
            if cursor:
                cursor.close()

    def create_buku(
        self,
        isbn,
        title,
        author,
        category,
        publication_year=None,
        stock=0,
    ):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            query = (
                f"INSERT INTO {self.table_name} "
                "(isbn, title, author, category, publication_year, stock) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(
                query,
                (isbn, title, author, category, publication_year, stock),
            )
            self.conn.commit()
            return True

        except Error as e:
            self.conn.rollback()
            print(f"Gagal menambahkan buku: {e}")
            return False

        finally:
            if cursor:
                cursor.close()

    def update_buku(
        self,
        id_buku,
        isbn,
        title,
        author,
        category,
        publication_year,
        stock,
    ):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            query = (
                f"UPDATE {self.table_name} "
                "SET isbn = %s, title = %s, author = %s, "
                "category = %s, publication_year = %s, stock = %s "
                "WHERE id = %s"
            )
            cursor.execute(
                query,
                (
                    isbn,
                    title,
                    author,
                    category,
                    publication_year,
                    stock,
                    id_buku,
                ),
            )
            self.conn.commit()
            return cursor.rowcount > 0

        except Error as e:
            self.conn.rollback()
            print(f"Gagal mengubah data buku: {e}")
            return False

        finally:
            if cursor:
                cursor.close()

    def delete_buku(self, id_buku):
        if not self.conn:
            return False

        cursor = None
        try:
            cursor = self.conn.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id = %s"
            cursor.execute(query, (id_buku,))
            self.conn.commit()
            return cursor.rowcount > 0

        except Error as e:
            self.conn.rollback()
            print(f"Gagal menghapus data buku: {e}")
            return False

        finally:
            if cursor:
                cursor.close()