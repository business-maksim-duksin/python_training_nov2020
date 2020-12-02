import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Union


class SaverToFile:
    """ Interface class for filesaving """

    @staticmethod
    def save_to_file(content: Union[Dict, List], path: str):
        raise NotImplementedError


class SaverToJSON(SaverToFile):
    """ Class for saving as JSON """

    @staticmethod
    def save_to_file(content: Union[Dict, List], path: str):
        with open(path, 'w') as f:
            json.dump(content, f, indent=4, default=str)


class SaverToXML(SaverToFile):
    """ Class for saving as XML """

    @staticmethod
    def save_to_file(content: Union[Dict, List], path: str) -> None:
        root_key = "root"
        root = ET.Element(str(root_key))
        content = {root_key: content}

        def _get_leafs(stuff):
            """ Recursively walk data branches forming a XML ElementTree. """
            leafs = []
            if isinstance(stuff, dict):
                for key, value in stuff.items():
                    elem = ET.Element(str(key))
                    if isinstance(value, dict):
                        elem.extend(_get_leafs(value))
                    elif isinstance(value, list):
                        elem.extend(_get_leafs(value))
                    else:
                        elem.text = str(value)
                    leafs.append(elem)
            elif isinstance(stuff, list):
                for value in stuff:
                    elem = ET.Element("obj")
                    if isinstance(value, dict):
                        elem.extend(_get_leafs(value))
                    elif isinstance(value, list):
                        for node in value:
                            elem.extend(_get_leafs(node))
                    else:
                        elem.text = str(value)
                    leafs.append(elem)
            return leafs

        for item in content.values():
            root.extend(_get_leafs(item))

        tree = ET.ElementTree(root)
        with open(path, "w") as f:
            tree.write(f, encoding="unicode")
