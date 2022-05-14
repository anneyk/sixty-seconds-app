
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail






app = Flask(__name__)
app.config['SECRET_KEY'] = '564648sjdhbfl654684adfa'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ihxlugvhbwpazq:b22f33bb92783a54f46d24f58b8d29554dcab17780799902a3d1e497fa582e5b@ec2-54-165-184-219.compute-1.amazonaws.com:5432/dcq9vagtjfhq2c'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sixtysecondspitch'
app.config['MAIL_PASSWORD'] = '42625435'
mail = Mail(app)

from pitch import routes