import yaml
import os
import argparse

def render_template(template_content, context):
    for key, value in context.items():
        placeholder = f"{{{{ares_config.{key}}}}}"
        template_content = template_content.replace(placeholder, str(value))
    return template_content

def main(yaml_file, base_directory):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    
    project_name = config.get('project', 'default')

    test_file_base = os.path.splitext(os.path.basename(yaml_file))[0]

    output_directory = os.path.join(base_directory, 'generated_tests', test_file_base)
    os.makedirs(output_directory, exist_ok=True)
    
    for test_name, test_params in config.get('tests', {}).items():
        template_file_path = test_params.get('path')
        
        if not template_file_path:
            print(f"No path defined for test {test_name}, skipping...")
            continue

        if not os.path.exists(template_file_path):
            print(f"Template file {template_file_path} not found, skipping...")
            continue
        
        with open(template_file_path, 'r') as template_file:
            template_content = template_file.read()
        
        rendered_content = render_template(template_content, test_params)
        
        output_file_name = os.path.basename(template_file_path).replace('.js', '.generated.js')
        output_file_path = os.path.join(output_directory, output_file_name)
        
        with open(output_file_path, 'w') as output_file:
            output_file.write(rendered_content)
        
        print(f"Generated test file: {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a test file from a YAML configuration.")
    parser.add_argument('yaml_file', type=str, help="Path to the input YAML configuration file.")
    parser.add_argument("base_directory", type=str, help="Base path where the output test file will be saved.")

    args = parser.parse_args()

    main(args.yaml_file, args.base_directory)
