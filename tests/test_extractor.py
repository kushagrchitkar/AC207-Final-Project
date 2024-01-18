"""
This runs test for the methods of Extractor class in extractor.py
"""
import os
import sys
import numpy as np 

#get the absolute path of the "code" dir
code_path = os.path.abspath("code")

# add the absolute path to sys.path
sys.path.append(code_path)

from baseclass import Extractor
import pandas as pd
import pytest

class TestExtractor:
	"""Runs test for the methods of Extractor class in extractor.py"""
    
	_query = "SELECT specObjID, lambdaEff, class, z, RUN2D, PLATE, MJD, FIBERID, ra, dec FROM SpecObj WHERE ra > 185 AND ra < 185.1 AND dec > 15 AND dec < 15.1"
	_query2 = "SELECT specObjID, lambdaEff, class, z, zerr, RUN2D, PLATE, MJD, FIBERID, ra, dec FROM SpecObj WHERE ra > 185 AND ra < 185.1 AND dec > 15 AND dec < 15.1"

	def test_from_query(self):
		extractor = Extractor.from_query(self._query)
		# check type
		assert isinstance(extractor, Extractor)
		data = extractor.get_data()
		# check if required columns exist
		assert sorted(list(data.columns)) == sorted(extractor.get_params())
        
	def test_from_query_extra_columns(self):
		extractor = Extractor.from_query(self._query2)
		# check type
		assert isinstance(extractor, Extractor)
		data = extractor.get_data()
		# check if required columns exist
		assert sorted(list(data.columns)) == sorted(extractor.get_params())
        
	def test_from_params(self):
		extractor = Extractor.from_params(185.0, 185.1, 15.0, 15.1)
		# check type
		assert isinstance(extractor, Extractor)
		data = extractor.get_data()
		extractor2 = Extractor.from_query(self._query)
		data2 = extractor2.get_data()
		assert data.equals(data2)
        
	def test_valid_df_empty(self):
		with pytest.raises(ValueError, match="Query range does not contain any objects--try again!"):
			Extractor._valid_df(pd.DataFrame())
            
	def test_valid_df_wrong_type(self):
		with pytest.raises(TypeError, match="Please input a dataframe"):
			Extractor._valid_df("not_a_dataframe")
            
	def test_from_query_invalid_query_type(self):
		with pytest.raises(TypeError, match="Query should be a string"):
			Extractor.from_query(123)
            
	def test_from_params_invalid_param_type(self):
		with pytest.raises(TypeError, match="'185.0' should be a float"):
			Extractor.from_params("185.0", 185.1, 15.0, 15.1)
            
	def test_get_wavelength(self):
		extractor = Extractor.from_query(self._query)
		df = extractor.get_data()
		wave1 = extractor.get_wavelength(df["specObjID"][0])
		flux1 = extractor.get_flux(df["specObjID"][0])
		with pytest.raises(ValueError, match="Given specObjID not part of dataframe."):
			wave2 = extractor.get_wavelength(123)
		with pytest.raises(ValueError, match="Given specObjID not part of dataframe."):
			flux2 = extractor.get_flux(123)
            
	def test_normalize(self):
		extractor = Extractor.from_query(self._query)
		df = extractor.get_data()
		extractor.normalize_flux()
		norm_flux = extractor.get_flux(df["specObjID"][0])
		assert 0 <= np.abs(np.mean(norm_flux)) < 1
		assert 0 <= np.abs(np.std(norm_flux)-1) < 1
        
	def test_remove_outliers(self):
		extractor = Extractor.from_query(self._query)
		df = extractor.get_data()
		extractor.remove_outliers()
		flux = extractor.get_flux(df["specObjID"][0])
		assert sum(flux < 0) == 0
        
	def test_interpolate(self):
		extractor = Extractor.from_query(self._query)
		df = extractor.get_data()
		wavelength = extractor.get_wavelength(df["specObjID"][0])
		arr_wv = np.linspace(wavelength.min(), wavelength.max(), 10)
		inter = extractor.interpolate(df["specObjID"][0], arr_wv)
		assert len(inter) == 10
        
	def test_redshift(self):
		extractor = Extractor.from_query(self._query)
		extractor.redshift_correction()
		df = extractor.get_data()
		assert 'lambdaEff' in df.columns

	def test_augment_data_unsupported_degree(self):
		extractor = Extractor.from_query(self._query)
		# Negative degree
		with pytest.raises(ValueError):
			extractor.augment_data(-1)  
		# Zero degree
		with pytest.raises(ValueError):
			extractor.augment_data(0)  
		# Non-numeric degree
		with pytest.raises(ValueError):
			extractor.augment_data("a")  

	def test_augment_derivative(self):
		extractor = Extractor.from_query(self._query)
		degree = 1
		extractor.augment_data(degree)
		# checking if the augmentation actually appends data to the spec_dict (1st derivative)
		for specObj, data_list in extractor._spec_dict.items():
			assert len(data_list) > 2
		degree_2 = 2
		extractor.augment_data(degree_2)
		# checking if the augmentation actually appends data to the spec_dict (2nd derivative)
		for specObj, data_list in extractor._spec_dict.items():
			assert len(data_list) > 2

	def test_fractional_derivative(self):
		extractor = Extractor.from_query(self._query)
		df = extractor.get_data()      
		specObjID = df["specObjID"][0]
		flux = extractor.get_flux(specObjID)
		wavelength = extractor.get_wavelength(specObjID)
		# Compute the fractional derivative
		alpha = 0.5
		fractional_derivative = extractor.calculate_fractional_derivative(flux, wavelength, alpha)
		# Check if the fractional derivative is different from the original flux
		assert len(flux) == len(fractional_derivative), "Length of the original and derivative arrays should be equal"
		assert not np.array_equal(flux, fractional_derivative), "Fractional derivative should differ from original flux"
  	
	def test_align_wavelength(self):
		extractor = Extractor.from_query(self._query)

		min_val = 3000 
		max_val = 7000
		num_of_points = 100 

		result = extractor.align_wavelength(min_val, max_val, num_of_points)

		assert isinstance(result, dict)
		key = next(iter(result))
		assert 'wavelength' in result[key]
		assert 'flux' in result[key]
		assert len(result[key]['wavelength']) == num_of_points
		assert len(result[key]['flux']) == num_of_points
