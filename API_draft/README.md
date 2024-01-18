# Galaxy_explorer API

## API Description
Our API `Galaxy_explorer` consists of a library designed to assist with astronomical research, specifically focusing on the classification of stars, galaxies, and QSOs (Quasi-Stellar Objects). It interfaces with the Sloan Digital Sky Survey (SDSS) services and databases. The API accepts an ADQL (Astronomical Data Query Language) query in string format, a series of constraints for a select subset of variables, and data in the same format as obtained from the SDSS.

## Modules

### Module 1: meta_extract (Metadata Extraction)
**Module Description:** Facilitates metadata extraction (identifiers, coordinates, chemical abundances, redshifts, or other fields as requested by the end-user) and queries the SDSS.

**Functions:**
- `extract()`

### Module 2: data_prepro (Data Preprocessing)
**Module Description:** Converts raw data into preprocessed data using methods from the `Preprocessor` class.

**Class Methods:**
- `normalize()`
- `outlier_removal()`
- `interpolation()`
- `redshift_correction()`

### Module 3: data_aug (Data Augmentation)
**Module Description:** Computes derivatives as well as fractional derivatives and appends them to each preprocessed spectrum.

**Functions:**
- `derivative()`
- `frac_derivative()`

### Module 4: align (Alignment in Wavelength)
**Module Description:** Aligns the wavelength of all the spectra across a predefined range, which may require interpolation.

**Functions:**
- `align()`

## Classes

### class_visual (Visualization)
**Class Description:** Provides a Matplotlib-based interface for spectral visualization. 

**Functions:**
- `visualize()`: Includes an overlay of the inferred continuum.
- `interactive_visualize()`: Enables users to select plot regions and quantify the flux of spectral lines.

### class_mach_learn (Machine Learning)
**Class Description:** Runs a machine learning model capable of distinguishing between Stars, Galaxies, and QSOs.

**Functions:**
- `fit()`
- `predict()`
- `predict_proba()`
