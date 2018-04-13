from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from app.routes.scan import scan_app


def create_app():

    # Instantiate Flask
    app_main = Flask(__name__)

    app_main.config['DEBUG'] = True

    # import settings
    app_main.config.from_object('app.config')

    # install SQLAlchemy
    # db.init_app(app_main)

    # import all blueprint
    app_main.register_blueprint(scan_app)

    return app_main


app = create_app()

from app.template_filter.ValueStatus import value_status_file

db = SQLAlchemy(app)

from app.models import DataBase

# print("Drop tables")
# db.drop_all()
# print("Create tables")
# db.create_all()

@app.route('/')
def index():
    return redirect(url_for('scan_app.files'))

app.run()

	