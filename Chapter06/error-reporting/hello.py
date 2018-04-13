# Sample code to demonstrate GCP Error Reporting

from flask import Flask
app = Flask(__name__)
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/error_reporting/api/report_exception.py 
def simulate_error():
    from google.cloud import error_reporting
    client = error_reporting.Client()
    try:
        # simulate calling a method that's not defined
        raise NameError
    except Exception:
        client.report_exception()
def report_manual_error():
    from google.cloud import error_reporting
    client = error_reporting.Client()
    client.report("An error has occurred.")
@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/error')
def error_reporting():
    simulate_error()
    report_manual_error()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
