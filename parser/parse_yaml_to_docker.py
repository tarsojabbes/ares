import yaml
import argparse

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

def main(input_file, output_file):
    with open(input_file, 'r') as file:
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

    with open(output_file, 'w') as file:
        yaml.dump(compose_data, file, default_flow_style=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Docker Compose file from a YAML configuration.")
    parser.add_argument('input_file', type=str, help="Path to the input YAML configuration file.")
    parser.add_argument('output_file', type=str, help="Path where the output docker-compose.yml will be saved.")

    args = parser.parse_args()
    main(args.input_file, args.output_file)
