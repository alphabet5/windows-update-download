

def p_xml(element):
    if len(element) > 0:
        return_dict = dict()
        for x in element:
            if x.tag in return_dict:
                if type(return_dict[x.tag]) != list:
                    return_dict[x.tag] = [return_dict[x.tag]]
                return_dict[x.tag].append(p_xml(x))
            else:
                return_dict[x.tag] = p_xml(x)
        return return_dict
    else:
        return element.text


def parse_arguments(arguments_yaml_file='arguments.yaml'):
    import yaml
    import argparse
    from pydoc import locate
    with open(arguments_yaml_file, 'r') as y:
        data = yaml.load(y, Loader=yaml.FullLoader)
        parser = argparse.ArgumentParser()
        for argument, parameters in data.items():
            if 'type' in parameters.keys():
                parameters['type'] = locate(parameters['type'])
            if 'required' in parameters.keys():
                if type(parameters['required']) == str:
                    parameters['required'] = exec(parameters['required'])
            parser.add_argument('--' + argument, **parameters)
        return parser.parse_args()


if __name__ == '__main__':
    import xml.etree.ElementTree as ET
    import requests
    import os
    args = vars(parse_arguments())
    element_tree = ET.fromstring(open(args['bpurl'], 'r').read())
    elements = p_xml(element_tree)
    for file in elements['Grid']:
        print("Downloading: " + file['columnUrl'])
        r = requests.get(file['columnUrl'], allow_redirects=True)
        filename = r.headers.get('content-disposition')
        if filename is None:
            filename = file['columnUrl'].rsplit('/')[-1]
        dest_file = os.path.join(args['directory'], filename)
        open(dest_file, 'wb').write(r.content)