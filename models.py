import pymysql, os
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def connect(self):
        return pymysql.connect(
            host='dsyafdha.mysql.pythonanywhere-services.com',
            user='dsyafdha',
            password='MySQLPass',
            database='dsyafdha$mocatalog',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query(self, sql, params=None):
        conn = self.connect()
        cur = conn_attach = conn.cursor()
        cur.execute(sql, params)
        cur.close()
        conn.close()


    def fetchall(self, sql, params=None):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result


    def fetchone(self, sql, params=None):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result

    def execute(self, sql, params=None):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, params)
        cur.close()
        conn.close()


db = Database()

# KATEGORI FILM
# =====================================================
class KategoriFilm:
    @staticmethod
    def get_all():
        return db.fetchall("SELECT * FROM kategori_film ORDER BY nama_kategori")

    @staticmethod
    def create(nama, deskripsi):
        db.query(
            "INSERT INTO kategori_film (nama_kategori, deskripsi) VALUES (%s,%s)",
            (nama, deskripsi)
        )

    @staticmethod
    def get_by_id(id):
        return db.fetchone(
            "SELECT * FROM kategori_film WHERE id_kategori=%s",
            (id,)
        )

    @staticmethod
    def update(id, nama, deskripsi):
        db.query("""
            UPDATE kategori_film
            SET nama_kategori=%s, deskripsi=%s
            WHERE id_kategori=%s
        """, (nama, deskripsi, id))

    @staticmethod
    def delete(id):
        db.query(
            "DELETE FROM kategori_film WHERE id_kategori=%s",
            (id,)
        )

# FILM
# =====================================================
class Film:
    @staticmethod
    def count_all():
        return db.fetchone(
            "SELECT COUNT(*) AS total FROM film"
        )['total']

    @staticmethod
    def get_paginated(limit, offset):
        return db.fetchall("""
            SELECT f.*, k.nama_kategori
            FROM film f
            JOIN kategori_film k ON f.id_kategori = k.id_kategori
            ORDER BY f.id_film DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))

    @staticmethod
    def get_all():
        return db.fetchall("""
            SELECT f.*, k.nama_kategori
            FROM film f
            JOIN kategori_film k ON f.id_kategori = k.id_kategori
            ORDER BY f.id_film DESC
        """)

    @staticmethod
    def get_by_id(id):
        return db.fetchone("""
            SELECT f.*, k.nama_kategori
            FROM film f
            JOIN kategori_film k ON f.id_kategori = k.id_kategori
            WHERE f.id_film = %s
        """, (id,))

    @staticmethod
    def create(judul, id_kategori, sinopsis, tahun, poster):
        db.query("""
            INSERT INTO film (judul, id_kategori, sinopsis, tahun, poster)
            VALUES (%s,%s,%s,%s,%s)
        """, (judul, int(id_kategori), sinopsis, tahun, poster)) # Konversi ke int

    @staticmethod
    def update(id, judul, id_kategori, sinopsis, tahun, poster):
        db.query("""
            UPDATE film SET
                judul=%s,
                id_kategori=%s,
                sinopsis=%s,
                tahun=%s,
                poster=%s
            WHERE id_film=%s
        """, (judul, int(id_kategori), sinopsis, tahun, poster, id))

    @staticmethod
    def delete(id):
        db.query("DELETE FROM film WHERE id_film=%s", (id,))

# USER
# =====================================================
class User:
    @staticmethod
    def create(username, password, role):
        db.query("""
            INSERT INTO users (username, password, role)
            VALUES (%s,%s,%s)
        """, (
            username,
            password,
            role
        ))

    @staticmethod
    def login(username, password):
        user = db.fetchone(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        if user and check_password_hash(user['password'], password):
            return user
        return None

# WATCHLIST
# =====================================================
class Watchlist:
    @staticmethod
    def get_user(id_user):
        return db.fetchall("""
            SELECT
                w.id_watchlist,
                w.status,
                f.id_film,
                f.judul,
                f.poster,
                f.tahun,
                k.nama_kategori
            FROM watchlist w
            JOIN film f ON w.id_film = f.id_film
            JOIN kategori_film k ON f.id_kategori = k.id_kategori
            WHERE w.id_user = %s
            ORDER BY
                CASE WHEN w.status = 'Belum Ditonton' THEN 0 ELSE 1 END,
                w.id_watchlist DESC
        """, (id_user,))

    @staticmethod
    def add(id_user, id_film):
        existing = db.fetchone("SELECT id_watchlist FROM watchlist WHERE id_user=%s AND id_film=%s", (id_user, id_film))
        if not existing:
            db.query("INSERT INTO watchlist (id_user, id_film) VALUES (%s,%s)", (id_user, id_film))

    @staticmethod
    def delete(id_watchlist):
        db.query("DELETE FROM watchlist WHERE id_watchlist=%s", (id_watchlist,))

    @staticmethod
    def update_rating(id_watchlist, rating):
        db.query("UPDATE watchlist SET rating=%s WHERE id_watchlist=%s", (rating, id_watchlist))

    @staticmethod
    def mark_as_watched(id_watchlist):
        db.query("""
            UPDATE watchlist
            SET status = 'Sudah Ditonton'
            WHERE id_watchlist = %s
        """, (id_watchlist,))
