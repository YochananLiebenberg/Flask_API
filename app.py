from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def hello():
    return {'message': "Hello world!"}, 200

if __name__ == '__main__':
    app.run(

    ) 
