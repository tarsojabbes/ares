import yaml

def map_service_config(service_name, service_info):
    config = {
        'image': service_info.get('image', 'default_image'),
        'ports': service_info.get('ports', []),
        'mem_limit': service_info.get('mem_limit', None),
        'cpus': service_info.get('cpus', None),
        'volumes': service_info.get('volumes', []),
        'environment': service_info.get('environment', {}),
        'networks': service_info.get('networks', []),
        'depends_on': service_info.get('depends_on', []),
        'deploy': service_info.get('deploy', {}),
        'restart': service_info.get('restart', 'no')
    }
    return {service_name: {key: value for key, value in config.items() if value is not None}}

with open('../projects/default/example-test.yaml', 'r') as file:
    config = yaml.safe_load(file)

compose_data = {
    'version': '3',
    'services': {}
}

for service_name, service_info in config.get('services', {}).items():
    if service_name == 'microservice':
        compose_data['services'].update(map_service_config(service_name, service_info))

volumes = config.get('volumes', [])
networks = config.get('networks', [])

if volumes:
    compose_data['volumes'] = {vol: {} for vol in volumes}

if networks:
    compose_data['networks'] = {net: {} for net in networks}

with open('../projects/default/docker-compose.yml', 'w') as file:
    yaml.dump(compose_data, file, default_flow_style=False)
