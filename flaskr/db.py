# 定义和操作数据库
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# 创建新的连接，g是一个特殊的对象，用来保存连接信息
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            # current_app 是另一个特殊对象，该对象指向处理请求的Flask 应用
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
# 初始化数据库
def init_db():
    # 获取数据库连接
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        # 执行SQL 命令
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)