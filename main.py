import os
import time

import flask

import models.locators
import models.repositories
import models.responses
import models.services


app = flask.Flask(__name__)


@app.before_first_request
def before_first_request():
    #context = models.repositories.GuestbookRepositoryMemoryContext()
    #RepoClass = models.locators.GuestbookRepositoryLocator.resolve('memory')
    context = models.repositories.GuestbookRepositoryDatabaseContext('guestbook.db')
    RepoClass = models.locators.GuestbookRepositoryLocator.resolve('sqlite')
    ServClass = models.locators.GuestbookServiceLocator.resolve('default')
    app.service = ServClass(RepoClass(context))


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route('/guestbook', methods=['GET'])
def guestbook_get():
    try:
        count = int(flask.request.values.get('count', 10))
    except (ValueError, TypeError):
        return models.responses.GuestbookNullResponse(400).flask()
    command = models.services.GuestbookGetCommand(count)
    posts = app.service.get(command)
    return models.responses.GuestbookGetResponse(posts, 200).flask()


@app.route('/guestbook', methods=['POST'])
def guestbook_post():
    try:
        name = flask.request.values['name']
        message = flask.request.values['message']
        timestamp = time.time()
        remoteaddr = os.environ.get('REMOTE_ADDR')
    except KeyError:
        return models.responses.GuestbookNullResponse(400).flask()
    command = models.services.GuestbookPostCommand(
        name, message, timestamp, remoteaddr
    )
    post = app.service.post(command)
    return models.responses.GuestbookPostResponse(post, 200).flask()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
