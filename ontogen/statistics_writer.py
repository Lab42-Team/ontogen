def write_statistic(owl_path, precision, recall, f11, precision1,
                    recall1, f111, statistic_name, counter=None):
    """
    Compiling statistics
        :param owl_path: owl ontology
        :param precision: precision of schema
        :param recall: recall of schema
        :param f11: f1 - measure of schema
        :param precision1: precision of named individuals
        :param recall1: recall of named individuals
        :param f111: f1 - measure of named individuals
        :param counter: number of rating files
        :return: string with total statistic
    """
    text = "total_statistics.txt"
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
    with open(statistic_name, 'a', encoding='utf-8') as f:
        f.write("Number of classes: " + str(count_class) + "\n")
        f.write("Number of object properties: " + str(count_object_prop) + "\n")
        f.write("Number of datatype properties: " + str(count_datatype_prop) + "\n")
        f.write("Number of named individuals: " + str(count_individual) + "\n" + "\n")
        if owl_path == "TotalOntology.owl":
            print()
            print("Total Ontology:")
            print("Number of classes: ", count_class)
            print("Number of object properties: ", count_object_prop)
            print("Number of datatype properties: ", count_datatype_prop)
            print("Number of named individuals: ", count_individual)
            print("Evaluation for ontology schema:")
            if counter != 0:
                print("Precision: ", precision/counter)
                print("Recall: ", recall / counter)
                print("F1: ", f11 / counter)
                print()
                print("Evaluation for named individuals:")
                print("Precision: ", precision1 / counter)
                print("Recall: ", recall1 / counter)
                print("F1: ", f111 / counter)
                print("------------------------------------------------")
                f.write("Total Ontology:" + "\n" + "Evaluation for ontology schema:" + "\n" + "Precision: " + str(precision/counter)
                        + "\n" + "Recall: " + str(recall / counter) + "\n" + "F1: " + str(f11 / counter) + "\n"
                        + "Evaluation for named individuals:" + "\n" + "\n" + "Precision: " +
                        str(precision1 / counter) + "\n" + "Recall: " + str(recall1 / counter) + "\n" + "F1: " +
                        str(f111 / counter) + "\n")
            else:
                print("Counter = 0")
        else:
            print("Number of classes: ", count_class)
            print("Number of object properties: ", count_object_prop)
            print("Number of datatype properties: ", count_datatype_prop)
            print("Number of named individuals: ", count_individual)
            print("------------------------------------------------")
            print()
            f.write("Evaluation for ontology schema:" + "\n")
            f.write("Precision: " + str(precision) + "\n")
            f.write("Recall: " + str(recall) + "\n")
            f.write("F1: " + str(f11) + "\n")
            f.write("Evaluation for named individuals:" + "\n")
            f.write("Precision: " + str(precision1) + "\n")
            f.write("Recall: " + str(recall1) + "\n")
            f.write("F1: " + str(f111) + "\n")
    return text
