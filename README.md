# Project Structure 


## Team: team02_2023

[![API Tests](https://code.harvard.edu/CS107/team02_2023/actions/workflows/test.yml/badge.svg?branch=main)](https://code.harvard.edu/CS107/team02_2023/actions/workflows/test.yml) [![Test Coverage](https://code.harvard.edu/CS107/team02_2023/actions/workflows/coverage.yml/badge.svg?branch=main)](https://code.harvard.edu/CS107/team02_2023/actions/workflows/coverage.yml)

# Link to API 

https://test.pypi.org/project/team2-api/

## API Project Structure

The project is organized into the following structure: 

```
API_project_root/
│
├── README.md
├── LICENSE
├── .github/
│   └── workflows/
│       ├── coverage.yml
│       └── test.yml
├── .gitignore
├── API_draft/
│   ├── APIdiagram
│   └── README.md
├── code/
│   ├── baseclass/
│   │   ├── __init__.py
│   │   ├── _prepro.py
│   │   ├── _wavelen.py
│   │   └── _aug.py
│   ├── viz.py
│   └── ml.py
├── tests/
│   ├── test_extractor.py
│   ├── test_viz.py
│   └── test_ml.py
├── html/
│   ├── index.html (documentation via Sphinx)
│   └── ...
├── docs/
│   ├── milestone4.md
│   ├── milestone5.md
│   └── AC207_Milestone 2.pdf
└── tutorial/
    ├── data/
    │   └── example.csv
    └── vignette_modules.ipynb

```

## API Description
Our API `Galaxy_explorer` consists of a library designed to assist with astronomical research, specifically focusing on the classification of stars, galaxies, and QSOs (Quasi-Stellar Objects). It interfaces with the Sloan Digital Sky Survey (SDSS) services and databases. The API accepts an ADQL (Astronomical Data Query Language) query in string format, a series of constraints for a select subset of variables, and data in the same format as obtained from the SDSS.

These are the modules and classes in our API. For specific details regarding functions and methods for these modules and classes are in the `API_draft`. 

### Modules
1. Augmentation (baseclass/_aug.py): Calculate the fractional derivative of a given function using the Grünwald-Letnikov approach.
2. Preprocessing (baseclass/_prepro.py): Normalize, remove outliers, interpolate flux, redshift correction.
3. Wavelength alignment (baseclass/_wavelen.py): Align wavelength of spectral objects.

### Classes
1. Extractor (baseclass/\_\_init\_\_.py): Metadata Extraction (imports Augmentation, Preprocessing and Wavelength alignment modules)
2. Visualization (viz.py): Visualise the spectrum of stellar objects, allowing interactive plot of an object's spectrum according to selected region.
3. SpectralClassifier (ml.py): A logistic regression classifier that predicts the class (e.g., star, galaxy) of objects based on spectral data.


## Software Development Agreement

In agreement with a client from the CS107/AC207 teaching staff, developers in team 2 group are designing, developing, and implementing software according to the software requirements specification in `AC207_Milestone 2.pdf` file. 

## Necessary Installation
Please run below code to install all necessary dependencies:

```
pip install pytest
pip install pandas
pip install scikit-image
pip install matplotlib
pip install scikit-learn
pip install astropy
pip install numpy
pip install scipy
pip install ipywidgets
pip install pytest-cov
pip install -i https://test.pypi.org/simple/ team2-api

git clone http://github.com/sciserver/SciScript-Python.git
cd SciScript-Python
python ShowSciServerTags.py
python Install.py
```

#### Link to API library: [team2_api](https://test.pypi.org/project/team2-api/)

## Testing


To run the existing test suite, run either of below in the root project directory and after cloning our git repository:

```
pytest tests

# With coverage
pytest tests --cov=code
```
The above code will throw a "no module found" error when running tests for "ml" and "viz" if you have already installed our team2_api. The reason for this is that, after installation, there is an "ml.py" and "viz.py" in the `site-packages` of your environment where you installed our package. Additionally, if there are already "ml.py" and "viz.py" from previous installations, then the above code will also throw a "no module found" error.

To run the existing test suite in the library after installing our team2_api, ensure that the library is installed in your personal environment, activate the environment, and ensure that you already have all the dependencies installed:

```
pytest tests

# With coverage
pytest tests --cov=team2_api
```

## Library's Functionalities Explanation
Examples are provided in `tutorial/vignette_modules.ipynb` for basic use of the API. 
