# Flask modules
from flask import Blueprint, redirect, url_for, render_template, flash, current_app, flash
import yaml

ui_blueprints = Blueprint('dashboard', __name__, url_prefix='/ui')

@ui_blueprints.context_processor
def inject_pages():
    return dict(pages=current_app.config['UI_PAGES'])

@ui_blueprints.route('/')
@ui_blueprints.route('/<page>')
def ui(page=None):
    print(page)
    pages = current_app.config['UI_PAGES']
    if not page:
        page = next(iter(pages))
    if page in pages:
        if pages[page]['type'] == 'iframe':
            return iframe(pages[page]['url'])
        elif pages[page]['type'] == 'dashboard':
            return dashboard(pages[page]['layout'])
        else:
            not_found(page)


def not_found(page):
    error_message = f'Requested page not found: {page}'
    current_app.logger.error(error_message)
    return render_template('error.html', error_message=error_message)

def iframe(url):
    return render_template('iframe.html', page=url)

def dashboard(layout_path):
    try:
        with open(layout_path, 'r') as f:
            layout_raw = f.read()
            layout = yaml.safe_load(layout_raw)
    except Exception as e:
        error_message = f'Error reading file: {e}'
        current_app.logger.error(error_message)
        return render_template('error.html', error_message=error_message)
    
    return render_template('dashboard.html', layout=layout)