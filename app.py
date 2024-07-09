# run.py
from app import create_app
from config import Config
from app.database.db import db
from flask_migrate import Migrate

app = create_app()
app.config.from_object(Config)
migrate = Migrate(app, db)
db.init_app(app)


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 90)
