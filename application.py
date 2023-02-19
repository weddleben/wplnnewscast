from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, Request

from rss import get_items

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def main():
    items = get_items()
    length = len(items)
    return(render_template('main.html', items=items, length=length))

@application.route('/about/')
def about():
    return render_template('about.html')


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.errorhandler(500)
def internal_error(e):
    return render_template("broken.html"), 500

if __name__ == "__main__":
    application.run(debug=True)