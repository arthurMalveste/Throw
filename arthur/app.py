from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Usar o caminho absoluto, mas fora da pasta instance para teste
db_path = os.path.join(os.path.dirname(__file__), 'throw_game.db')

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita o tracking de modificações

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Modelo de dados
class BugReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_report = db.Column(db.Date, nullable=False, default=db.func.current_date())

    def __repr__(self):
        return f'<BugReport {self.id}>'

# Rotas
@app.route('/relatorio')
def relatorio():
    bugs = BugReport.query.all()
    return render_template('relatorio.html', bugs=bugs)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']

        print(f"Recebido: Nome={nome}, Email={email}, Mensagem={mensagem}")  # Debug

        try:
            novo_bug = BugReport(nome=nome, email=email, mensagem=mensagem)
            db.session.add(novo_bug)
            db.session.commit()
            print("Bug salvo com sucesso")
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            db.session.rollback()

    return render_template('index.html')

@app.route('/personagens')
def personagens():
    return render_template('personagens.html')


if __name__ == '__main__':
    with app.app_context():
        print(f"Criando banco de dados em: {db_path}")
        db.create_all()  # Cria as tabelas
    app.run(debug=True)
