import fileinput
import glob
import json
import os


def unifier(path):
    """
    Creation of a single ontology based on the created ontologies from each file
    :param path: Path to files where ontologies are stored
    :return: Unified ontology file
    """
    list_files = []
    for dirs, folder, files in os.walk(path):
        for element in glob.glob(dirs + '\*.owl'):
            list_files.append(element)
    new_file = 'TotalOntology.owl'
    class_set = set()
    flag_object = 0
    key = ""
    named_individual_dictionary = dict()
    flag_datatype = 0
    flag_individual = 0
    object_dictionary = dict()
    datatype_dictionary = dict()
    text_object = ""
    text_datatype = ""
    if list_files:
        with fileinput.FileInput(files=list_files, openhook=fileinput.hook_encoded("utf-8")) as fr:
            for line in fr:
                if line.find("<owl:Class") != -1:
                    class_set.add(line)

                if line.find("<owl:ObjectProperty") != -1:
                    key = line
                    flag_object = 1
                    object_dictionary.setdefault(line, [])
                if flag_object == 1:
                    if line.find("<owl:ObjectProperty") == -1 and line.find("</owl:ObjectProperty") == -1:
                        text_object = text_object + line
                if line.find("</owl:ObjectProperty") != -1:
                    object_dictionary[key].append(text_object)
                    object_dictionary[key] = list(set(object_dictionary[key]))
                    flag_object = 0
                    text_object = ""

                if line.find("<owl:DatatypeProperty") != -1:
                    key = line
                    flag_datatype = 1
                    datatype_dictionary.setdefault(line, [])
                if flag_datatype == 1:
                    if line.find("<owl:DatatypeProperty") == -1 and line.find("</owl:DatatypeProperty") == -1:
                        text_datatype = text_datatype + line
                if line.find("</owl:DatatypeProperty") != -1:
                    datatype_dictionary[key].append(text_datatype)
                    datatype_dictionary[key] = list(set(datatype_dictionary[key]))
                    flag_datatype = 0
                    text_datatype = ""

                if line.find("<owl:NamedIndividual") != -1:
                    flag_individual = 1
                    key = line
                    named_individual_dictionary.setdefault(line, [])
                if flag_individual == 1:
                    if line.find("<owl:NamedIndividual") == -1:
                        named_individual_dictionary[key].append(line)
                if line.find("</owl:NamedIndividual") != -1:
                    named_individual_dictionary[key].pop()
                    named_individual_dictionary[key] = list(set(named_individual_dictionary[key]))
                    flag_individual = 0
    with open(new_file, 'w', encoding='utf-8') as fw:
        fw.write(
            '<?xml version="1.0" ?>' + "\n" +
            '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xsd="http://www.w3.org/2001'
            '/XMLSchema" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" xmlns:owl="http://www.w3.org/2002/07/owl#" '
            'xmlns:base="http://test.org/onto.owl" xmlns="http://test.org/onto.owl#">' + "\n"
            + "\t" + '<owl:Ontology rdf:about="http://test.org/onto.owl"/>' + "\n")
        for element in class_set:
            fw.write(element)
        for key, elements in object_dictionary.items():
            count = 0
            if len(object_dictionary[key]) > 1:
                for element in elements:
                    if count == 0:
                        fw.write(key)
                        fw.write(element)
                        fw.write("\t</owl:ObjectProperty>\n")
                    else:
                        fw.write(key[0:-3] + str(count) + key[len(key)-3:len(key)-1] + "\n")
                        fw.write(element)
                        fw.write("\t</owl:ObjectProperty>\n")
                    count += 1
            else:
                fw.write(key)
                fw.write(object_dictionary[key][0])
                fw.write("\t</owl:ObjectProperty>\n")
        for key, elements in datatype_dictionary.items():
            count = 0
            if len(datatype_dictionary[key]) > 1:
                for element in elements:
                    if count == 0:
                        fw.write(key)
                        fw.write(element)
                        fw.write("\t</owl:DatatypeProperty>\n")
                    else:
                        fw.write(key[0:-3] + str(count) + key[len(key) - 3:len(key) - 1] + "\n")
                        fw.write(element)
                        fw.write("\t</owl:DatatypeProperty>\n")
                    count += 1
            else:
                fw.write(key)
                fw.write(datatype_dictionary[key][0])
                fw.write("\t</owl:DatatypeProperty>\n")
        for key, elements in named_individual_dictionary.items():
            fw.write(key)
            named_individual_dictionary[key].append("\t</owl:NamedIndividual>\n")
            for element in elements:
                fw.write(element)
        fw.write("</rdf:RDF>")
    return new_file
