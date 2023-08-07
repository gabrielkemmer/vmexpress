from flask import Flask, render_template, request, redirect, flash, session, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from api_ssw import *


def creat_app(host='146.190.165.62', port=5000):
    app = Flask(__name__)
    app.secret_key = 'Fn741953.741953'
    
    # MongoDB configuration
    client = MongoClient('mongodb+srv://gabrielkemmer:Fn741953.741953@microblog.ojr4lzw.mongodb.net/?retryWrites=true&w=majority')
    db = client['guilherme']
    users_collection = db['users']
    consults_collection = db['consultas']
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if 'username' in session:
            if request.method == 'POST':
                cnpj = request.form['cnpj']
    
            return render_template('home.html')  # Pass the cnpj variable to the template
    
        return redirect('/login')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            cnpj = request.form['cnpj']
    
            user = users_collection.find_one({'username': username})
    
            if user and cnpj and check_password_hash(user['password'], password):
                session['username'] = username
                session['cnpj'] = cnpj
                return redirect('/')
            else:
                return 'Invalid username or password'
    
        return render_template('login.html')
    
    @app.route('/rastreamento_logado')
    def rastreamento_logado():
        cnpj = session.get('cnpj')  # Retrieve the cnpj from the query parameter
        if not cnpj:
            return redirect ('/login')
        query_result = consults_collection.find({'CNPJ': cnpj})
        data_list = list(query_result)
        return render_template('rastreamento_logado.html', data_list=data_list, cnpj=cnpj)
    
    @app.route('/login_admin', methods=['GET', 'POST'])
    def login_admin():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
    
            user = users_collection.find_one({'username': username})
    
            if user and check_password_hash(user['password'], password):
                session['username'] = username
                return render_template('admin.html')
            else:
                return 'Invalid username or password'
    
        return render_template('login_admin.html')
    
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        if request.method == 'POST':
            path = os.getcwd()
            UPLOAD_FOLDER = os.path.join(path, 'cnpjs')
    
            if not os.path.isdir(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
    
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
            # Check if the 'file' key exists in the request.files dictionary
            if 'file' not in request.files:
                flash('No file part')
                return redirect('/admin')
    
            file = request.files['file']
    
            # If the user does not select a file, the browser submits an empty part
            if file.filename == '':
                flash('No selected file')
                return redirect('/admin')
    
            # Save the file with its original name using the secure_filename function
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
    
            return redirect('/admin')
    
        return render_template('admin.html')
    
    @app.route('/home_rastreamento', methods=['GET', 'POST'])
    def home_rastreamento():
        if request.method == 'POST':
            cnpj = request.form['cnpj']
            nota_fiscal = request.form['nota_fiscal']
            return redirect('/rastreamento?cnpj=' + cnpj + '&nota_fiscal=' + nota_fiscal)
            
        return render_template('home_rastreamento.html')
    
    @app.route('/rastreamento')
    def rastreamento():
        cnpj = request.args.get('cnpj')
        nota_fiscal = request.args.get('nota_fiscal')
        result = api_ssw(cnpj, nota_fiscal)
    
        if result:
            remetente, destinatario, data_hora, cidade, ocorrencia, descricao, tipo, data_hora_efetiva, nome_recebedor = result
            return render_template('rastreamento.html', remetente=remetente, destinatario=destinatario, data_hora=data_hora, cidade=cidade, ocorrencia=ocorrencia, descricao=descricao, tipo=tipo, data_hora_efetiva=data_hora_efetiva, nome_recebedor=nome_recebedor)
        
        if request.method == ["POST"]:
            cnpj = request.form['cnpj']
            nota_fiscal = request.form['nota_fiscal']
            return redirect(url_for('rastreamento_completo', cnpj=cnpj, nota_fiscal=nota_fiscal))
    
        return render_template('rastreamento.html')
    
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            cnpj = request.form["cnpj"]
    
            existing_user = users_collection.find_one({'username': username})
    
            if existing_user:
                return 'Este usuário já existe, escolha um novo nome de usuário'
    
            hashed_password = generate_password_hash(password)
    
            new_user = {'username': username, 'password': hashed_password, 'cnpj': cnpj}
            users_collection.insert_one(new_user)
    
            session['username'] = username
            return redirect('/')
    
        return render_template('signup.html')
    
    @app.route('/logout')
    def logout():
        session.pop('username', None)
        return redirect('/')
        
app = create_app()

