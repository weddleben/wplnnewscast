import os

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, Request

from rss import get_items, check_banner

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def main():
    items = get_items()
    length = len(items)

    banner = check_banner()

    return(render_template('main.html', items=items, length=length, banner=banner))

@application.route('/about/')
def about():
    return render_template('about.html')

@application.route('/podcast/')
def podcast():
    return render_template('podcast.html')

@application.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        user = request.form['user']
        message = request.form['message']
        if user == 'hackmebitches':
            with open('message.txt', 'w') as banner:
                banner.write(message)
                banner.close()
        else:
            return render_template('admin.html', emoji='&#128078;')

    return render_template('admin.html')
    


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.errorhandler(500)
def internal_error(e):
    return render_template("broken.html"), 500

if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=2122)