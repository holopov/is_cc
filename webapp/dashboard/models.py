from datetime import datetime
import locale
import platform

from sqlalchemy.orm import relationship

from webapp.db import db

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')

class Case(db.Model):
    __tablename__ = "case"
    id = db.Column(db.Integer, primary_key=True)
    number_case = db.Column(db.String, unique=True, nullable=False)
    applicant = db.Column(db.String, nullable=False)
    type_applicant = db.Column(db.Integer, db.ForeignKey('type_applicant.id'), default=1)
    appraiser  = db.Column(db.String, nullable=True)
    judge = db.Column(db.String, nullable=True)
    status_case = db.Column(db.Integer, db.ForeignKey('status_case.id'), default=1)
    stage = db.Column(db.String, nullable=True)
    comment = db.Column(db.String, nullable=True)
    date_added = db.Column(db.DateTime, nullable=True, default=datetime.now())

    @property
    def fstage(self):
        if self.stage is None:
            return ''
        return self.stage

    @property
    def fcomment(self):
        if self.comment is None:
            return ''
        return self.comment

    def status_case_description(self):
        status = StatusCase.query.filter(StatusCase.id == self.status_case).first()
        return status.description

    def count_documents(self):
        return Document.query.filter(Document.number_case == self.number_case).count()

    def count_events(self):
        return Event.query.filter(Event.number_case == self.number_case).count()

    def count_objects(self):
        return RealtyObject.query.filter(RealtyObject.number_case == self.number_case).count()

    def __repr__(self):
        return f'Case: {self.number_case}, id: {self.id}>'

class RealtyObject(db.Model):
    __tablename__ = "realty_object"
    id = db.Column(db.Integer, primary_key=True)
    cadastral_number = db.Column(db.String, nullable=False, index=True)
    type_realty = db.Column(db.Integer, db.ForeignKey('type_realty.id'))
    category = db.Column(db.String, db.ForeignKey('categories.id'))
    article = db.Column(db.String, nullable=True)
    current_cadastral_cost = db.Column(db.Float, nullable=True)
    new_cadastral_cost = db.Column(db.Float, nullable=True)
    approved_cadastral_cost = db.Column(db.Float, nullable=True)
    segment = db.Column(db.Integer, nullable=True)
    codervi = db.Column(db.String, nullable=True)
    number_case = db.Column(db.String, db.ForeignKey('case.number_case'), index=True)

    case = relationship('Case', backref='objects')

    @property
    def fcurrent_cadastral_cost(self):
        return locale.format_string("%.2f",(self.current_cadastral_cost), grouping=True)

    @property
    def fnew_cadastral_cost(self):
        return locale.format_string("%.2f",(self.new_cadastral_cost), grouping=True)

    @property
    def fapproved_cadastral_cost(self):
        return locale.format_string("%.2f",(self.approved_cadastral_cost), grouping=True)

    @property
    def percent(self):
        if self.approved_cadastral_cost is not None and self.approved_cadastral_cost > 0:
            return locale.format_string("%.2f",(100 - (self.approved_cadastral_cost / self.current_cadastral_cost * 100)), grouping=True)
            #return '{:.2f}'.format(100 - (self.approved_cadastral_cost / self.current_cadastral_cost * 100))
        if self.new_cadastral_cost is not None and self.new_cadastral_cost > 0:
            #return '{:.2f}'.format(100 - (self.new_cadastral_cost / self.current_cadastral_cost * 100))
            return locale.format_string("%.2f",(100 - (self.new_cadastral_cost / self.current_cadastral_cost * 100)), grouping=True)
        return '-'

    def __repr__(self):
        return f'<Realty object: {self.cadastral_number} for case {self.number_case}>'

class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=True)
    date = db.Column(db.String, nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('type_document.id'))
    url = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=True)
    size = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String, nullable=True)
    number_case = db.Column(db.String, db.ForeignKey('case.number_case'), index=True)
    expert = db.Column(db.String, nullable=True)
    type_examination = db.Column(db.String, nullable=True)
    parent_document = db.Column(db.Integer, nullable=True)

    case = relationship('Case', backref='documents')

    @property
    def fcomment(self):
        if self.comment is None:
            return ''
        return self.comment

    @property
    def fdate(self):
        return datetime.strptime(self.date,'%Y-%m-%d').strftime('%d.%m.%Y')

    @property
    def fexpert(self):
        if self.expert is None:
            return ''
        return self.expert

    @property
    def ftype_examination(self):
        if self.type_examination is None or self.type_examination == '':
            return ''
        return self.type_examination

    @property
    def fnumber(self):
        if self.number is None:
            return ''
        return self.number

    @property
    def file_size(self):
        try:
            size = self.size / 1024
            if size < 1024:
                return f'{size:.2f} Кб'
            else:
                size /= 1024
                return f'{size:.2f} Мб'
        except:
            return 0

    @property
    def file_type_icon(self):
        file_types = {'docx':'icon_doc.png', 'doc':'icon_doc.png', 'xlsx':'icon_xls.png', 'xls':'icon_xls.png',
                  'pdf':'icon_pdf.png', 'odt':'icon_odt.png', 'ods':'icon_ods.png', 'txt':'icon_txt.png',
                  'zip':'icon_zip.png', }
        if self.extension is not None and self.extension.lower() in file_types:
            return file_types[self.extension.lower()]
        return '_Documents.png'


    def __repr__(self):
        return f'<Document: {self.title} for case {self.number_case}>'

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=True)
    comment = db.Column(db.String, nullable=True)
    number_case = db.Column(db.String, db.ForeignKey('case.number_case'), index=True)

    case = relationship('Case', backref='events')

    @property
    def fdate(self):
        return datetime.strptime(self.date,'%Y-%m-%d').strftime('%d.%m.%Y')

    @property
    def ftime(self):
        if self.time is None:
            return ''
        return self.time

    @property
    def fcomment(self):
        if self.comment is None:
            return ''
        return self.comment

    def __repr__(self):
        return f'<Event: {self.date} for case {self.number_case}>'

class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    description_lite = db.Column(db.String, nullable=True)
    type_realty = db.Column(db.String, db.ForeignKey('type_realty.id'))
    
    realty = relationship('RealtyObject', backref='category_description')

    def __repr__(self):
        return f'Category: {self.id}, {self.description}>'

class TypeApplicant(db.Model):
    __tablename__ = "type_applicant"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'<Type applicant: {self.id}, {self.description}>'

class TypeDocument(db.Model):
    __tablename__ = "type_document"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    
    document = relationship('Document', backref='type_description')

    def __repr__(self):
        return f'Type document: {self.id}, {self.description}>'

class TypeRealty(db.Model):
    __tablename__ = "type_realty"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'Type realty: {self.id}, {self.description}>'

class StatusCase(db.Model):
    __tablename__ = "status_case"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'Status case: {self.id}, {self.description}>'
