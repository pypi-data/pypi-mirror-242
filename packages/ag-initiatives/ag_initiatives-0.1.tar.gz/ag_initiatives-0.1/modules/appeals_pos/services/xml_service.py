from copy import deepcopy

from lxml import etree


class XMLService:
    @staticmethod
    def insert_xml_str_in_etree(root: etree.ElementBase, xml_str: str, block_name: str) -> None:
        block = root.xpath(f'//*[local-name()="{block_name}"]')
        if block:
            block[0].append(etree.fromstring(xml_str))

    @staticmethod
    def insert_el_in_etree(root: etree.ElementBase, element: etree.ElementBase, block_name: str) -> None:
        block = root.xpath(f'//*[local-name()="{block_name}"]')
        if block:
            block[0].append(element)

    @staticmethod
    def insert_str_in_etree(root: etree.ElementBase, insert_str: str, block_name: str) -> None:
        block = root.xpath(f'//*[local-name()="{block_name}"]')
        if block:
            block[0].text = str(insert_str)

    @classmethod
    def copy_element(cls, element):
        new_element = deepcopy(element)  # Создаем копию элемента
        for child in element:  # Рекурсивно копируем вложенные элементы
            new_child = cls.copy_element(child)
            new_element.append(new_child)
        return new_element

    @classmethod
    def insert_list_in_etree(cls, root: etree.ElementBase, insert_list: list) -> None:
        is_first = True
        parent = root.getparent()
        for value in insert_list:
            if not is_first:
                root = deepcopy(root)
                parent.insert(0, root)
            else:
                is_first = False

            if type(value) == dict:
                cls.insert_dict_in_etree(root, value)
            else:
                root.text = str(value)

    @classmethod
    def insert_dict_in_etree(cls, root: etree.ElementBase, insert_dict: dict) -> None:
        for k, v in insert_dict.items():
            if v is None:
                root.remove(root.xpath(f'//*[local-name()="{k}"]')[0])
                continue
            elif v == []:
                root.getparent().remove(root)
                continue

            if type(v) in [str, int, float]:
                XMLService.insert_str_in_etree(root, v, k)
            elif type(v) is dict:
                cls.insert_dict_in_etree(root.xpath(f'//*[local-name()="{k}"]')[0], v)
            elif type(v) in [list, tuple]:
                cls.insert_list_in_etree(root.xpath(f'//*[local-name()="{k}"]')[0], v)
            else:
                raise Exception('parse error', type(v), k, v)

    @classmethod
    def xml_to_dict(cls, root: etree.ElementBase) -> dict:
        result = {}
        for child in root:
            child_data = cls.xml_to_dict(child)
            if not child_data:
                continue
            tag_name = etree.QName(child).localname
            if tag_name in result:
                if type(result[tag_name]) is list:
                    result[tag_name].append(child_data)
                else:
                    result[tag_name] = [result[tag_name], child_data]
            else:
                result[tag_name] = child_data
        if not result:
            return root.text
        return result
