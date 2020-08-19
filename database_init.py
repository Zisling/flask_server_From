from shared_resources import db
from app import create_app


def database_init():
    app = create_app()
    app.app_context().push()
    db.create_all()


if __name__ == '__main__':
    database_init()
