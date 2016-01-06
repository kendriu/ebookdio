from flask import Flask
from flask_bootstrap import Bootstrap
from decorators import templated


def create_app():
    app = Flask(__name__)
    app.debug = True
    Bootstrap(app)
    return app

app = create_app()


@app.route('/')
@templated()
def home():
    pass

if __name__ == "__main__":
    app.run()
