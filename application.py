from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, Request

from rss import get_items

application = Flask(__name__)

def pull_feed():
    items = get_items()
    return items

@application.route('/', methods=['GET', 'POST'])
def main():
    return 'hello world'

# if __name__ == "__main__":
#     application.run( debug=True)