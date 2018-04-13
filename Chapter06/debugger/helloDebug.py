# Sample code to demonstrate GCP Debugger 
from flask import Flask
import re
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! - testing Debugger'

@app.route('/add/<int_list>')
# Thanks to :
# https://stackoverflow.com/questions/35437180/capture-a-list-of-integers-with-a-flask-route
def index(int_list):
    # Make sure it is a list that only contains integers.
    if not re.match(r'^\d+(?:,\d+)*,?$', int_list):
        return "Please input a list of integers, split with ','"
    result = sum(int(i) for i in int_list.split(','))
    return "{0}".format(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
