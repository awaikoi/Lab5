import os
from datetime import datetime

from flask import Flask, render_template, session

import models

from routes import admin_bp, feedback_bp, shop_bp, api_v1, api_v2
from routes.api.errors import register_error_handlers

app = Flask(__name__)
app.config['DATABASE'] = os.environ.get('DATABASE', os.path.join(app.root_path, 'db.sqlite'))
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 + 256 * 1024
app.register_blueprint(api_v1)
app.register_blueprint(api_v2)
register_error_handlers(app)

app.teardown_appcontext(models.close_db)

with app.app_context():
    models.init_db()

app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)


@app.template_filter('money')
def money(value):
    return f'{value:.2f} грн'


@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'cart_count': sum(session.get('cart', {}).values()),
    }


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)

