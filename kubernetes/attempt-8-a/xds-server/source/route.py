class RouteBuilder(object):
    base_config = {
      '@type': 'type.googleapis.com/envoy.api.v2.RouteConfiguration',
      'name': 'egress_routes',
    }

    def __init__(self):
        self.services = {}
        self.version_info = 0

    def add_service(self, name, ports):
        self.services[name] = ports
        self.version_info += 1

    def remove_service(self):
        pass

    def update_service(self):
        pass

    def process_route(self, action, name, ports):
        if action == 'ADDED':
            self.add_service(
                name,
                ports
            )

    def _build_services_route(self):
        routes = []
        for service, ports in self.services.items():
            base_service = {
                'name': service,
                'domains': [f'{service}*'],
                'routes': []
            }
            for port in ports:
                base_service['routes'].append(
                    {
                        'match': {
                            'prefix': '/',
                            'headers': [{
                                'name': ':authority',
                                'suffix_match': f':{port}'
                            }]
                        },
                        'route': { 'cluster': f'{service}_{port}' }
                    }
                )

            routes.append(base_service)
        return routes

    def get_versioned_routes(self):
        return {
            'version_info': self.version_info,
            'resources': [
                {
                    **RouteBuilder.base_config,
                    **{
                        'virtual_hosts': self._build_services_route()
                    }
                }
            ]
        }
