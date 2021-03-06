def write_statistic(owl_path, precision, recall, f11, precision1,
                    recall1, f111, counter = None):
    text = "statistic.txt"
    with open(owl_path, 'r', encoding='utf-8') as f:
        count_individual = 0
        count_class = 0
        count_object_prop = 0
        count_datatype_prop = 0
        for line in f:
            if line.find("<owl:NamedIndividual") != -1:
                count_individual = count_individual + 1
            if line.find("<owl:Class") != -1:
                count_class = count_class + 1
            if line.find("<owl:ObjectProperty") != -1:
                count_object_prop = count_object_prop + 1
            if line.find("<owl:DatatypeProperty") != -1:
                count_datatype_prop = count_datatype_prop + 1
    with open(text, 'a', encoding='utf-8') as f:
        print(owl_path)
        print("Number of classes: ", count_class)
        print("Number of object properties: ", count_object_prop)
        print("Number of datatype properties: ", count_datatype_prop)
        print("Number of Named individuals: ", count_individual)
        print()
        f.write(owl_path + "\n")
        f.write("Number of classes: " + str(count_class) + "\n")
        f.write("Number of object properties: " + str(count_object_prop) + "\n")
        f.write("Number of datatype properties: " + str(count_datatype_prop) + "\n")
        f.write("Number of Named individuals: " + str(count_individual) + "\n" + "\n")
        if owl_path == "new_file1.owl":
            print()
            print("Total:")
            print("Precision ", precision/counter)
            print("Recall ", recall / counter)
            print("F1 ", f11 / counter)
            print()
            print("Precision ", precision1 / counter)
            print("Recall ", recall1 / counter)
            print("F1 ", f111 / counter)
            f.write("Total:" + "\n" + "Precision " + str(precision/counter) + "\n" + "Recall " +
                    str(recall / counter) + "\n" + "F1 " + str(f11 / counter) + "\n" + "Precision " +
                    str(precision1 / counter) + "\n" + "Recall " + str(recall1 / counter) + "\n" + "F1 " +
                    str(f111 / counter) + "\n")
        else:
            f.write("Accuracy for ontology schema:" + "\n")
            f.write("Precision " + str(precision) + "\n")
            f.write("Recall " + str(recall) + "\n")
            f.write("F1 " + str(f11) + "\n")
            f.write("Accuracy for named individuals:" + "\n")
            f.write("Precision " + str(precision1) + "\n")
            f.write("Recall " + str(recall1) + "\n")
            f.write("F1 " + str(f111) + "\n")
    return text
