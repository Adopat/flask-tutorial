# 包含应用工厂
# Python flaskr 应该作为一个包
import os
from flask import Flask
# create_app 是一个应用工厂函数
def create_app(test_config=None):
    # 创建Flask 实例
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping() 设置一个应用的缺省配置
    app.config.from_mapping(
        SECRET_KEY='dev',
        #数据库文件存放路径
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
        return 'Hello, World!'
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app


