
from flask import Flask, request, make_response, redirect, render_template


app = Flask(__name__)


todos = [
    'Comprar cafe',
    'Enviar solicitud de compra',
    'Entregar video al productor'
]


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/healthcheck'))
    response.set_cookie('user_ip', user_ip)

    return response


@app.route('/healthcheck')
def healtcheck():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }

    return render_template('hello.html', **context)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)
