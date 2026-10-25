import os
from pathlib import Path
from secrets import compare_digest

from dotenv import load_dotenv
from flask import Flask, request, redirect, render_template

from app.utils.rss import get_items, check_banner
from app.utils.mail import Mail


load_dotenv(Path(__file__).resolve().parent.parent / '.env')

app = Flask(__name__)
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', '')

@app.route('/', methods=['GET'])
def main():
    items = get_items()
    banner = check_banner()

    return(render_template('main.html', items=items, banner=banner))

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/legal/')
def legal():
    return render_template('legal.html')

@app.route('/podcast/')
def podcast():
    return render_template('podcast.html')

@app.route('/podcastrss/')
def podcastrss():
    return redirect('https://wplnnewscast.s3.us-east-2.amazonaws.com/rss/feed.xml')

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        password = request.form['password']
        message = request.form['message']
        admin_password = app.config['ADMIN_PASSWORD']
        if admin_password and compare_digest(password.encode('utf-8'), admin_password.encode('utf-8')):
            with open('message.txt', 'w') as banner:
                banner.write(message)
                banner.close()
            return render_template('admin.html', emoji='&#128077;', banner_text = check_banner())
        else:   
            return render_template('admin.html', emoji='&#128078;', banner_text = check_banner())

    return render_template('admin.html', banner_text = check_banner())

@app.route('/contact/', methods=['GET', 'POST'] )    
def contact():
    if request.method == 'POST':

        if not request.form["notabot"]:
            return "you're no good, you're no good"

        email_address = request.form['email_address']
        if email_address == '':
            email_address = 'not provided'

        email_message = request.form['email_message']

        to_send = f'Email Address: {email_address}\nEmail Message:\n{email_message}'
        Mail().send_email(body=to_send)

        return render_template('post_contact.html', emoji='&#128077;')

    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def page_not_found(e):
    return "you're no good, you're no good", 405

@app.errorhandler(500)
def internal_error(e):
    return render_template("broken.html"), 500
