from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

@app.route('/v2/discovery:clusters', methods=['GET', 'POST'])
def cluster_discovery():
    print(f"Request received for cluster discovery", file=sys.stderr)
    print(request.get_json(), file=sys.stderr)
    return jsonify({
        'version_info': '0',
        'resources': [
            {
                '@type': 'type.googleapis.com/envoy.api.v2.Cluster',
                'name': 'local_service',
                'connect_timeout': '0.25s',
                'type': 'strict_dns',
                'lb_policy': 'round_robin',
                'load_assignment': {
                    'cluster_name': 'local_service',
                    'endpoints': [
                        {
                            'lb_endpoints': [
                                {
                                    'endpoint': {
                                        'address': {
                                            'socket_address': {
                                                'address': '127.0.0.1',
                                                'port_value': '8080'
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    })


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
