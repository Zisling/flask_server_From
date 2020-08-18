from flask import Flask
import sqlite3

app = Flask(__name__)


@app.route('/' , methods=['GET'])
def hello_world():
    return 'Hello World!'

@app.route('/' , methods=['POST'])
def print_hello_world():
    print("hello world!")
    return ''

if __name__ == '__main__':
    app.run(port=5000)
