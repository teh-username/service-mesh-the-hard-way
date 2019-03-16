from flask import Flask, request
import requests
import sys

app = Flask(__name__)

# /service?flow=bccb
@app.route('/service')
def service_hello():
    flow=request.args.get('flow')
    print(f"Hello from service {flow[0]} -- flow: {flow}", file=sys.stderr)
    if len(flow) > 1:
        print(f"Requesting: http://service-{flow[1]}:8080/service?flow={flow[1:]}", file=sys.stderr)
        requests.get(f"http://service-{flow[1]}:8080/service?flow={flow[1:]}")

    return ""

if __name__ == "__main__":
  app.run(host='127.0.0.1', port=8080, debug=True)
