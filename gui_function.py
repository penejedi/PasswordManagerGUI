import pyperclip
import random
import string
import sys
import tkinter.messagebox
from hashlib import sha256
import mysql.connector
from cryptography.fernet import Fernet

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password='Hanafi2096!'
)

cursor = db.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS password_manager')
cursor.execute('USE password_manager')
cursor.execute('CREATE TABLE IF NOT EXISTS password_data ('
               '    website VARCHAR(50) NOT NULL,'
               '    username VARCHAR(50) NOT NULL,'
               '    password VARCHAR(100) NOT NULL,'
               'PRIMARY KEY (website, username))')


def master(master_password_input):
    web = 'master'
    name = 'master'
    master_password = master_password_input.get()

    try:
        new_master_password = sha256(master_password.encode('utf-8')).hexdigest()
        cursor.execute('INSERT INTO password_data (website, username, password) VALUES (%s,%s,%s)',
                       (web, name, new_master_password))
        db.commit()
        tkinter.messagebox.showinfo('Welcome', 'Password created, access granted!')
        # print('Master password created!')
    except mysql.connector.errors.IntegrityError:
        hash_input = sha256(master_password.encode('utf-8')).hexdigest()
        cursor.execute('SELECT password FROM password_data WHERE website=(%s) AND username=(%s)',
                       (web, name))
        password = cursor.fetchall()
        if len(password) == 1:
            master_password_hash = password[0][0]
            if hash_input == master_password_hash:
                tkinter.messagebox.showinfo('Welcome', 'Access granted!')
            else:
                tkinter.messagebox.showerror('Access denied', 'Wrong password!')
                sys.exit()


def generate_password(password_input):
    pass_length = random.randint(8,16)
    symbol = '()~!@#$%^&*-_=+[{}]\/?'
    letters = string.ascii_letters + string.digits + symbol
    password = ''.join(random.sample(letters, pass_length - 1))
    password = password + random.choice(symbol)
    password_input.delete(0, tkinter.constants.END)
    password_input.insert(0, str(password))
    pyperclip.copy(password)
    tkinter.messagebox.showinfo('Password created', 'Password copied to clipboard')


def encrypt_password(password):
    try:
        with open('key.key', 'rb') as k:
            key = k.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('key.key', 'wb') as k:
            k.write(key)
    finally:
        fernet = Fernet(key)
        password_enc = fernet.encrypt(bytes(password, 'utf-8'))
        return password_enc


def save(website_input, username_input, password_input):
    try:
        website = website_input.get()
        username = username_input.get()
        password = password_input.get()
        if website and username and password:
            password_enc = encrypt_password(password)
            cursor.execute('INSERT INTO password_data (website, username, password) VALUES (%s,%s,%s)',
                           (website, username, password_enc))
            db.commit()
            tkinter.messagebox.showinfo('Success', 'Password saved!')
            website_input.delete(0, tkinter.constants.END)
            username_input.delete(0, tkinter.constants.END)
            password_input.delete(0, tkinter.constants.END)
        else:
            tkinter.messagebox.showwarning('Error', 'Must fill all fields!')
    except mysql.connector.errors.IntegrityError:
        tkinter.messagebox.showwarning('Duplicate data', 'Password already saved!')


def decrypt_password(password):
    with open('key.key', 'rb') as k:
        key = k.read()
        fernet = Fernet(key)
        dec = fernet.decrypt(bytes(password, 'utf-8')).decode()
        return dec


def retrieve(website_input, username_input):
    website = website_input.get()
    username = username_input.get()
    if website != 'master' and username != 'master':
        cursor.execute('SELECT password FROM password_data WHERE website=(%s) AND username=(%s)',
                       (website, username))
        password = cursor.fetchall()
        if len(password) == 1:
            a = password[0][0]
            b = decrypt_password(a)
            pyperclip.copy(b)
            tkinter.messagebox.showinfo('Password found', f'Your password is {b}')
            website_input.delete(0, tkinter.constants.END)
            username_input.delete(0, tkinter.constants.END)
        else:
            tkinter.messagebox.showwarning('Error', 'No data!')
    else:
        tkinter.messagebox.showwarning('Error', 'No data!')


def exit_programme():
    sys.exit()
