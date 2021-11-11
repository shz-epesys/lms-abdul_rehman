from flask import Flask
from flask_migrate import Migrate

# Routes
from routes.auth_bp import auth_bp
from routes.teacher_bp import teacher_bp
from routes.student_bp import student_bp
from routes.class_bp import class_bp

# Models
from models.models import db

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(teacher_bp, url_prefix='/teachers')
app.register_blueprint(student_bp, url_prefix='/students')
app.register_blueprint(class_bp, url_prefix='/classes')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
