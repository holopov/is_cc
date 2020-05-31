from flask import Blueprint, render_template
from flask_login import current_user, login_required

from webapp.db import db
from webapp.dashboard.models import Case, Event
from webapp.user.decorators import lawyer_required

blueprint = Blueprint('event', __name__, url_prefix='/event')

@blueprint.route("/")
@lawyer_required
def add_event():
    return 'Добавление события с указанием дела'
    # content = {}
    # content['count_case'] = Case.query.count()
    # content['count_case_complete'] = Case.query.filter(Case.status_case==0).count()
    # content['count_parcels'] = RealtyObject.query.filter(RealtyObject.type_realty==0).count()
    # content['count_realty'] = RealtyObject.query.filter(RealtyObject.type_realty==1).count()
    # if current_user.is_authenticated and current_user.is_user:
    #     content['cases'] = Case.query.order_by(Case.id.desc()).limit(3)
    #     content['events'] = Event.query.order_by(Event.id.desc()).limit(3)
    # return render_template('dashboard/index.html', **content)
    