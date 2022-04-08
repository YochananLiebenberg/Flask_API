from flask import Flask, jsonify, request
app=Flask(__name__)

@app.route("/addseven",methods=['GET','POST'])
def index():
    if request.method=='GET':
          
    number = request.args.get('number')
    result = number + 7
    return jsonify(result)
    else:
        return jsonify({'Error':"This is a GET API method"})
    
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=9007)
