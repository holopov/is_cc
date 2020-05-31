from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import DateField, HiddenField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from webapp.dashboard.models import Case, Event, StatusCase, TypeApplicant, TypeDocument

ALLOWED_EXTENSIONS = ['txt', 'tiff', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'odt', 'ods', '7z', 'zip', 'rar']

def case_form_factory(default_type_applicant=None, default_status_case=1, is_activate_check_number_case=1):
    class CaseForm(FlaskForm):
        if is_activate_check_number_case:
            number_case = StringField('Номер дела', validators=[DataRequired()], render_kw={'class':'validate'})
        else:
            number_case = StringField('Номер дела', render_kw={'class':'validate'})
        applicant = StringField('Истец', validators=[DataRequired()], render_kw={'class':'validate'})
        if default_type_applicant is None:
            type_applicant = QuerySelectField('Статус истца', validators=[DataRequired()], query_factory=lambda: TypeApplicant.query.all(),
                                                get_pk=lambda item:item.id, get_label='description', allow_blank=True)
        else:
            type_applicant = QuerySelectField('Статус истца', validators=[DataRequired()], query_factory=lambda: TypeApplicant.query.all(),
                                                get_pk=lambda item:item.id, get_label='description',
                                                default=lambda: TypeApplicant.query.filter(TypeApplicant.id==default_type_applicant).first())
        appraiser = StringField('Рыночный оценщик', render_kw={'class':'validate'})
        judge = StringField('Судья', render_kw={'class':'validate'})
        status_case = QuerySelectField('Статус дела', validators=[DataRequired()], query_factory=lambda: StatusCase.query.all(),
                                            get_pk=lambda item:item.id, get_label='description', allow_blank=False,
                                            default=lambda: StatusCase.query.filter(StatusCase.id==default_status_case).first())
        comment = TextAreaField('Комментарий', render_kw={'class':'materialize-textarea'})
        submit = SubmitField('Добавить заседание', render_kw={'class':'btn waves-effect waves-light white-text'})

        def validate_number_case(self, number_case, is_activate_check_number_case=1):
            if is_activate_check_number_case and Case.query.filter_by(number_case = number_case.data).count() > 0:
                raise ValidationError('Дело с таким номером уже существует')
    return CaseForm

class DocumentForm(FlaskForm):
    case_id = HiddenField('ID дела', validators=[DataRequired()])
    title = StringField('Наименование', validators=[DataRequired()], render_kw={'class':'validate'})
    type_document = QuerySelectField('Тип документа', validators=[DataRequired()], query_factory=lambda: TypeDocument.query.all(),
                                        get_pk=lambda item:item.id, get_label=lambda item:item.description, allow_blank=True)
    number = StringField('Номер документа', render_kw={'class':'validate'})
    date = DateField('Дата документа', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'class':'validate'})
    comment = TextAreaField('Комментарий', render_kw={'class':'materialize-textarea'})
    upload = FileField('Файл', validators=[FileRequired(),
                                FileAllowed(ALLOWED_EXTENSIONS, 'Загрузка данного типа документа запрещена')])
    submit = SubmitField('Загрузить', render_kw={'class':'btn waves-effect waves-light white-text'})

    def validate_case_id(self, case_id):
        if not Case.query.get(case_id.data):
            raise ValidationError('Дело не существует')

class EventForm(FlaskForm):
    case_id = HiddenField('ID дела', validators=[DataRequired()])
    date_event = DateField('Дата заседания', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'class':'datepicker'})
    time_event = StringField('Время заседания', render_kw={'class':'timepicker'})
    comment = TextAreaField('Комментарий', render_kw={'class':'materialize-textarea'})
    submit = SubmitField('Добавить заседание', render_kw={'class':'btn waves-effect waves-light white-text'})

    def validate_case_id(self, case_id):
        if not Case.query.get(case_id.data):
            raise ValidationError('Дело не существует')

class SearchForm(FlaskForm):
    search_string = StringField('Текст для поиска',  validators=[DataRequired()], render_kw={'class':'validate'})
    submit = SubmitField('Искать', render_kw={'class':'btn waves-effect waves-light white-text'})
