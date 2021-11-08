from flask import Flask
from flask_migrate import Migrate
from routes.auth_bp import auth_bp
from routes.teacher_bp import teacher_bp
from models.models import db

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(teacher_bp, url_prefix='/teachers/<teacher_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
