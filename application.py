from flask import Flask, request, redirect, render_template

from utils.rss import get_items, check_banner
from utils.mail import Mail


application = Flask(__name__)

@application.route('/', methods=['GET'])
def main():
    items = get_items()
    length = len(items)

    banner = check_banner()

    return(render_template('main.html', items=items, length=length, banner=banner))

@application.route('/about/')
def about():
    return render_template('about.html')

@application.route('/legal/')
def legal():
    return render_template('legal.html')

@application.route('/podcast/')
def podcast():
    return render_template('podcast.html')

@application.route('/podcastrss/')
def podcastrss():
    return redirect('https://wplnnewscast.s3.us-east-2.amazonaws.com/rss/feed.xml')

@application.route('/admin/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        user = request.form['user']
        message = request.form['message']
        if user == 'hackmebitches':
            with open('message.txt', 'w') as banner:
                banner.write(message)
                banner.close()
            return render_template('admin.html', emoji='&#128077;')
        else:
            return render_template('admin.html', emoji='&#128078;')

    return render_template('admin.html')

@application.route('/contact/', methods=['GET', 'POST'] )    
def contact():
    if request.method == 'POST':

        email_address = request.form['email_address']
        if email_address == '':
            email_address = 'not provided'

        email_message = request.form['email_message']

        to_send = f'Email Address: {email_address}\nEmail Message:\n{email_message}'
        Mail().send_email(body=to_send)

        return render_template('post_contact.html', emoji='&#128077;')

    return render_template('contact.html')


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.errorhandler(405)
def page_not_found(e):
    return "you're no good, you're no good", 405

@application.errorhandler(500)
def internal_error(e):
    return render_template("broken.html"), 500

if __name__ == "__main__":
    application.run(debug=True)