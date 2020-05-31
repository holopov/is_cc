import os
from datetime import datetime

from flask import current_app, Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_required
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from webapp.db import db
from webapp.case.forms import case_form_factory, DocumentForm, EventForm, SearchForm
from webapp.dashboard.models import Case, Document, Event
from webapp.user.decorators import lawyer_required

blueprint = Blueprint('case', __name__, url_prefix='/case')


@blueprint.route("/")
@login_required
def show_last_case():
    content = {}
    content['cases'] = Case.query.order_by(Case.id.desc()).limit(10)
    return render_template('case/index.html', **content)

@blueprint.route("/search", methods=['GET'])
@login_required
def search_case():
    search_string = request.args.get('search_string').strip()
    if search_string:
        content = {}
        content['cases'] = Case.query.filter(or_(Case.number_case.like(f'%{search_string}%'), Case.applicant.like(f'%{search_string}%'), Case.judge.like(f'%{search_string}%'))).order_by(Case.number_case).all()
        return render_template('case/index.html', **content)
    else:
        flash('Ничего не найдено')
        return render_template('case/index.html')

@blueprint.route("/<int:case_id>")
@login_required
def case_information(case_id):
    content = {}
    content['case'] = Case.query.filter(Case.id==case_id).first()
    return render_template('case/single_case.html', **content)

@blueprint.route("/add", methods=['GET'])
@lawyer_required
def add_case():
    form = case_form_factory()()
    return render_template('case/add/case.html', form=form)

@blueprint.route("/add", methods=['POST'])
@lawyer_required
def add_case_process():
    form = case_form_factory()()
    if form.validate_on_submit():
        case = Case(number_case=form.number_case.data, applicant=form.applicant.data, type_applicant=form.type_applicant.data.id,
                    appraiser=form.appraiser.data, judge=form.judge.data, comment=form.comment.data)
        db.session.add(case)
        db.session.commit()
        try:            
            os.mkdir(os.path.join(current_app.config['DOCUMENTS'], str(case.id)))
        except:
            flash(f'Ошибка при создании папки для Дела с номером {form.number_case.data}')
            db.session.delete(case)
            db.session.commit()
            return redirect(url_for('case.case_information', case_id=case.id))
        flash(f'Дело с номером {form.number_case.data} успешно добавлено в базу')
        return redirect(url_for('case.show_last_case'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: - {error}')
        return redirect(url_for('case.add_case', form=form))
    
@blueprint.route("/edit/case/<int:case_id>", methods=['GET'])
@lawyer_required
def edit_case(case_id):
    content = {}
    content['case'] = Case.query.filter_by(id=case_id).first()
    content['form'] = case_form_factory(default_type_applicant=content['case'].type_applicant,
                                        default_status_case=content['case'].status_case)(number_case=content['case'].number_case, applicant=content['case'].applicant,
                                                                                        judge=content['case'].judge, appraiser=content['case'].appraiser, comment=content['case'].comment)
    return render_template('case/edit/case.html', **content)

@blueprint.route("/edit/case/<int:case_id>", methods=['POST'])
@lawyer_required
def edit_case_process(case_id):
    form = case_form_factory(is_activate_check_number_case=0)()
    case = Case.query.filter(Case.id==case_id).first()
    if form.validate_on_submit():
        #case.number_case = form.number_case.data
        case.applicant = form.applicant.data
        case.type_applicant = form.type_applicant.data.id
        case.judge = form.judge.data
        case.appraiser = form.appraiser.data
        case.status_case = form.status_case.data.id
        case.comment = form.comment.data
        db.session.add(case)
        db.session.commit()
        return redirect(url_for('case.case_information', case_id=case.id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: - {error}')
        content = {}
        content['case'] = case
        content['form'] = case_form_factory(default_type_applicant=content['case'].type_applicant,
                                            default_status_case=content['case'].status_case)(number_case=content['case'].number_case, applicant=content['case'].applicant,
                                                                                        judge=content['case'].judge, appraiser=content['case'].appraiser, comment=content['case'].comment)
        return render_template('case/edit/case.html', **content)


@blueprint.route("/add/document/<int:case_id>")
@lawyer_required
def add_document(case_id):
    content = {}
    content['form'] = DocumentForm(case_id=case_id)
    content['case'] = Case.query.get(case_id)
    return render_template('case/add/document.html', **content)
    return f'Добавить документ в дело {case_id}'

@blueprint.route("/add/document/<int:case_id>", methods=['POST'])
@lawyer_required
def add_document_process(case_id):
    form = DocumentForm()
    if form.validate_on_submit():
        case = Case.query.get(form.case_id.data)
        f = form.upload.data
        filename = os.path.join(current_app.config['DOCUMENTS'], str(case.id), secure_filename(f.filename)) 
        # app.instance_path
        if not os.path.exists(filename):
            f.save(filename)
            document = Document(number_case=case.number_case, title=form.title.data, number=form.number.data, date=form.date.data,
                                type=form.type_document.data.id, url=secure_filename(f.filename), size=os.path.getsize(filename),
                                extension=os.path.splitext(filename)[1][1:], comment=form.comment.data)
            db.session.add(document)
            db.session.commit()
            return redirect(url_for('case.case_information', case_id=case_id, _anchor='block3'))
        else:
            flash(f'Файл с именем {f.filename} уже был загружен ранее', 'error')
            return redirect(url_for('case.add_document', case_id=case_id))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: - {error}')
        return redirect(url_for('case.add_document', case_id=case_id))

@blueprint.route("/delete/document/<int:document_id>", methods=['POST'])
@lawyer_required
def delete_document(document_id):
    document = Document.query.get(document_id)
    case = Case.query.filter_by(number_case=document.number_case).first()
    os.remove(os.path.join(current_app.config['DOCUMENTS'], str(case.id), document.url))
    db.session.delete(document)
    db.session.commit()
    return redirect(url_for('case.case_information', case_id=case.id, _anchor='block3'))

@blueprint.route("/add/object/<int:case_id>")
@lawyer_required
def add_object(case_id):
    return f'Добавить объект в дело {case_id}'

@blueprint.route("/add/examination/<int:case_id>")
@lawyer_required
def add_examination(case_id):
    return f'Добавить экспертизу в дело {case_id}'

@blueprint.route("/add/event/<int:case_id>", methods=['GET'])
@lawyer_required
def add_event(case_id):
    content = {}
    content['form'] = EventForm(case_id=case_id)
    content['case'] = Case.query.get(case_id)
    return render_template('case/add/event.html', **content)

@blueprint.route("/add/event/<int:case_id>", methods=['POST'])
@lawyer_required
def add_event_process(case_id):
    form = EventForm()
    if form.validate_on_submit():
        case = Case.query.get(form.case_id.data)
        event = Event(date=form.date_event.data, time=form.time_event.data, comment=form.comment.data, number_case=case.number_case)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('case.case_information', case_id=case_id, _anchor='block6'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: - {error}')
        return redirect(url_for('case.add_event', case_id=case_id))

@blueprint.route("/edit/event/<int:event_id>", methods=['GET'])
@lawyer_required
def edit_event(event_id):
    content = {}
    event = Event.query.filter_by(id=event_id).first()
    content['case'] = Case.query.filter_by(number_case=event.number_case).first()
    content['event'] = event
    content['form'] = EventForm(case_id=content['case'].id, date_event=datetime.strptime(event.date,'%Y-%m-%d'), time_event=event.time, comment=event.comment)
    return render_template('case/edit/event.html', **content)

@blueprint.route("/edit/event/<int:event_id>", methods=['POST'])
@lawyer_required
def edit_event_process(event_id):
    form = EventForm()
    if form.validate_on_submit():
        event = Event.query.get(event_id)
        event.date = form.date_event.data
        event.time = form.time_event.data
        event.comment = form.comment.data
        db.session.add(event)
        db.session.commit()
        case = Case.query.filter_by(number_case=event.number_case).first()
        return redirect(url_for('case.case_information', case_id=case.id, _anchor='block6'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле {getattr(form, field).label.text}: - {error}')
        return 'Ошибка при редактировании формы.'

@blueprint.route("/delete/event/<int:event_id>", methods=['POST'])
@lawyer_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    case = Case.query.filter_by(number_case=event.number_case).first()
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('case.case_information', case_id=case.id, _anchor='block6'))
