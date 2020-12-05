from flask import redirect, request, session, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from fooding import app, db
from fooding.models import Meal, MealCategory, Order, User

admin = Admin(app)

admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(MealCategory, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(User, db.session))


@app.before_request
def admin_access_control():
    if 'admin' in request.url:
        user_id = session.get('user_id')
        if not user_id:
            flash('Войдите, чтобы получить доступ к этой странице!')
            return redirect('/auth/')
        elif int(user_id) > 2:
            flash('Вы не имеете доступ к этой странице!')
            return redirect('/account/')
