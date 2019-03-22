from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

service_a_cluster = {
    '@type': 'type.googleapis.com/envoy.api.v2.Cluster',
    'name': 'service_a_8080',
    'connect_timeout': '0.25s',
    'type': 'strict_dns',
    'lb_policy': 'round_robin',
    'load_assignment': {
        'cluster_name': 'service_a_8080',
        'endpoints': [
            {
                'lb_endpoints': [
                    {
                        'endpoint': {
                            'address': {
                                'socket_address': {
                                    'address': 'service-a',
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

service_b_cluster = {
    '@type': 'type.googleapis.com/envoy.api.v2.Cluster',
    'name': 'service_b_8080',
    'connect_timeout': '0.25s',
    'type': 'strict_dns',
    'lb_policy': 'round_robin',
    'load_assignment': {
        'cluster_name': 'service_b_8080',
        'endpoints': [
            {
                'lb_endpoints': [
                    {
                        'endpoint': {
                            'address': {
                                'socket_address': {
                                    'address': 'service-b',
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

service_c_cluster = {
    '@type': 'type.googleapis.com/envoy.api.v2.Cluster',
    'name': 'service_c_8080',
    'connect_timeout': '0.25s',
    'type': 'strict_dns',
    'lb_policy': 'round_robin',
    'load_assignment': {
        'cluster_name': 'service_c_8080',
        'endpoints': [
            {
                'lb_endpoints': [
                    {
                        'endpoint': {
                            'address': {
                                'socket_address': {
                                    'address': 'service-c',
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

init_cluster_config = {
    'version_info': '0',
    'resources': [
        service_a_cluster
    ]
}

cluster_config_lookup = {
    '0': {
        'version_info': '1',
        'resources': [
            service_a_cluster,
            service_b_cluster
        ]
    },
    '1': {
        'version_info': '2',
        'resources': [
            service_a_cluster,
            service_b_cluster,
            service_c_cluster
        ]
    }
}

@app.route('/v2/discovery:clusters', methods=['GET', 'POST'])
def cluster_discovery():
    discovery_request = request.get_json()

    print(f"Request received for cluster discovery", file=sys.stderr)
    print(discovery_request, file=sys.stderr)

    if 'version_info' not in discovery_request:
        return jsonify(init_cluster_config)

    discovery_response = cluster_config_lookup.get(
        discovery_request['version_info'],
        cluster_config_lookup['1']
    )

    return jsonify(discovery_response)

service_a_route = {
    'name': 'service_a',
    'domains': ['service-a:8080'],
    'routes': [
        {
            'match': { 'prefix': '/' },
            'route': { 'cluster': 'service_a_8080' }
        }
    ]
}

service_b_route = {
    'name': 'service_b',
    'domains': ['service-b:8080'],
    'routes': [
        {
            'match': { 'prefix': '/' },
            'route': { 'cluster': 'service_b_8080' }
        }
    ]
}

service_c_route = {
    'name': 'service_c',
    'domains': ['service-c:8080'],
    'routes': [
        {
            'match': { 'prefix': '/' },
            'route': { 'cluster': 'service_c_8080' }
        }
    ]
}

v0_egress_route = {
    '@type': 'type.googleapis.com/envoy.api.v2.RouteConfiguration',
    'name': 'egress_routes',
    'virtual_hosts': [service_a_route]
}

v1_egress_route = {
    '@type': 'type.googleapis.com/envoy.api.v2.RouteConfiguration',
    'name': 'egress_routes',
    'virtual_hosts': [service_a_route, service_b_route]
}

v2_egress_route = {
    '@type': 'type.googleapis.com/envoy.api.v2.RouteConfiguration',
    'name': 'egress_routes',
    'virtual_hosts': [service_a_route, service_b_route, service_c_route]
}

init_route_config = {
    'version_info': '0',
    'resources': [
        v0_egress_route
    ]
}

route_config_lookup = {
    '0': {
        'version_info': '1',
        'resources': [
            v1_egress_route
        ]
    },
    '1': {
        'version_info': '2',
        'resources': [
            v2_egress_route
        ]
    }
}

@app.route('/v2/discovery:routes', methods=['GET', 'POST'])
def route_discovery():
    discovery_request = request.get_json()

    print(f"Request received for route discovery", file=sys.stderr)
    print(discovery_request, file=sys.stderr)

    if 'version_info' not in discovery_request:
        return jsonify(init_route_config)

    discovery_response = route_config_lookup.get(
        discovery_request['version_info'],
        route_config_lookup['1']
    )

    return jsonify(discovery_response)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
