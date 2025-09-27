import json


def f_measure(json_path, json_path3, json_path4, owl_path):
    """
    Obtaining an experimental evaluation of the ontology
        :param json_path: name of source json file
        :param json_path3: name of source with typed columns
        :param json_path4: name of source with entity column
        :param owl_path: name of source ontology
        :return: precision, recall, f1, for ontology schema and precision, recall, f1 for named individuals
    """
    with open(json_path3, 'r', encoding='utf-8') as f:
        text = json.load(f)
        potential_class = 0
        potential_datatype_prop = 0
        for str_json in text:
            for obj_json in str_json:
                if text[0][obj_json] == "CATEGORICAL":
                    potential_class = potential_class + 1
                if text[0][obj_json] == "LITERAL":
                    potential_datatype_prop = potential_datatype_prop + 1
        potential_obj_prop = potential_class - 1
        potential_element = potential_class + potential_obj_prop + potential_datatype_prop
    with open(json_path4, 'r', encoding='utf-8') as f:
        text = json.load(f)
        i = -1
        object_prop_item = 0
        class_item = 0
        datatype_prop_item = 0
        list_item = []
        subj_item = ""
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                if text[i][obj_json] == "CATEGORICAL":
                    object_prop_item = object_prop_item + 1
                    class_item = class_item + 1
                    list_item.append(obj_json.capitalize())
                if text[i][obj_json] == "SUBJECT":
                    class_item = class_item + 1
                    subj_item = obj_json
                    list_item.append(obj_json.capitalize())
                if text[i][obj_json] == "LITERAL":
                    datatype_prop_item = datatype_prop_item + 1
    count2 = 0
    correct_item = 0
    with open(owl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find("<owl:Class") != -1:
                correct_item = correct_item + 1
            for item in list_item:
                if line.find('<rdfs:domain rdf:resource="#' + item.title().replace(" ", "")) != -1 and \
                        (item.title().replace(" ", "") == subj_item.title().replace(" ", "")):
                    correct_item = correct_item + 1
    with open(owl_path, 'r', encoding='utf-8') as f:
        count_obj = 0
        count_named_individual = 0
        correct_individual = 0
        flag_object = 0
        for line in f:
            if line.find("<owl:NamedIndividual") != -1:
                flag_object = 1
                count_named_individual = count_named_individual + 1
            if flag_object == 1:
                count2 = count2 + 1
            if line.find("</owl:NamedIndividual") != -1:
                count2 = count2 - 2
                if (count2 == 1) or (count2 == (potential_obj_prop + potential_datatype_prop + 1)):
                    correct_individual = correct_individual + 1
                count_obj = count_obj + 1
                count2 = 0
                flag_object = 0
    precision = correct_item / (object_prop_item + datatype_prop_item + class_item)
    recall = correct_item / potential_element
    f1 = (2 * precision * recall) / (precision + recall)

    print(owl_path)
    print()
    print("Evaluation for ontology schema:")
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1)
    print()

    with open(json_path4, 'r', encoding='utf-8') as f, open(json_path, 'r', encoding='utf-8') as fs:
        text = json.load(f)
        text1 = json.load(fs)
        i = 0
        categorical_individual = 0
        subject_individual = 0
        entity_name = set()
        entity_name1 = set()
        for str_json in text1:
            for obj_json in str_json:
                length_set = len(entity_name)
                if text[0][obj_json] == "CATEGORICAL":
                    entity_name.add(text1[i][obj_json])
                    if length_set == len(entity_name):
                        continue
                    else:
                        categorical_individual = categorical_individual + 1
                if text[0][obj_json] == "SUBJECT":
                    subject_individual = subject_individual + 1
                    entity_name1.add(text1[i][obj_json])

            i = i + 1
    count_individual1 = (subject_individual + categorical_individual)
    count_individual2 = len(entity_name) + len(entity_name1)
    precision1 = correct_individual / count_named_individual
    recall1 = correct_individual / count_individual1
    recall2 = correct_individual / count_individual2
    if recall1 > 1:
        recall1 = 1
    if precision1 + recall1 != 0:
        f11 = (2 * precision1 * recall1) / (precision1 + recall1)
    else:
        f11 = 0
    print("Evaluation for named individuals:")
    print("Precision: ", precision1)
    print("Recall: ", recall1)
    print("F1: ", f11)
    print()
    return precision, recall, f1, precision1, recall1, f11
