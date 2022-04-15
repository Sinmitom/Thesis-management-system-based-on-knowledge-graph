from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField     # StringField对应HTML中type="text"的<input>元素，SubmitField对应type='submit'的<input>元素
from wtforms.validators import DataRequired, Length


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class NerForm(MyBaseForm):
    ner_text = TextAreaField('ner_text', validators=[DataRequired(), Length(0, 300)])  # 表单做数据验证
    submit = SubmitField('确认')


class EntityForm(MyBaseForm):
    entity = StringField('entity', validators=[DataRequired()])
    submit = SubmitField('查询')


class RelationForm(MyBaseForm):
    entity1 = StringField('entity1')
    relation = SelectField('relation', choices=[(1, '无限制')], default=1, coerce=int)
    entity2 = StringField('entity2')
    submit = SubmitField('查询')