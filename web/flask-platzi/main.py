
import unittest

from flask import request, make_response, redirect, render_template, session, url_for, flash

from app import create_app
from app.forms import LoginForm


app = create_app()

todos = [
    'Comprar cafe',
    'Enviar solicitud de compra',
    'Entregar video al productor'
]



@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/healthcheck'))
    session['user_ip'] = user_ip

    return response


@app.route('/healthcheck', methods=['GET', 'POST'])
def healthcheck():
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username,
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('Nombre de usuario registrado con exito')

        return redirect(url_for('index'))

    return render_template('hello.html', **context)


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)
