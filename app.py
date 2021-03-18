#!/usr/local/bin/python3
import os, sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask
import db, auth, blog, admin, contact

sentry_sdk.init(
    dsn="https://3312a0c0adb3482c85dc3e330a36dfca@o543738.ingest.sentry.io/5682771",
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "cl0e7me4em150ghg1eat"
UPLOAD_FOLDER='./static/uploads'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

app.register_blueprint(contact.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(admin.bp)

app.add_url_rule("/", endpoint="index")

if __name__ == "__main__":
    app.run()