from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def main():
    configure()
    register_blueprints()
    app.run(debug=True)


def configure():
    register_blueprints()


def register_blueprints():
    from views import home_views, account_views
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)


if __name__ == '__main__':
    main()
else:
    configure()
