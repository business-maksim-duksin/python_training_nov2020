import json
import xml.etree.ElementTree as ET
from typing import Dict
# from logging_config import log


def save_as_json(d: Dict, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(d, f, indent=4)


def save_as_xml(d: Dict, path: str) -> None:
    root_key = list(d.keys())[0]
    root = ET.Element(str(root_key))

    def get_leafs(stuff):
        """ Recursively walk data branches forming a XML ElementTree. """
        leafs = []
        if isinstance(stuff, dict):
            for key, value in stuff.items():
                elem = ET.Element(str(key))
                if isinstance(value, dict):
                    elem.extend(get_leafs(value))
                elif isinstance(value, list):
                    elem.extend(get_leafs(value))
                else:
                    elem.text = str(value)
                leafs.append(elem)
        elif isinstance(stuff, list):
            for value in stuff:
                elem = ET.Element("obj")
                if isinstance(value, dict):
                    elem.extend(get_leafs(value))
                elif isinstance(value, list):
                    for node in value:
                        elem.extend(get_leafs(node))
                else:
                    elem.text = str(value)
                leafs.append(elem)
        return leafs

    for item in d[root_key]:
        root.extend(get_leafs(item))

    tree = ET.ElementTree(root)
    with open(path, "w") as f:
        tree.write(f, encoding="unicode")
