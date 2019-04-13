import os
import sys

from flask import Flask, request, jsonify
from route import RouteBuilder
from cluster import ClusterBuilder

app = Flask(__name__)
routes = RouteBuilder()
clusters = ClusterBuilder()

@app.route('/v1/service', methods=['POST'])
def service():
    service_json = request.get_json()

    print(f"Request received for service update", file=sys.stderr)
    print(service_json, file=sys.stderr)

    action = service_json['type']
    name = service_json['name']
    ports = [port['port'] for port in service_json['spec']['ports']]

    routes.process_route(
        action,
        name,
        ports
    )

    clusters.process_cluster(
        action,
        name,
        ports
    )

    return jsonify({
        'success': True
    })

@app.route('/debug', methods=['GET'])
def debug():
    return jsonify({
        'routes': routes.get_versioned_routes(),
        'clusters': clusters.get_versioned_clusters()
    })

@app.route('/v2/discovery:routes', methods=['POST'])
def route_discovery():
    print(f"Request received for route discovery", file=sys.stderr)
    print(request.get_json(), file=sys.stderr)
    return jsonify(
        routes.get_versioned_routes()
    )

@app.route('/v2/discovery:clusters', methods=['POST'])
def cluster_discovery():
    print(f"Request received for cluster discovery", file=sys.stderr)
    print(request.get_json(), file=sys.stderr)
    return jsonify(
        clusters.get_versioned_clusters()
    )

if __name__ == "__main__":
    xds_port_number = os.environ.get('XDS_PORT_NUMBER', '7001')
    app.run(host='0.0.0.0', port=xds_port_number, debug=True)
