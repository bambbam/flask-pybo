from flask import Blueprint,render_template, request, url_for,g,flash
from pybo.models import Question, Answer, User, question_voter, answer_voter
from ..forms import QuestionForm,AnswerForm
from datetime import datetime
from .. import db
from werkzeug.utils import redirect
from .auth_views import login_required
from sqlalchemy import func
bp = Blueprint('question',__name__,url_prefix='/question')


@bp.route('/list/')
def _list():
    page = request.args.get('page',type=int,default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='')

    if so == 'recommend':
        subquery = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()
        question_list = Question.query \
            .outerjoin(subquery, Question.id==subquery.c.question_id) \
            .order_by(subquery.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        subquery = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()
        question_list = Question.query \
            .outerjoin(subquery, Question.id == subquery.c.question_id) \
            .order_by(subquery.c.num_answer.desc(), Question.create_date.desc())
    else:
        question_list = Question.query.order_by(Question.create_date.desc())

    #조회
    if kw:
        search = '%%{}%%'.format(kw)
        subquery = db.session.query(Answer.question_id, Answer.content, User.user_name) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(subquery, subquery.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search)  |
                    Question.content.ilike(search)  |
                    User.user_name.ilike(search)    |
                    subquery.c.content.ilike(search)|
                    subquery.c.user_name.ilike(search)
                    )\
            .distinct()
    question_list = question_list.paginate(page,per_page=10)
    return render_template('question/question_list.html',question_list=question_list, page=page, kw=kw, so=so);

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    page = request.args.get('page',type=int,default=1)
    question = Question.query.get_or_404(question_id)

    sub_query = db.session.query(answer_voter.c.answer_id, func.count('*').label('num_voter')) \
        .group_by(answer_voter.c.answer_id).subquery()

    answer_list = Answer.query \
        .outerjoin(sub_query, Answer.id == sub_query.c.answer_id) \
        .order_by(sub_query.c.num_voter.desc(),Answer.create_date.desc())

    answer_list = answer_list.filter(Answer.question_id == question.id).order_by()
    answer_list = answer_list.paginate(page,per_page=3)
    return render_template('question/question_detail.html',question = question, answer_list=answer_list, page=page, form = form);

@bp.route('/create/', methods=('GET','POST'))
@login_required
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html',form = form)
@bp.route('/modify/<int:question_id>',methods=('GET','POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("수정권한이 없습니다.")
        return redirect(url_for('question_detail',question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail',question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))