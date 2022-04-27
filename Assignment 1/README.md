# Data Ingestion and Visualization using GCP

[Live GitHub Page](https://kshitijzutshi.github.io/DAMG7245-Assignment1/) :rocket:

### Understanding the SEVIR dataset

Asking the following questions -

1. Where is the data?
2. What is the data about?
3. How do we plan to access it?

### Understanding the data visualization

Asking the following questions - 

1. What were the longest occurring events in the data?
2. What was the Age-to-Sex distribution for all events in the data?
3. What were the most occurring event types in the data?
4. What was the Geo-Location distribution of Indirect and Direct injuries in the data?

### Run CodeLabs
Login Using a Google account to access the codelab below

Run the [CodeLab Live Here](https://codelabs-preview.appspot.com/?file_id=1PctEbzkwbyFJlADhzmLieD-Jzh-_xK5x-QO1SedG3xY#7) :rocket:


### Project Organization

[Check the cookie-cutter generated directory structure here.](https://github.com/kshitijzutshi/DAMG7245-Assignment1/tree/main/data-ingestion-and-visualization-using-gcp)

------------
### Requirements to use the cookiecutter template:
-----------
 - Python 2.7 or 3.5+
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:

``` bash
$ pip install cookiecutter
```

or

``` bash
$ conda config --add channels conda-forge
$ conda install cookiecutter
```

### To start a new project, run:
------------

``` bash
    cookiecutter -c v1 https://github.com/drivendata/cookiecutter-data-science
```

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------


### Installing development requirements
------------

    pip install -r requirements.txt

### Running the tests
------------

    py.test tests



### Team Member

| NUID | Team Member       |
|:-----:|---------------|
| 001021288    | Kshitij Zutshi |
| 001524484      | Priyanka Dilip Shinde              |
| 002114630      | Dwithika Shetty              |
