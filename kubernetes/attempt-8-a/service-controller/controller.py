import os
import requests
from kubernetes import client, config, watch

try:
    config.load_incluster_config()
except config.config_exception.ConfigException:
    config.load_kube_config()

def build_request(type, event_dict):
    return {
        'name': event_dict['metadata']['name'],
        'type': type,
        'kind': event_dict['kind'],
        'spec': event_dict['spec']
    }

if __name__ == "__main__":
    namespace = os.environ.get('NAMESPACE', 'default')
    xds_service_name = os.environ.get('XDS_SERVICE_NAME', 'http://localhost')
    xds_port_number = os.environ.get('XDS_PORT_NUMBER', '7001')
    xds_endpoint = os.environ.get('XDS_ENDPOINT', '/v1/service')

    w = watch.Watch()
    core_api = client.CoreV1Api()
    for event in w.stream(core_api.list_namespaced_service, namespace=namespace):
        requests.post(
            f'{xds_service_name}:{xds_port_number}{xds_endpoint}',
            json=build_request(
                event['type'],
                event['object'].to_dict()
            )
        )
