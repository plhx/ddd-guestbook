import flask

from core.apps import *
from core.models import *
from infrastructures import *
from presentations import *

app = flask.Flask(
    __name__,
    static_folder='view/static',
    template_folder='view/templates'
)


@app.before_first_request
def before_first_request():
    context = GuestbookRepositoryMemoryContext()
    app.repository = GuestbookMemoryRepository(context)
    #context = GuestbookRepositoryDatabaseContext('guestbook.db')
    #app.repository = GuestbookSQLiteRepository(context)
    app.request = GuestbookFlaskRequest()
    app.converter = FlaskResponseConverter()


@app.route('/', methods=['GET'])
def index():
    return app.converter.convert(RenderHTMLResponse('index.html'))


@app.route('/guestbook', methods=['GET'])
def guestbook_get():
    try:
        count = int(app.request.params('count', 10))
    except (KeyError, ValueError, TypeError):
        return app.converter.convert(HTTPResponse('', 400))
    command = GuestbookGetCommand(count)
    return app.converter.convert(GuestbookResponse(
        GuestbookGetUseCase(app.repository).execute(command),
        200
    ))


@app.route('/guestbook', methods=['POST'])
def guestbook_post():
    try:
        count = int(app.request.params('count', 10))
        name = app.request.data('name')
        message = app.request.data('message')
    except (KeyError, ValueError, TypeError):
        return app.converter.convert(HTTPResponse('', 400))
    command = GuestbookAddCommand(
        Name(name),
        Message(message),
        Timestamp.now(),
        app.request.remote_addr()
    )
    GuestbookAddUseCase(app.repository).execute(command)
    command = GuestbookGetCommand(count)
    return app.converter.convert(GuestbookResponse(
        GuestbookGetUseCase(app.repository).execute(command),
        200
    ))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
