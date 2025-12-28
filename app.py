from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import KategoriFilm, Film, Watchlist, User
from werkzeug.utils import secure_filename
from pymysql import IntegrityError
from werkzeug.security import generate_password_hash
import os

# APP CONFIG
app = Flask(__name__)
app.secret_key = "movie-secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'posters')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def is_login():
    return 'user_id' in session

def is_admin():
    return session.get('role') == 'admin'

# AUTH & HOME
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_login():
        return redirect(url_for('home'))

    if request.method == 'POST':
        user = User.login(request.form['username'], request.form['password'])
        if user:
            session.update({'user_id': user['id_user'], 'username': user['username'], 'role': user['role']})
            flash("Login berhasil!", "success")
            return redirect(url_for('home'))
        flash("Username atau password salah", "danger")

    return render_template('login.html', show_menu=False)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def home():
    if not is_login():
        return redirect(url_for('login'))
    return redirect(url_for('admin_dashboard' if is_admin() else 'user_index'))

# USER ROUTES
@app.route('/user')
def user_index():
    if not is_login(): return redirect(url_for('login'))
    page = int(request.args.get('page', 1))
    limit = 12
    films = Film.get_paginated(limit, (page - 1) * limit)
    total_pages = (Film.count_all() + limit - 1) // limit
    return render_template('index.html', films=films, page=page, total_pages=total_pages, show_menu=True)

@app.route('/film/<int:id>')
def film_detail(id):
    if not is_login(): return redirect(url_for('login'))
    film = Film.get_by_id(id) 

    if film:
        return render_template('detail_film.html', film=film, show_menu=True)
    else:
        flash("Film tidak ditemukan!", "danger")
        return redirect(url_for('user_index'))
    
@app.route('/watchlist')
def watchlist():
    if not is_login(): 
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    data = Watchlist.get_user(user_id)

    total = len(data)
    watched = len([w for w in data if w['status'] == 'Sudah Ditonton'])
    
    percent = (watched / total * 100) if total > 0 else 0
    
    return render_template('watchlist.html', 
                           watchlist=data, 
                           stats={'total': total, 'watched': watched, 'percent': int(percent)},
                           show_menu=True)

@app.route('/watchlist/add/<int:id_film>')
def add_watchlist(id_film):
    if not is_login(): return redirect(url_for('login'))
    Watchlist.add(session['user_id'], id_film)
    flash("Ditambahkan ke watchlist", "success")
    return redirect(url_for('watchlist'))

@app.route('/watchlist/delete/<int:id>')
def delete_watchlist(id):
    if not is_login(): return redirect(url_for('login'))
    Watchlist.delete(id)
    return redirect(url_for('watchlist'))

@app.route('/watchlist/done/<int:id>')
def watched_watchlist(id):
    if not is_login(): 
        return redirect(url_for('login'))
    
    Watchlist.mark_as_watched(id)
    flash("Selamat! Satu film lagi selesai ditonton.", "success")
    return redirect(url_for('watchlist'))

# ADMIN ROUTES
@app.route('/admin')
def admin_dashboard():
    if not is_admin(): return "Akses ditolak", 403
    return render_template('admin/dashboard.html', show_menu=True)

@app.route('/admin/film')
def admin_film():
    if not is_admin(): return "Akses ditolak", 403
    films = Film.get_paginated(100, 0)
    return render_template('admin/film.html', films=films, show_menu=True)

@app.route('/admin/film/add', methods=['GET', 'POST'])
def admin_film_add():
    if not is_admin(): return "Akses ditolak", 403
    
    if request.method == 'POST':
        judul_film = request.form.get('judul')
        
        file = request.files.get('poster')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'default.jpg'

        try:
            Film.create(
                judul_film, 
                request.form['id_kategori'], 
                request.form['sinopsis'], 
                request.form['tahun'], 
                filename
            )
            flash(f"Film '{judul_film}' berhasil ditambahkan ke katalog!", "success")
            return redirect(url_for('admin_film'))
            
        except Exception as e:
            flash(f"Gagal menambahkan film: {str(e)}", "danger")
            return redirect(url_for('admin_film'))

    kategori = KategoriFilm.get_all()
    return render_template('admin/film_form.html', kategori=kategori, show_menu=True)

@app.route('/admin/film/edit/<int:id>', methods=['GET', 'POST'])
def admin_film_edit(id):
    if not is_admin(): return "Akses ditolak", 403
    
    film = Film.get_by_id(id)
    if request.method == 'POST':
        judul_baru = request.form.get('judul')
        file = request.files.get('poster')
        
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = film['poster'] 

        Film.update(id, judul_baru, request.form['id_kategori'], 
                    request.form['sinopsis'], request.form['tahun'], filename)
        
        flash(f"Film '{judul_baru}' berhasil diperbarui!", "success")
        return redirect(url_for('admin_film'))

    kategori = KategoriFilm.get_all()
    return render_template('admin/film_edit.html', film=film, kategori=kategori, show_menu=True)

@app.route('/admin/film/delete/<int:id>')
def admin_film_delete(id):
    if not is_admin(): return "Akses ditolak", 403
    film = Film.get_by_id(id)
    judul_film = film['judul'] if film else "Film"
    Film.delete(id)
    flash(f"Film '{judul_film}' telah dihapus dari katalog.", "success")
    return redirect(url_for('admin_film'))

@app.route('/admin/kategori')
def admin_kategori():
    if not is_admin(): return "Akses ditolak", 403
    kategori_list = KategoriFilm.get_all()
    return render_template('admin/kategori.html', kategori=kategori_list, show_menu=True)

@app.route('/admin/kategori/add', methods=['POST'])
def admin_kategori_add():
    nama = request.form['nama_kategori']
    deskripsi = request.form.get('deskripsi', '')
    
    try:
        KategoriFilm.create(nama, deskripsi)
        flash(f"Kategori '{nama}' berhasil ditambahkan!", "success")
    except Exception as e:
        flash(f"Gagal menambahkan kategori: {str(e)}", "danger")
        
    return redirect(url_for('admin_kategori'))

@app.route('/admin/kategori/delete/<int:id>')
def admin_kategori_delete(id):
    kategori = KategoriFilm.get_by_id(id)
    nama_kategori = kategori['nama_kategori'] if kategori else "Kategori"

    try:
        KategoriFilm.delete(id)
        flash(f"Kategori '{nama_kategori}' berhasil dihapus!", "success")
    except IntegrityError:
        flash(f"Gagal menghapus! Kategori '{nama_kategori}' masih digunakan oleh beberapa film.", "danger")
    except Exception as e:
        flash(f"Terjadi kesalahan: {str(e)}", "danger")
        
    return redirect(url_for('admin_kategori'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_login():
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Konfirmasi password tidak cocok!", "danger")
            return render_template('register.html', show_menu=False)

        hashed_pw = generate_password_hash(password)

        try:
            User.create(username, hashed_pw, role='user')
            flash(f"Akun '{username}' berhasil didaftarkan! Silakan login.", "success")
            return redirect(url_for('login'))
        except IntegrityError:
            flash("Username sudah digunakan, cari nama lain.", "danger")
        except Exception as e:
            flash(f"Terjadi kesalahan: {str(e)}", "danger")

    return render_template('register.html', show_menu=False)

if __name__ == '__main__':
    app.run