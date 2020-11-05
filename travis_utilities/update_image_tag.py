import yaml
import sys

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit(status='Missing argyments. Call as "update_image_tag.py <new_tag> <filename>')

    tag = sys.argv[1]
    filename = sys.argv[2]
    with open(filename, 'r') as f:
        data = yaml.full_load(f)

    data['image']['tag'] = tag
    with open(filename, 'w') as f:
        yaml.dump(data, f)
