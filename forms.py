from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField, \
    PasswordField  # StringField对应HTML中type="text"的<input>元素，SubmitField对应type='submit'的<input>元素
from wtforms.validators import DataRequired, Length


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class LoginForm(MyBaseForm):
    # 登录模块布局
    username = StringField('username', validators=[DataRequired(message="用户名不能为空哦")])
    password = PasswordField('password', validators=[DataRequired(message="密码不能为空哦"),
                                                     Length(3, message='密码不能小于3位数，请重新输入！')])
    # username = StringField('username')
    # password = PasswordField('password')
    submit = SubmitField('登录')


class NerForm(MyBaseForm):
    ner_text = TextAreaField('ner_text', validators=[DataRequired(), Length(0, 300)])  # 表单做数据验证
    submit = SubmitField('确认')


class EntityForm(MyBaseForm):
    # 输入框前加入候选框
    select = SelectField('relation', choices=[(1, 'paperName'), (2, 'authorName')], default=1, coerce=int)
    entity = StringField('entity', validators=[DataRequired()])
    submit = SubmitField('查询')


class RelationForm(MyBaseForm):
    selectFunction = SelectField('selectFunction', choices=[(1, '添加关系'), (2, '删除关系')],
                                 default=1, coerce=int)
    entity1 = StringField('entity1')
    relation = SelectField('relation', choices=[(1, '无限制'), (2, 'refer'), (3, 'own'), (4, 'belong'), (5, 'interest')],
                           default=1, coerce=int)
    entity2 = StringField('entity2')
    submit = SubmitField('查询')
    submit1 = SubmitField('确认')

class UpdateForm(MyBaseForm):
    selectFunction = SelectField('selectFunction', choices=[(1, '添加实体'), (2, '删除实体')],
                                 default=1, coerce=int)
    selectBox = SelectField('selectBox', choices=[(0, '空'),(1, '论文'), (2, '作者'), (3, '机构'), (4, '期刊'), (5, '研究领域')],
                            default=0, coerce=int)
    paperId = StringField('paperId')
    paperTitle = StringField('paperTitle')
    paperYear = StringField('paperYear')

    authorId = StringField('authorId')
    authorName = StringField('authorName')

    affiliationId = StringField('affiliationId')
    affiliationName = StringField('affiliationName')

    venueId = StringField('venueId')
    venueName = StringField('venueName')

    conceptId = StringField('conceptId')
    conceptName = StringField('conceptName')

    submit = SubmitField('确认')
