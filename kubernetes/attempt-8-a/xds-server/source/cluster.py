class ClusterBuilder(object):
    base_config = {
        '@type': 'type.googleapis.com/envoy.api.v2.Cluster',
        'connect_timeout': '0.25s',
        'type': 'strict_dns',
        'lb_policy': 'round_robin',
    }

    def __init__(self):
        self.clusters = {}
        self.version_info = 0

    def add_cluster(self, name, ports):
        self.clusters[name] = ports
        self.version_info += 1

    def remove_cluster(self):
        pass

    def update_cluster(self):
        pass

    def process_cluster(self, action, name, ports):
        if action == 'ADDED':
            self.add_cluster(
                name,
                ports
            )

    def _build_clusters(self):
        clusters = []
        for cluster_name, ports in self.clusters.items():
            for port in ports:
                base_cluster = {
                    'name': f'{cluster_name}_{port}',
                    'load_assignment': {
                        'cluster_name': f'{cluster_name}_{port}',
                        'endpoints': [{
                            'lb_endpoints': [{
                                'endpoint': {
                                    'address': {
                                        'socket_address': {
                                            'address': cluster_name,
                                            'port_value': port
                                        }
                                    }
                                }
                            }]
                        }]
                    }
                }

                clusters.append({
                    **ClusterBuilder.base_config,
                    **base_cluster
                })

        return clusters

    def get_versioned_clusters(self):
        return {
            'version_info': str(self.version_info),
            'resources': self._build_clusters()
        }

