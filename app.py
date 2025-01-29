from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from utils.db_requests import getSQLFetchone, addSQL, updateSQL
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

import os
from werkzeug.utils import secure_filename

import requests
from datetime import datetime

app = Flask(__name__)  # Здесь исправлено

# Настройки приложения
app.secret_key = "qF9kSzTzcSQn"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def update_user_city(user_id, city):
    """Обновление города пользователя в базе данных"""
    updateSQL("UPDATE users SET city = %s WHERE id = %s", (city, user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not name:
            flash('Name is required!', 'danger')
            return render_template('signup.html')
        if not email:
            flash('Email is required!', 'danger')
            return render_template('signup.html')
        if not password:
            flash('Password is required!', 'danger')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password)
        addSQL("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", params=[name, email, hashed_password])

        user = getSQLFetchone("SELECT id FROM users WHERE email = %s", params=[email])
        if user:
            session['user_id'] = user[0]
            session['user_name'] = name
            session['user_email'] = email  # Сохраняем email в сессии
            flash('Registration successful!', 'success')
            return redirect(url_for('profile'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Авторизация пользователя"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Email and Password are required!', 'danger')
            return redirect(url_for('login'))

        user = getSQLFetchone("SELECT id, name, password FROM users WHERE email = %s", params=[email])

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = email
            flash(f'Welcome back, {user[1]}!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'warning')
        return redirect(url_for('login'))

    user = getSQLFetchone("SELECT name, email, photo FROM users WHERE id = %s", [session['user_id']])

    return render_template(
        'profile.html',
        user_name=user[0],
        user_email=user[1],
        user_photo=user[2],
    )

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    """Загрузка фотографии профиля"""
    if 'user_id' not in session:
        flash('Please log in to upload a photo.', 'warning')
        return redirect(url_for('login'))

    if 'photo' not in request.files:
        flash('No file part.', 'danger')
        return redirect(url_for('profile'))

    file = request.files['photo']

    if file.filename == '':
        flash('No selected file.', 'danger')
        return redirect(url_for('profile'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Обновляем информацию в базе данных
        addSQL("UPDATE users SET photo = %s WHERE id = %s", [filename, session['user_id']])
        flash('Photo uploaded successfully!', 'success')
        return redirect(url_for('profile'))
    else:
        flash('Invalid file format.', 'danger')
        return redirect(url_for('profile'))


@app.route('/logout')
def logout():
    """Выход из учетной записи"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/test')
def test():
    flash('This is a test error message.', 'danger')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
