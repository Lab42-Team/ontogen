import operator
import collections
from math import sqrt


CATEGORICAL_COLUMN = "CATEGORICAL"  # Categorical column type
LITERAL_COLUMN = "LITERAL"  # Literal column type
SUBJECT_COLUMN = "SUBJECT"  # Subject column type


def is_float(string):
    """
    Determines if a string is a numeric value
    :param string: source string
    :return: True if the string is a number, False otherwise
    """
    try:
        float(string.replace(",", "."))
        return True
    except ValueError:
        return False


def get_empty_cell_fraction(source_table, classified_table):
    """
    Get percentage of empty cells for categorical columns
    :param source_table: source dictionary (table) consisting of objects: key and entity reference (cell value)
    :param classified_table: dictionary (table) with typed columns
    :return: dictionary with score for each column
    """
    result_list = dict()
    # Calculate the total number of cells in a column
    cell_number = len(source_table)
    # Bypass column types
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            # Calculate the number of empty cells in a column
            empty_cell_number = 0
            for row in source_table:
                for key, mention_entity in source_table.items():
                    if column_key == key and not mention_entity:
                        empty_cell_number += 1
            # Calculate the proportion of empty cells in a column
            result_list[column_key] = empty_cell_number / cell_number

    return result_list


def get_unique_content_cell_fraction(source_table, classified_table):
    """
    Get the proportion of cells with unique content for categorical columns.
    :param source_table: source dictionary (table) consisting of objects: key and entity reference (cell value)
    :param classified_table: dictionary (table) with typed columns
    :return: dictionary with score for each column
    """
    result_list = dict()
    # Calculate the total number of cells in a column
    cell_number = len(source_table)
    # Bypass column types
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            # Calculate the number of cells with unique content
            col = collections.Counter()
            for row in source_table:
                for key, mention_entity in source_table.items():
                    if column_key == key:
                        col[mention_entity] += 1
            # Calculate the proportion of cells with unique content in a column
            result_list[column_key] = len(col) / cell_number

    return result_list


def get_distance_from_first_ne_column(classified_table):
    """
    Getting the distance from the first entity column for categorical columns
    :param classified_table: dictionary (table) with typed columns
    :return: dictionary with score for each column
    """
    result_list = dict()
    column_number = 0
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            result_list[column_key] = column_number
        column_number += 1

    return result_list


def get_average_word_number(source_table, classified_table):
    """
    Getting the average number of words for categorical columns
    :param source_table: source dictionary (table) consisting of objects: key and entity reference (cell value)
    :param classified_table: dictionary (table) with typed columns
    :return: dictionary with score for each column
    """
    result_list = dict()
    # Calculate the total number of cells in a column
    cell_number = len(source_table)
    # Bypass column types
    for column_key, column_type in classified_table.items():
        if column_type == CATEGORICAL_COLUMN:
            # Count the number of words in cells
            total_word_number = 0
            for row in source_table:
                for key, mention_entity in source_table.items():
                    if column_key == key and mention_entity:
                        total_word_number += len(mention_entity.split())
            # Calculate the average number of words in the cells of a column
            result_list[column_key] = total_word_number / cell_number

    return result_list


def define_subject_column(source_table, classified_table, index=None):
    """
    Definition of an essential (thematic) column based on heuristic estimates
    :param source_table: source dictionary (table) consisting of objects: key and entity reference (cell value)
    :param classified_table: dictionary (table) with typed columns
    :param index: explicit indication of the number of the entity (thematic) column
    :return: dictionary (table) with marked entity (thematic) column
    """
    result_list = dict()
    # If the column number is explicitly specified, then this column is assigned to the essential (thematic)
    if is_float(str(index)) and 0 <= index <= len(classified_table):
        i = 0
        for key, type_column in classified_table.items():
            if i == index:
                result_list[key] = SUBJECT_COLUMN
            else:
                result_list[key] = type_column
            i += 1
    else:
        sub_col = dict()
        # Get the proportion of empty cells
        empty_cell_fraction = get_empty_cell_fraction(source_table, classified_table)
        # Get the proportion of cells with unique content
        unique_content_cell_fraction = get_unique_content_cell_fraction(source_table, classified_table)
        # Get the distance from the first entity column
        distance_from_first_ne_column = get_distance_from_first_ne_column(classified_table)
        # Get the average number of words
        average_word_number = get_average_word_number(source_table, classified_table)
        # Estimation aggregation
        for key, type_column in classified_table.items():
            if type_column == CATEGORICAL_COLUMN:
                sub_col[key] = (2 * unique_content_cell_fraction[key] + average_word_number[key] -
                                empty_cell_fraction[key]) / sqrt(distance_from_first_ne_column[key] + 1)
        # Determining the column key with the highest score
        subject_key = max(sub_col.items(), key=operator.itemgetter(1))[0]
        # Formation of a dictionary with a certain essential (thematic) column
        for key, type_column in classified_table.items():
            if key == subject_key:
                result_list[key] = SUBJECT_COLUMN
            else:
                result_list[key] = type_column

    return result_list
