from flask import Flask, render_template, request, flash, url_for
from handler import ner_handler, search_entity_handler, search_relation_handler
from forms import NerForm, EntityForm, RelationForm
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask import Flask, render_template, redirect
import click

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['WTF_I18N_ENABLED'] = False  # 让Flask-WTF使用WTForms内置的错误消息翻译
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.debug = True

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
login_manager = LoginManager(app)  # 实例化扩展类
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


# 生成管理员账户
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)  # 设置密码
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done.')


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


@app.route('/')
def index():
    entity_form = EntityForm()
    # print('测试1')
    # print(type(entity_form.select.choices))
    select = entity_form.select.choices[entity_form.select.data - 1][1]
    # print(select)
    res = {'ctx': 'padding', 'entityRelation': ''}
    if entity_form.validate_on_submit():
        res = search_entity_handler.search_entity(entity_form.entity.data, select)  # 传入输入框信息和下拉框信息
    return render_template('entity.html', form=entity_form, ctx=res['ctx'], entityRelation=res['entityRelation'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/search_entity', methods=['GET', 'POST'])
def search_entity():
    entity_form = EntityForm()
    print('测试1')
    # print(type(entity_form.select.choices))
    select = entity_form.select.choices[entity_form.select.data - 1][1]
    # print(select)
    res = {'ctx': 'padding', 'entityRelation': ''}
    if entity_form.validate_on_submit():
        res = search_entity_handler.search_entity(entity_form.entity.data, select)  # 传入输入框信息和下拉框信息
    return render_template('entity.html', form=entity_form, ctx=res['ctx'], entityRelation=res['entityRelation'])


@app.route('/search_relation', methods=['GET', 'POST'])
def search_relation():
    # 基于关系查询
    relation_form = RelationForm()
    relation = relation_form.relation.choices[relation_form.relation.data - 1][1]  # 相应的查找关系
    print('关系查询测试')
    res = {'ctx': '', 'searchResult': ''}
    if relation_form.validate_on_submit():
        res = search_relation_handler.search_relation(relation_form.entity1.data, relation,
                                                      relation_form.entity2.data)

    # print('*'*50)
    # print('*'*50)
    # print(res['searchResult'])
    return render_template('relation.html', form=relation_form, ctx=res['ctx'], searchResult=res['searchResult'])


@app.route('/ner-post', methods=['POST'])
def ner_post():
    ner_form = NerForm()
    ctx = {'rlt': '', 'seg_word': ''}
    if ner_form.validate_on_submit():
        ctx = ner_handler.ner_post(ner_form.ner_text.data)
    return render_template("index.html", form=ner_form, rlt=ctx['rlt'], seg_word=ctx['seg_word'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        print(user)
        print(user.validate_password(password))
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('search_entity'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')


@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('search_entity'))  # 重定向回首页
