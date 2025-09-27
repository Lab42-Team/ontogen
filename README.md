# OntoGen

A command-line software called **OntoGen** for analysis and transformation of source spreadsheet data (CSV) to ontology (OWL/XML).

## Version

1.1

## Preliminaries

A source (input) spreadsheet represents a set of same type entities in a relational form (a subset of the Cartesian product of *K*-data domains), where:
1.	*Attribute (a column name)* is a name of a data domain in a relationship schema;
2.	*Metadata (a schema)* is an ordered set of *K*-attributes of a relational table;
3.	*Tuple (a record)* is an ordered set of *K*-atomic values (one for each attribute of a relation);
4.	*Data (a recordset)* is a set of tuples of a relational table.

A spreadsheet of same type entities (*a canonicalized form*) is a relational table in the third normal form (3NF), which contains an ordered set of *N*-rows and *M*-columns.

A table represents a set of entities of the same type, where:
1.	*Categorical column or Named entities column (NE-column)* contains names (text mentions) of some named entities;
2.	*Literal column (L-column)* contains literal values (e.g. dates, numbers);
3.	*Subject (thematic) column (S-column)* is a *NE*-column represented as a potential primary key and defines a subject of a source table;
4.	*Another (non-subject) columns* represent entity properties including their relationships with other entities.

**Assumption 1.** *The first row of a source spreadsheet is a header containing attribute (column) names.*

**Assumption 2.** *All values of column cells in a source spreadsheet have same entity types and data types.*

**Assumption 3.** *Source spreadsheets should be presented in the CSV format.*

**OntoGen** supports the process of ontology engineering based on spreadsheet data transformation.

**Assumption 4.** *A target ontology is presented in the [OWL2 DL](https://www.w3.org/TR/owl2-overview/) format.*

## Installation

First, you need to clone the project into your directory:

```
git clone https://github.com/Lab42-Team/ontogen.git
```

Next, you need to install all requirements for this project:

```
pip install -r requirements.txt
```

*We recommend you to use Python 3.0 or more.*

## Directory Structure

* `datasets` contains datasets of source spreadsheets in the CSV format:
    * `tough-tables` contains [Tough Tables (2T)](https://zenodo.org/record/4246370#.Yf5AO-pBw2w) dataset, where noise spreadsheets are excluded;
    * `wiki-uku-49` contains spreadsheets describing the main concepts and relationships in the field of education, in particular, universities in the United Kingdom (see [wiki-UKU-49: United Kingdom Universities from Wikipedia](https://data.mendeley.com/datasets/33v9tk6jjb/1));
    * `isi-167e` contains spreadsheets describing the main concepts and relationships in the field of Industrial Safety Inspection (see [ISI-167E: Entity spreadsheet tables](https://data.mendeley.com/datasets/3gjy46mx88/1)).
* `examples` contains spreadsheet examples for testing.
* `ontogen` contains software modules (py-scripts), including `main.py`.
* `results` contains processing results (target ontologies).

## Usage

#### Usage: python main.py [OPTIONS]
**Options:**
- `--name=c:\userpath` -- Create ontologies
#### A simple example
```
python main.py --name=C:/test
```
or

```
python main.py
Your path to source spreadsheets: C:/test
```

## Authors

* [Daria A. Denisova](mailto:daryalich@mail.ru)
* [Nikita O. Dorodnykh](mailto:tualatin32@mail.ru)