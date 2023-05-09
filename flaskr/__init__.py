import os
from flask import Flask


# 1 The Application Factory¶ - create_app()
def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, Flask!'

    # //--\\ (1.0) - Application Setup¶
    # \\--// (2.4) - Define and Access the Database¶ -> Initialize the Database File¶

    from . import db
    db.init_app(app)

    # //--\\ (2.4) - Define and Access the Database¶ -> Initialize the Database File¶
    # \\--// (3.2) - Blueprints and Views¶ -> Import and register the blueprint from[,,,]

    from . import auth
    app.register_blueprint(auth.bp)

    # //--\\ Blueprints and Views¶ -> Import and register the blueprint from[,,,]
    # \\--// Blog Blueprint¶

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
