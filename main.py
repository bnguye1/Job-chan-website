from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         # email = request.form['email']
#         pass
#
#     else:
#         pass

if __name__ == '__main__':
    app.run(debug=True)
