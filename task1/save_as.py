import json
import xml.etree.ElementTree as ET
from typing import Dict, List


def save_as_json(d: Dict, path: str) -> None:
    with open(path, 'w') as f:
        json.dump(d, f, indent=4)


def save_as_xml(d: Dict, path: str) -> None:
    # root = ET.Element("Catalog")
    root_key = list(d.keys())[0]
    root = ET.Element(str(root_key))

    def get_leafs(stuff):
        leafs = []
        if isinstance(stuff, dict):
            for key, value in stuff.items():
                elem = ET.Element(str(key))
                if isinstance(value, dict):
                    # for node in value.values():
                    #     elem.append(get_leafs(node))
                    elem.extend(get_leafs(value))
                elif isinstance(value, list):
                    # for node in value:
                    #     elem.append(get_leafs(node))
                    elem.extend(get_leafs(value))
                else:
                    elem.text = str(value)
                leafs.append(elem)
        elif isinstance(stuff, list):
            for value in stuff:
                elem = ET.Element("obj")
                if isinstance(value, dict):
                    # for node in value.values():
                    #     elem.append(get_leafs(node))
                    elem.extend(get_leafs(value))
                elif isinstance(value, list):
                    for node in value:
                        elem.extend(get_leafs(node))
                else:
                    elem.text = str(value)
                leafs.append(elem)

        return leafs


    # for key, value in d[root_key].items():
    #     elem = ET.Element(str(key))
    #     if isinstance(value, dict):
    #         for leaf in get_leafs(list(d.values())):
    #             elem.append(leaf)
    #     elif isinstance(value, list):
    #         for leaf in get_leafs(value):
    #             elem.append(leaf)
    #     else:
    #         elem.text = str(value)
    #     root.append(elem)

    for item in d[root_key]:
        root.extend(get_leafs(item))

    tree = ET.ElementTree(root)
    with open(path, "w") as f:
        tree.write(f, encoding="unicode")

    #         #
    # root = ET.Element("Catalog")
    # m1 = ET.Element("mobile")
    # root.append(m1)
    #
    # b1 = ET.SubElement(m1, "brand")
    # b1.text = "Redmi"
    # b2 = ET.SubElement(m1, "price")
    # b2.text = "6999"
    #
    # m2 = ET.Element("mobile")
    # root.append(m2)
    #
    # c1 = ET.SubElement(m2, "brand")
    # c1.text = "Samsung"
    # c2 = ET.SubElement(m2, "price")
    # c2.text = "9999"
    #
    # m3 = ET.Element("mobile")
    # root.append(m3)
    #
    # d1 = ET.SubElement(m3, "brand")
    # d1.text = "RealMe"
    # d2 = ET.SubElement(m3, "price")
    # d2.text = "11999"
    #
    # tree = ET.ElementTree(root)
    #
    # with open(path, "w") as f:
    #     tree.write(f, encoding="unicode")

    # def get_leafs(dd):
    #     leafs = []
    #     for key, value in dd.items():
    #         elem = ET.Element(str(key))
    #         if isinstance(value, dict):
    #             for leaf in get_leafs(list(d.values())[0]):
    #                 elem.append(leaf)
    #         else:
    #             root.text = str(list(d.values())[0])
    #         subnodes.append(elem)
    #     return subnodes
    #
    # root = ET.Element(str(list(d.keys())[0]))
    # if isinstance(list(d.values())[0], dict):
    #     for leaf in get_leafs(list(d.values())[0]):
    #         root.append(leaf)
    # else:
    #     root.text = str(list(d.values())[0])
    #
    # with open(path, "w") as f:
    #     tree.write(f, encoding="unicode")

