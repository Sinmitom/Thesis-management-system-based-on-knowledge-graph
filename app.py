import json

from flask import request, flash, url_for, Flask, render_template, redirect
from handler import ner_handler, search_entity_handler, search_relation_handler, update_entity_handler, \
    update_relation_handler
from forms import NerForm, EntityForm, RelationForm, LoginForm, UpdateForm
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
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
    # 管理员用户类
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


@app.route('/')  # 主页
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
def search_entity():  # 实体查询功能
    entity_form = EntityForm()
    print('测试实体查询')
    # print(entity_form.select.choices)
    select = entity_form.select.choices[entity_form.select.data - 1][1]
    # print(select)
    res = {'ctx': 'padding', 'entityRelation': ''}
    if entity_form.validate_on_submit():
        res = search_entity_handler.search_entity(entity_form.entity.data, select)  # 传入输入框信息和下拉框信息
        print(res)
    return render_template('entity.html', form=entity_form, ctx=res['ctx'], entityRelation=res['entityRelation'],
                           select=select)


@app.route('/search_relation', methods=['GET', 'POST'])
def search_relation():
    # 基于关系查询
    message = ""
    mode = 1  # mode为1为关系查询
    flag = 0  # 类别标志0为论文，1为作者
    relation_form = RelationForm()
    relation = relation_form.relation.choices[relation_form.relation.data - 1][1]  # 相应的查找关系
    print('关系查询测试')
    res = {'ctx': '', 'searchResult': ''}
    if relation_form.validate_on_submit():
        if len(relation_form.entity1.data) != 0 and len(relation_form.entity2.data) != 0 and relation == "无限制":
            mode = 2  # mode为2为路径查询
        if len(relation_form.entity1.data) == 0 and len(relation_form.entity2.data) == 0:
            message = "这怎么查询(╯▔皿▔)╯！请输入信息！"
        res, flag = search_relation_handler.search_relation(relation_form.entity1.data, relation,
                                                            relation_form.entity2.data)
    print('*' * 50)
    print(res)
    return render_template('relation.html', form=relation_form, ctx=res['ctx'], searchResult=res['searchResult'],
                           mode=mode, f=flag, message=message)


@app.route('/ner-post', methods=['POST'])
def ner_post():
    ner_form = NerForm()
    ctx = {'rlt': '', 'seg_word': ''}
    if ner_form.validate_on_submit():
        ctx = ner_handler.ner_post(ner_form.ner_text.data)
    return render_template("index.html", form=ner_form, rlt=ctx['rlt'], seg_word=ctx['seg_word'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 测试登录功能
    login_form = LoginForm()
    username = login_form.username.data
    password = login_form.password.data
    user = User.query.first()
    message = ""
    if login_form.is_submitted():
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            print('登录成功！')
            return redirect(url_for('search_entity'))  # 重定向到主页
        elif username != user.username:
            message = "无此账户名信息！"
            print(message)
        elif not user.validate_password(password):
            message = "密码输入错误！"
            print(message)
    print('测试登录功能', user.username == username, password)
    # print(user.validate_password(password), login_form.password.errors)
    return render_template('login.html', form=login_form, message=message)


@app.route('/logout')
@login_required  # 用于视图保护
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('search_entity'))  # 重定向回首页


@app.route('/update', methods=['GET', 'POST'])
@login_required  # 用于视图保护
def update():  # 更新图谱
    update_form = UpdateForm()
    res = {'ctx': 'padding', 'entityRelation': ''}
    message = ""
    if update_form.is_submitted():
        selectFunction = update_form.selectFunction.data  # 选择相应功能
        if selectFunction == 1:  # 选择添加实体功能
            select = update_form.selectBox.data  # 传入select 表单选择的内容
            print("添加实体测试", type(select))
            if select == 1:
                # 验证数据
                paperId = update_form.paperId.data
                paperTitle = update_form.paperTitle.data
                paperYear = update_form.paperYear.data
                if len(paperId) == 0 or len(paperTitle) == 0 or len(paperYear) != 4 or len(paperTitle) < 2:
                    if len(paperId) == 0 or len(paperTitle) == 0:
                        message += "Id号和标题不能为空！"
                    elif len(paperYear) != 4 or int(paperYear) > 2022:
                        message += "年份输入格式有误！"
                    elif len(paperTitle) < 2:
                        message += "标题输入过短！"
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.add_entity(paperId, paperTitle, select, paperYear)  # 传入输入框信息和下拉框信息
                print(res)

            elif select == 2:
                # 验证数据
                authorId = update_form.authorId.data
                authorName = update_form.authorName.data
                print(authorName)
                if not authorId or not authorName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.add_entity(authorId, authorName, select)  # 传入输入框信息和下拉框信息

            elif select == 3:  # 添加机构信息
                # 验证数据
                affiliationId = update_form.affiliationId.data
                affiliationName = update_form.affiliationName.data
                print(affiliationName)
                if not affiliationId or not affiliationName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.add_entity(affiliationId, affiliationName, select)  # 传入输入框信息和下拉框信息

            elif select == 4:  # 添加Venue信息
                # 验证数据
                venueId = update_form.venueId.data
                venueName = update_form.venueName.data
                print(venueName)
                if not venueId or not venueName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.add_entity(venueId, venueName, select)  # 传入输入框信息和下拉框信息

            elif select == 5:  # 添加Concept信息
                # 验证数据
                conceptId = update_form.conceptId.data
                conceptName = update_form.conceptName.data
                print(conceptName)
                if not conceptId or not conceptName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)

                res = update_entity_handler.add_entity(conceptId, conceptName, select)  # 传入输入框信息和下拉框信息

        elif selectFunction == 2:
            # 选择删除实体功能
            select = update_form.selectBox.data  # 传入select 表单选择的内容
            print("删除实体测试", type(select))
            if select == 1:
                # 验证数据
                paperId = update_form.paperId.data
                paperTitle = update_form.paperTitle.data
                paperYear = update_form.paperYear.data
                if len(paperTitle) == 0:
                    flash('非法输入！')  # 显示错误
                    if len(paperTitle) == 0:
                        message += "论文标题不能为空！"
                    elif len(paperTitle) < 2:
                        message += "标题输入过短！"
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.delete_entity(paperId, paperTitle, select, paperYear)  # 传入输入框信息和下拉框信息
                print(res)
            elif select == 2:
                # 验证数据
                authorId = update_form.authorId.data
                authorName = update_form.authorName.data
                print(authorName)
                if not authorName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.delete_entity(authorId, authorName, select)  # 传入输入框信息和下拉框信息

            elif select == 3:  # 删除机构信息
                # 验证数据
                affiliationId = update_form.affiliationId.data
                affiliationName = update_form.affiliationName.data
                print(affiliationName)
                if not affiliationName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.delete_entity(affiliationId, affiliationName, select)  # 传入输入框信息和下拉框信息

            elif select == 4:  # 删除Venue信息
                # 验证数据
                venueId = update_form.venueId.data
                venueName = update_form.venueName.data
                print(venueName)
                if not venueName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)

                res = update_entity_handler.delete_entity(venueId, venueName, select)  # 传入输入框信息和下拉框信息

            elif select == 5:  # 删除Concept信息
                # 验证数据
                conceptId = update_form.conceptId.data
                conceptName = update_form.conceptName.data
                print(conceptName)
                if not conceptName:
                    message = '输入信息格式有误！'
                    flash('非法输入！')  # 显示错误
                    return render_template('update.html', form=update_form, message=message)
                res = update_entity_handler.delete_entity(conceptId, conceptName, select)  # 传入输入框信息和下拉框信息

    return render_template('update.html', form=update_form, ctx=res['ctx'], entityRelation=res['entityRelation'])


@app.route('/update_relation', methods=['GET', 'POST'])
@login_required  # 用于视图保护
def update_relation():  # 更新图谱关系
    res = {'ctx': '', 'searchResult': ''}
    selectFunction = -1
    relation_form = RelationForm()
    relation = relation_form.relation.choices[relation_form.relation.data - 1][1]  # 相应的关系
    print('更新关系测试1', relation_form.entity1.data, relation, relation_form.entity2.data)
    if relation_form.validate_on_submit():
        selectFunction = relation_form.selectFunction.data
        if selectFunction == 1:  # 添加关系
            res = update_relation_handler.update_relation(relation_form.entity1.data, relation,
                                                          relation_form.entity2.data)
            print('更新关系测试2', res)

        else:   # 删除关系
            res = update_relation_handler.delete_relation(relation_form.entity1.data, relation,
                                                          relation_form.entity2.data)
            print(res)
            #print('更新关系测试2', res['ctx'], res['searchResult'])
    return render_template('update_relation.html', form=relation_form, ctx=res['ctx'], searchResult=res['searchResult'],
                           selectFunction=selectFunction)