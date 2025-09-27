import csv
import json
import ftfy
import os
import re
import shutil
import click
from ontogen import statistics_writer, f_measure_identidier, unifer_creator, reg_exp_definder, ontology_creator, \
    subject_column_identifier
from datetime import datetime
from pathlib import Path


def define_literal_categorical(json_path1, json_path2, json_path3):
    """
    Defining column types
    :param json_path1: the name of the file that defines the literal values in the cells
    :param json_path2: the name of the file in which the cell types will be defined("CATEGORICAL" or "LITERAL")
    :param json_path3: the name of the file where the column types will be defined("CATEGORICAL" or "LITERAL")
    """
    with open(json_path1, 'r', encoding='utf-8') as f:
        text1 = []
        text = json.load(f)
        i = -1
        j = 0
        dictionary = {}
        dictionary1 = {}
        for str_json in text:
            keys = str_json.keys()
            for key in keys:
                dictionary[key] = ''
                dictionary1[key] = ''
            break
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                if text[i][obj_json] == 'NONE':
                    text[i][obj_json] = 'CATEGORICAL'
                else:
                    text[i][obj_json] = 'LITERAL'
                dictionary[obj_json] = [text[j][object_json] for object_json in str_json]
        k = 0
        for key in dictionary.keys():
            dictionary1[key] = [dictionary[key][k] for key in dictionary.keys()]
            k = k + 1
        keys = dictionary1.keys()
        c = 0
        length = 0
        error = 0
        for key in keys:
            k = 0
            while k < len(dictionary1[key]):
                if dictionary1[key][k] == 'CATEGORICAL':
                    c = c + 1
                else:
                    length = length + 1
                k = k + 1
            if c > length:
                dictionary1[key] = "CATEGORICAL"
            else:
                dictionary1[key] = 'LITERAL'
            if c == 0:
                error = error + 1
            c = 0
            length = 0
            text1 = [dictionary1]
        if error != 0:
            i = -1
            for str_json in text:
                i = i + 1
                for obj_json in str_json:
                    text[i][obj_json] = "CATEGORICAL"
                    break
            i = -1
            for str_json in text1:
                i = i + 1
                for obj_json in str_json:
                    text1[i][obj_json] = "CATEGORICAL"
                    break
        open_json_file(json_path2, text)
        open_json_file(json_path3, text1)


def check_path_ent(csv_path):
    """
    Checking if a file is a .csv file
    :param csv_path: file name
    :return: file name if it is a .csv file, otherwise 1
    """
    if csv_path[len(csv_path) - 4:len(csv_path)] == '.csv':
        return csv_path
    else:
        return 1


def uno_code_ftfy(json_path):
    """
    Fix broken characters and remove extra spaces
    :param json_path: json file name
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        text = json.load(f)
        new_dictionary = {}
        text1 = []
        i = -1
        for str_json in text:
            i = i + 1
            for obj_json in str_json:
                if text[i][obj_json] is None:
                    text[i][obj_json] = ""
                json_str = ftfy.fix_text(str(text[i][obj_json]))
                json_str = re.sub(r'\s+', ' ', json_str)
                json_str = re.sub(
                    r'[\!\?\№\»\^\&\*\[\]\{\}\+\=\’\|\_\№\&\<\>\-\`\±\,\′\×\;\°\'\≥\•\½\£]', '',
                    json_str)
                json_str = re.sub(r'\s+', ' ', json_str)
                if json_str == "":
                    json_str = "NONE"
                new_obj_json = ftfy.fix_text(obj_json)
                new_obj_json = re.sub(r'\s+', ' ', new_obj_json)
                new_obj_json = re.sub(
                    r'[\!\?\№\»\^\&\*\[\]\{\}\+\=\(\)\’\/\\\|\_\№\&\<\>\-\$\#\%\`\±\−\,\′\×\;\°\–\'\≥\•\½\:\£]', '',
                    new_obj_json)
                new_obj_json = re.sub(r'\s+', ' ', new_obj_json)
                if new_obj_json == "":
                    new_obj_json = "NONE"
                new_dictionary[new_obj_json] = json_str
            text1.append(new_dictionary)
            new_dictionary = {}
    open_json_file(json_path, text1)


def open_csv_file(csv_path):
    """
    Opening a .csv file
    :param csv_path: .csv file name
    :return: 0 if the file is empty, rows(string) is the content of the .csv file
    """
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, skipinitialspace=True, delimiter=',')
        rows = list(reader)
        if reader.line_num <= 1:
            return 0
        else:
            return rows


def open_json_file(json_path, rows):
    """
    Writing a .json file
    :param json_path: .json file name
    :param rows: list with .json file content
    """
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)


@click.command()
@click.option("--name", prompt="Your path to source tables", help="The path to the folder.")
def folder_owl(name):
    """
    Console User Interaction
    :param name: file path name entered by the user
    """
    click.echo(f"{name}")
    path_in = name
    path = [path_in]
    # path = ['fj:\\test']
    precision, recall, f11, precision1, recall1, f111 = 0, 0, 0, 0, 0, 0
    counter = 0
    time1 = datetime.now().time()
    rows = 0
    c = 0
    print('Start of the program at:', time1)
    cl = str(Path(__file__).parent.parent) + '/results'
    results = str(Path(__file__).parent.parent) + '/results' + '/evaluation'
    js_cl = str(Path(__file__).parent.parent) + '/results' + '/jsondocs'
    for el in path:
        if os.path.exists(el):
            if os.listdir(el):
                for awhile in os.listdir(el):
                    if awhile[-4:] == '.csv' or awhile[-5:] == '.json':
                        c = c + 1
                if c:
                    for awhile in os.listdir(el):
                        if check_path_ent(awhile) == 1 and awhile[len(awhile) - 5:len(awhile)] != '.json':
                            continue
                        else:
                            if not os.path.exists(cl):
                                os.mkdir(cl)
                            if not os.path.exists(results):
                                os.mkdir(results)
                            csv_path = el + '/' + awhile
                            if awhile[len(awhile) - 5:len(awhile)] != '.json':
                                json_path = awhile[0:len(awhile) - 4] + '.json'
                                try:
                                    rows = open_csv_file(csv_path)
                                except BaseException:
                                    print("Incorrect file! ", json_path)
                                    print("------------------------------------------------")
                                    print()
                                    continue
                            else:
                                json_full_path = el + '/' + awhile
                                try:
                                    with open(json_full_path, 'r', encoding='utf-8') as fileopen:
                                        rows = json.load(fileopen)
                                        json_path = awhile
                                except BaseException:
                                    print("Incorrect file! ", json_path)
                                    print("------------------------------------------------")
                                    print()
                                    continue
                            if rows == 0:
                                continue
                            else:
                                try:
                                    open_json_file(json_path, rows)
                                    if rows:
                                        if not os.path.exists(js_cl):
                                            os.mkdir(js_cl)
                                        json_path1 = json_path[0:len(json_path) - 5] + '1' + '.json'
                                        cf = js_cl + '/' + json_path1[:-6]
                                        if not os.path.exists(cf):
                                            os.mkdir(cf)
                                        oa = str(Path(__file__).parent.parent) + '/results' + '/owl'
                                        if not os.path.exists(oa):
                                            os.mkdir(oa)
                                        shutil.copyfile(json_path, cf + '/' + json_path)
                                        json_path2 = json_path[0:len(json_path) - 5] + '2' + '.json'
                                        json_path3 = json_path[0:len(json_path) - 5] + '3' + '.json'
                                        json_path4 = json_path[0:len(json_path) - 5] + '4' + '.json'
                                        owl_path = json_path[0:len(json_path) - 5] + '.owl'
                                        statistic_name = owl_path[:-4] + '.txt'
                                        uno_code_ftfy(json_path)
                                        json_path1, text = reg_exp_definder.create_json(json_path, json_path1)
                                        open_json_file(json_path1, text)
                                        define_literal_categorical(json_path1, json_path2, json_path3)
                                        with open(json_path3, 'r', encoding='utf-8') as f:
                                            text = json.load(f)
                                            with open(json_path, 'r', encoding='utf-8') as f1:
                                                text1 = json.load(f1)
                                                i = 0
                                                while i < len(text1):
                                                    dictionary2 = subject_column_identifier.define_subject_column(text1[i],
                                                                                                                  text[0])
                                                    i += 1
                                        text = [dictionary2]
                                        open_json_file(json_path4, text)
                                        dictionary3 = {}
                                        new_string = ontology_creator.create_ontology(json_path, json_path1, json_path4,
                                                                                      dictionary3)
                                        with open(owl_path, "w", encoding='utf-8') as my_file:
                                            my_file.write(new_string)
                                        count1, count2, count3, count4, count5, count6 = \
                                            f_measure_identidier.f_measure(json_path, json_path3, json_path4, owl_path)
                                        precision += count1
                                        recall += count2
                                        f11 = f11 + count3
                                        precision1 += count4
                                        recall1 += count5
                                        f111 += count6
                                        counter += 1
                                        statistics_writer.write_statistic(owl_path, count1,
                                                                          count2, count3, count4, count5,
                                                                          count6, statistic_name)
                                        shutil.copyfile(json_path1, cf + '/' + json_path1)
                                        shutil.copyfile(json_path2, cf + '/' + json_path2)
                                        shutil.copyfile(json_path3, cf + '/' + json_path3)
                                        shutil.copyfile(json_path4, cf + '/' + json_path4)
                                        shutil.copyfile(owl_path, oa + '/' + owl_path)
                                        shutil.copyfile(statistic_name, results + '/' + statistic_name)
                                        os.remove(json_path)
                                        os.remove(json_path1)
                                        os.remove(json_path2)
                                        os.remove(json_path3)
                                        os.remove(json_path4)
                                        os.remove(owl_path)
                                        os.remove(statistic_name)
                                    else:
                                        os.remove(json_path)
                                except BaseException:
                                    print("Incorrect file! ", json_path)
                                    print("------------------------------------------------")
                                    print()
                                    os.remove(json_path)
                                    os.remove(json_path1)
                                    os.remove(json_path2)
                                    os.remove(json_path3)
                                    os.remove(json_path4)
                                    continue
                    if os.path.exists(str(Path(__file__).parent.parent) + '/results' + '/jsondocs'):
                        new_file = unifer_creator.unifier(str(Path(__file__).parent.parent) + '/results' + '/owl')
                        statistic_name = "total_statistics.txt"
                        statistic = statistics_writer.write_statistic(new_file, precision,
                                                                      recall, f11, precision1, recall1,
                                                                      f111, statistic_name, counter)

                        shutil.copyfile(new_file, str(Path(__file__).parent.parent) + '/results' + '/owl' + '/' + new_file)
                        shutil.copyfile(statistic, results + '/' + statistic)
                        os.remove(statistic)
                        os.remove(new_file)
                else:
                    print("There are no csv or json files in this folder.")
            else:
                print('This folder is empty')
        else:
            print("This path doesn't exist", el)
    time2 = datetime.now().time()
    print('End of the program at:', time2)
    print('Total time:',
          ((time2.hour * 60 + time2.minute + ((time2.second - time1.second) / 60)) - (time1.hour * 60 + time1.minute)),
          'minutes')


if __name__ == '__main__':
    folder_owl()
