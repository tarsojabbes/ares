import yaml
import argparse
import os

def load_yaml(yaml_file):
    """Load YAML file and return data."""
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def replace_placeholders(template_content, replacements):
    """Replace placeholders in the template with provided replacements."""
    for placeholder, replacement in replacements.items():
        # Make sure placeholders match the format in the template
        formatted_placeholder = f"{{{{ {placeholder} }}}}"
        if formatted_placeholder in template_content:
            template_content = template_content.replace(formatted_placeholder, replacement)
        else:
            print(f"Placeholder {formatted_placeholder} not found in the template.")
    return template_content

def main(yaml_file, template_file):
    # Load the YAML file
    config = load_yaml(yaml_file)
    
    # Extract the container_name and project_name
    container_name = config.get('services', {}).get('microservice', {}).get('container_name', 'default_container_name')
    project_name = config.get('project', 'default')

    # Load the template file
    with open(template_file, 'r') as file:
        template_content = file.read()

    # Replace placeholders in the template
    replacements = {
        'ares_config.project.microservice_name': f'{project_name}.{container_name}'
    }
    updated_content = replace_placeholders(template_content, replacements)
    
    output_file = f'./infra/grafana/dashboards/{project_name}.{container_name}.json'
    # Write the updated content to the output file
    with open(output_file, 'w') as file:
        file.write(updated_content)
    
    print(f"Updated dashboard saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace placeholders in a Grafana dashboard template with values from a YAML configuration.")
    parser.add_argument('yaml_file', type=str, help="Path to the YAML configuration file.")
    parser.add_argument('template_file', type=str, help="Path to the Grafana dashboard template file.")

    args = parser.parse_args()
    main(args.yaml_file, args.template_file)
