import argparse
import os
import subprocess
import yaml
from deepdiff import DeepDiff

def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def compare_configs(local_config, git_config):
    return DeepDiff(local_config, git_config, ignore_order=True).pretty()

def main(local_config_path):
    git_config_path = local_config_path.replace('/parsed_data/', '/parsed_data_git/')

    # Create directory if not exists
    os.makedirs(os.path.dirname(git_config_path), exist_ok=True)

    # Fetch the git version of the config file
    subprocess.run(['git', 'checkout', 'HEAD', '--', git_config_path])

    local_config = load_yaml_file(local_config_path)
    git_config = load_yaml_file(git_config_path)

    diff = compare_configs(local_config, git_config)

    diff_file = f"{local_config_path}.diff"
    with open(diff_file, 'w') as file:
        file.write(diff)

    if diff:
        print(f"Differences found and saved to {diff_file}")
    else:
        print("No differences found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare local and git configurations")
    parser.add_argument("local_config_path", help="Path to the local configuration file")
    args = parser.parse_args()

    main(args.local_config_path)

