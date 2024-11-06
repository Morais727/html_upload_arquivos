from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Pasta onde os arquivos serão salvos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uploads.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Para flash messages

db = SQLAlchemy(app)

# Modelo para armazenar dados do arquivo no banco de dados
class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    filepath = db.Column(db.String(120), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)

# Rota para a página de upload
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Rota para receber e salvar o arquivo
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('upload_form'))

    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('upload_form'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Salva informações do arquivo no banco de dados
        uploaded_file = UploadedFile(filename=filename, filepath=filepath, mimetype=file.mimetype)
        db.session.add(uploaded_file)
        db.session.commit()

        flash('Upload feito com sucesso')
        return redirect(url_for('upload_form'))

# Inicializa o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Cria a pasta de uploads, caso não exista
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)


# http://127.0.0.1:5000