import re
import json
import ftfy


def create_json(json_path, json_path1):
    """
    Defining Literal Values in Cells
    :param json_path: name of source json file
    :param json_path1: name of the file where the literal values in the cells will be defined
    :return: file where literal values in cells will be defined, dictionary with defined values
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = -1
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                text[i][obj_json] = ftfy.fix_text(text[i][obj_json])
                text_string = text[i][obj_json]
                if text[i][obj_json] == 'NONE':
                    text[i][obj_json] = 'SYMBOL'
                result = re.search('[A-Za-z0-9А-Яа-я]', text_string)
                if result:
                    result = re.search(r'^[-+]?[0-9]+$', text_string)
                    if result:
                        text[i][obj_json] = 'INTEGER'
                    result = re.search('[0-2][0-9][0-9][0-9]', text_string)
                    if result:
                        text[i][obj_json] = 'DATE'
                    result = re.search(
                        '(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d|(19|20)\d\d-((0[1-9]|1[012])-(0[1-9]|[12]\d)|(0[13-9]|1[012])-30|(0[13578]|1[02])-31)',
                        text_string)
                    if result:
                        text[i][obj_json] = 'DATE'
                    result = re.search(
                        '^(0?[1-9]|1[0-2]):[0-5][0-9]$|((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))|^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$|^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$|(?:[01]\d|2[0-3]):(?:[0-5]\d):(?:[0-5]\d)',
                        text_string)
                    if result:
                        text[i][obj_json] = 'TIME'
                    result = re.search('^"true|false|True|False|TRUE|FALSE"&', text_string)
                    if result:
                        text[i][obj_json] = 'LOGIC'
                    result = re.search('^\d{6}$', text_string)
                    if result:
                        text[i][obj_json] = 'MAIL'
                    result = re.search('^[-+]?([1-9]\d*|0)\\$|\\£|\\€', text_string)
                    if result:
                        text[i][obj_json] = 'CURRENCY'
                    result = re.search('^\d{5}(?:[-\s]\d{4})?$', text_string)
                    if result:
                        text[i][obj_json] = 'MAIL'
                    result = re.search('^[0-9]{4}-[0-9]{3}[0-9xX]$', text_string)
                    if result:
                        text[i][obj_json] = 'ISSN'
                    result = re.search('^(?:ISBN(?:: ?| ))?((?:97[89])?\d{9}[\dx])+$', text_string)
                    if result:
                        text[i][obj_json] = 'ISBN'
                    result = re.search('((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)', text_string)
                    if result:
                        text[i][obj_json] = 'IPv4'
                    result = re.search('((\\b100)|(\\b[0-9]{1,2}\\.?[0-9]?))(?=%| *percent)', text_string)
                    if result:
                        text[i][obj_json] = 'PERCENT'
                    result = re.search(r'^([456][0-9]{3})-?([0-9]{4})-?([0-9]{4})-?([0-9]{4})$', text_string)
                    if result:
                        text[i][obj_json] = 'CARD'
                    result = re.search(r'#[0-9A-Fa-f]{6}', text_string)
                    if result:
                        text[i][obj_json] = 'COLOR'
                    result = re.search(r'[\w.-]+@[\w.-]+\.?[\w]+?', text_string)
                    if result:
                        text[i][obj_json] = 'EMAIL'
                    result = re.search("[+-]?\d+\.\d+", text_string)
                    if result:
                        text[i][obj_json] = 'FLOAT'
                if (text[i][obj_json] != 'INTEGER' and text[i][obj_json] != 'SYMBOL' and text[i][obj_json] != 'DATE' and
                        text[i][obj_json] != 'TIME' and text[i][obj_json] != 'LOGIC' and text[i][obj_json] != 'MAIL' and
                        text[i][obj_json] != 'CURRENCY' and text[i][obj_json] != 'ISSN' and text[i][
                            obj_json] != 'ISBN' and
                        text[i][obj_json] != 'IPv4' and text[i][obj_json] != 'IPv6' and text[i][
                            obj_json] != 'PERCENT' and
                        text[i][obj_json] != 'CARD' and text[i][obj_json] != 'COLOR' and text[i][
                            obj_json] != 'EMAIL' and
                        text[i][obj_json] != 'FLOAT'):
                    text[i][obj_json] = 'NONE'
        return json_path1, text
