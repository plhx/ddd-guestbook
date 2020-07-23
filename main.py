import flask

from core.apps import *
from core.models import *
from infrastructures import *
from presentations import *

app = flask.Flask(__name__)


@app.before_first_request
def before_first_request():
    context = GuestbookRepositoryMemoryContext()
    app.repository = GuestbookMemoryRepository(context)

    #context = GuestbookRepositoryDatabaseContext('guestbook.db')
    #app.repository = GuestbookSQLiteRepository(context)

    app.request = GuestbookFlaskRequest()
    app.converter = GuestbookFlaskResponseConverter()


@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')


@app.route('/guestbook', methods=['GET'])
def guestbook_get():
    try:
        count = app.request.params('count', 10)
    except (KeyError, ValueError, TypeError):
        return app.converter.convert(GuestbookEmptyResponse(400))
    command = GuestbookGetCommand(count)
    response = GuestbookGetResponse(
        GuestbookGetUseCase(app.repository).execute(command),
        200
    )
    return app.converter.convert(response)


@app.route('/guestbook', methods=['POST'])
def guestbook_post():
    try:
        name = app.request.data('name')
        message = app.request.data('message')
    except (KeyError, ValueError, TypeError):
        return app.converter.convert(GuestbookEmptyResponse(400))
    command = GuestbookAddCommand(
        Name(name),
        Message(message),
        Timestamp.now(),
        app.request.remote_addr()
    )
    response = GuestbookAddResponse(
        GuestbookAddUseCase(app.repository).execute(command),
        200
    )
    return app.converter.convert(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
