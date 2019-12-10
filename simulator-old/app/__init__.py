from flask import Flask
import os


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # register blueprints for health
    from project.api.ping import ping_blueprint
    app.register_blueprint(ping_blueprint)

    from project.api.users.views import users_blueprint

    app.register_blueprint(users_blueprint)

    # shell context to register the app to the flask shell
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
