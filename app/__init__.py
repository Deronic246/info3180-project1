from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "wooooow"
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://nbudsinjvocwuf:65352f1613db543f56ff557d4baead3590990b1c99530f22d7d8988191383ce1@ec2-75-101-131-79.compute-1.amazonaws.com:5432/dcnh5o2u3ftoq"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)
UPLOAD_FOLDER = './app/static/uploads'

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
