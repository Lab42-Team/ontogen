from ontogen.xmler import dict2xml
import json

dict1 = {"DATE": "http://www.w3.org/2001/XMLSchema#date",
         "TIME": "http://www.w3.org/2001/XMLSchema#time",
         "INTEGER": "http://www.w3.org/2001/XMLSchema#integer",
         "LOGIC": "http://www.w3.org/2001/XMLSchema#boolean",
         "MAIL": "http://www.w3.org/2001/XMLSchema#unsignedLong",
         "CURRENCY": "http://www.w3.org/2001/XMLSchema#nonNegativeInteger",
         "ISSN": "http://www.w3.org/2001/XMLSchema#token",
         "ISBN": "http://www.w3.org/2001/XMLSchema#token",
         "IPv6": "http://www.w3.org/2001/XMLSchema#token",
         "IPv4": "http://www.w3.org/2001/XMLSchema#token",
         "PERCENT": "http://www.w3.org/2001/XMLSchema#positiveInteger",
         "CARD": "http://www.w3.org/2001/XMLSchema#token",
         "COLOR": "http://www.w3.org/2001/XMLSchema#positiveInteger",
         "EMAIL": "http://www.w3.org/2001/XMLSchema#string",
         "FLOAT": "http://www.w3.org/2001/XMLSchema#float",
         "SYMBOL": "http://www.w3.org/2001/XMLSchema#token",
         "NONE": "http://www.w3.org/2001/XMLSchema#string"}


def open_file(json_file):
    """
        Opening .json file and extracting content
        :param json_file: .json file name
        :return: list with .json file content
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        text = json.load(f)
    return text


def create_class(entity_name, i):
    """
        Create a class
        :param entity_name: class name
        :param i: class number
        :return: dictionary with class
    """
    entity_name = entity_name.replace("_", "")
    ont_class = [{"Class" + str(i): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "Class",
        "@attrs": {
            "rdf:about": '#' + entity_name.replace(" ", "")
        }
    }}]
    return ont_class


def create_object_property(entity_name, sub_name, j):
    """
        Creating an Entity Object Property
        :param entity_name: object property name
        :param sub_name: domain name
        :param j: serial number of the object
        :return: dictionary with entity object property
    """
    entity_name = entity_name.replace("_", "")
    sub_name = sub_name.replace("_", "")
    ont_obj_prop = [{"ObjectProperty" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "ObjectProperty",
        "@attrs": {
            "rdf:about": '#' + "has" + entity_name.replace(" ", "")
        },
        "domain": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + sub_name.replace(" ", "")
            }
        },
        "range": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + entity_name.replace(" ", "")
            }
        }
    }}]
    return ont_obj_prop


def create_sub_atr(sub_name, subject_value, dictionary3):
    """
    Create a tag with the name of an individual
    :param sub_name: the name of the class to which the individual belongs
    :param subject_value: tag attribute name
    :param dictionary3: vocabulary in which the individual is formed
    :return: dictionary with the name of the individual
    """
    sub_name = sub_name.replace("_", "")
    subject_value = subject_value.replace("_", "")
    dictionary5 = {
        "@ns": "rdf",
        "@attrs": {
            "rdf:resource": '#' + sub_name.replace(" ", "")
        }
    }
    dictionary3.update({"@ns": "owl",
                        "@name": "NamedIndividual",
                        "@attrs": {
                            "rdf:about": '#' + subject_value.replace(" ", "")
                        }, "type": dictionary5})
    return dictionary3


def create_categorical_obj_atr(categorical_obj_name, categorical_obj_value, dictionary3):
    """
        Creating a Dictionary with the Object Properties of an Individual
        :param categorical_obj_name: object property name
        :param categorical_obj_value: object property value
        :param dictionary3: vocabulary in which the individual is formed
        :return: dictionary with object properties of an individual
    """
    categorical_obj_name = categorical_obj_name.replace("_", "")
    categorical_obj_value = categorical_obj_value.replace("_", "")
    dictionary5 = {
        "@attrs": {
            "rdf:resource": '#' + categorical_obj_value.replace(" ", "")
        }
    }
    dictionary3.update({"has" + categorical_obj_name.replace(" ", ""): dictionary5})
    return dictionary3


def create_literal_obj_atr(literal_obj_name, literal_obj_value, dictionary3):
    """
        Creating a Dictionary with an Individual Data Type
        :param literal_obj_name: the name of the data type of the individual
        :param literal_obj_value: literal value of an individual
        :param dictionary3: vocabulary in which the individual is formed
        :return: dictionary with literal properties of an individual
    """
    literal_obj_name = literal_obj_name.replace("_", "")
    literal_obj_value = literal_obj_value.replace("_", "")
    dictionary5 = {
        "@attrs": {
            "rdf:resource": literal_obj_value.replace(" ", "")
        }
    }
    dictionary3.update({"has" + literal_obj_name.replace(" ", ""): dictionary5})
    return dictionary3


def create_datatype_property(obj_json, subj_name, type_name, j):
    """
        Converting all L-column headers of a table to value properties
        :param obj_json: L-column header name
        :param subj_name: domain name
        :param type_name: data type name
        :param j: serial number of the object
        :return: dictionary with literal values
    """
    obj_json = obj_json.replace("_", "")
    subj_name = subj_name.replace("_", "")
    ont_data_prop = [{"DatatypeProperty" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@name": "DatatypeProperty",
        "@attrs": {
            "rdf:about": '#' + "has" + obj_json.replace(" ", "")
        },
        "domain": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": '#' + subj_name.replace(" ", "")
            }
        },
        "range": {
            "@ns": "rdfs",
            "@attrs": {
                "rdf:resource": type_name
            }
        }
    }}]
    return ont_data_prop


def create_name_individual_categorical(obj_json, obj_name, j):
    """
    Generation of the individual
    :param obj_json: the type of the individual
    :param obj_name: name of the individual
    :param j: index number of the individual
    :return: dictionary with individual
    """
    obj_json = obj_json.replace("_", "")
    obj_name = obj_name.replace("_", "")
    ont_name_individual_categorical = [
        {"NamedIndividual1" + str(j): {  # The root tag. Will not necessarily be root. (see #customRoot)
            "@ns": "owl",
            "@name": "NamedIndividual",
            "@attrs": {
                "rdf:about": '#' + obj_name.replace(" ", "")
            },
            "type": {
                "@ns": "rdf",
                "@attrs": {
                    "rdf:resource": '#' + obj_json.replace(" ", "")
                }
            }
        }}]
    return ont_name_individual_categorical


def create_ontology(json_path, json_path1, json_path4, dictionary3):
    """
    Creation of an ontology
    :param json_path: name of source json file
    :param json_path1: name of the file that defines the literal values in the cells
    :param json_path4: name of file with score for each column
    :param dictionary3: dictionary in which the individual will be formed
    :return: line with ontology
    """
    json_file = json_path
    ont_namespace = {"@ns": "rdf",  # The namespace for the RootTag. The RootTag will appear as <rdf:RootTag ...>
                     "@attrs": {  # @attrs takes a dictionary. each key-value pair will become an attribute
                         "xmlns:rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                         "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
                         "xmlns:rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                         "xmlns:owl": "http://www.w3.org/2002/07/owl#",
                         "xmlns:base": "http://test.org/onto.owl",
                         "xmlns": "http://test.org/onto.owl#",
                     }}
    ont_ontology = {"Ontology": {  # The root tag. Will not necessarily be root. (see #customRoot)
        "@ns": "owl",
        "@attrs": {
            "rdf:about": "http://test.org/onto.owl"
        }
    }}
    ont_class = []
    text = open_file(json_file)
    text1 = open_file(json_path4)
    text2 = open_file(json_path1)
    i = -1
    j = 0
    entity_name = set()
    subject_name = ""
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            if text1[0][obj_json] == "SUBJECT":
                subject_name = obj_json
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if (text1[0][obj_json] == "SUBJECT") or (text1[0][obj_json] == "CATEGORICAL"):
                entity_name.add((obj_json.replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    lst = create_class(obj_json.title(), j)
                    ont_class.extend(lst)
    entity_name = set()
    i = -1
    j = 0
    ont_obj_prop = []
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "SUBJECT":
                subject_name = obj_json
            if text1[0][obj_json] == "CATEGORICAL":
                entity_name.add((obj_json.replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    lst = create_object_property(obj_json.title(), subject_name.title(), j)
                    ont_obj_prop.extend(lst)
    entity_name = set()
    i = -1
    j = 0
    ont_data_prop = []
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "LITERAL":
                entity_name.add((obj_json.replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    type_name = text2[len(text2) - 1][obj_json]
                    for key, value in dict1.items():
                        if type_name == key:
                            type_name = dict1[key]
                    lst = create_datatype_property(obj_json.title(), subject_name.title(), type_name, j)
                    ont_data_prop.extend(lst)
    i = -1
    entity_name = set()
    k = 1
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            entity_name.add((text[i][obj_json].replace(" ", "")).replace("_", ""))
            if (length_set == len(entity_name)) and (
                    text1[0][obj_json] == "CATEGORICAL" or text1[0][obj_json] == "SUBJECT"):
                text[i][obj_json] = text[i][obj_json] + str(k)
    entity_name = set()
    i = -1
    j = 0
    ont_name_individual_categorical = []
    for str_json in text:
        i = i + 1
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "CATEGORICAL":
                entity_name.add((text[i][obj_json].replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    continue
                else:
                    j = j + 1
                    obj_name = text[i][obj_json]
                    lst = create_name_individual_categorical(obj_json.title(), obj_name, j)
                    ont_name_individual_categorical.extend(lst)
    i = -1
    entity_name = set()
    j = 0
    dictionary2 = {}
    k = 0
    for str_json in text:
        i = i + 1
        length_set = len(entity_name)
        entity_name.add((text[i][subject_name].replace(" ", "")).replace("_", ""))
        if length_set == len(entity_name):
            continue
        else:
            subject_value = text[i][subject_name]
            dictionary3 = create_sub_atr(subject_name.title(), subject_value, dictionary3)
        for obj_json in str_json:
            length_set = len(entity_name)
            if text1[0][obj_json] == "SUBJECT":
                entity_name.add((text[i][obj_json].replace(" ", "")).replace("_", ""))
                if length_set == len(entity_name):
                    k = k + 1
                subject_name = obj_json
                subject_value = text[i][obj_json]
                dictionary3 = create_sub_atr(subject_name.title(), subject_value, dictionary3)
            if text1[0][obj_json] == "CATEGORICAL":
                categorical_obj_name = obj_json
                categorical_obj_value = text[i][obj_json]
                dictionary3 = create_categorical_obj_atr(categorical_obj_name.title(),
                                                         categorical_obj_value, dictionary3)
            if text1[0][obj_json] == "LITERAL":
                literal_obj_name = obj_json
                literal_obj_value = text[i][obj_json]
                dictionary3 = create_literal_obj_atr(literal_obj_name.title(), literal_obj_value, dictionary3)
        dictionary2.update({"NamedIndividual" + str(j): dictionary3})
        j = j + 1
        dictionary3 = {}
    ont_name_individual_subject = [dictionary2]

    ns_no = {}
    for key in ont_namespace.keys():
        ns_no.update({key: ont_namespace[key]})
    for key in ont_ontology.keys():
        ns_no.update({key: ont_ontology[key]})
    for str_json in ont_class:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_obj_prop:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_data_prop:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_name_individual_categorical:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    for str_json in ont_name_individual_subject:
        for key in str_json.keys():
            ns_no.update({key: str_json[key]})
    dictionary = {"RDF": ns_no}
    new_string = dict2xml(dictionary, pretty=True)
    return new_string
