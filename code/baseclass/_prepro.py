from sklearn import preprocessing
import pandas as pd
import numpy as np

def normalize_flux(self):
	"""Normalizes flux for all spectral objects.
	
	Note:
		This particular normaliser applies the StandardScaler by subtracting the mean and dividing by the standard deviation.
	
	"""
	for specObjID in self._spec_dict.keys():
		# Get raw flux for the current specObjID
		raw_flux = self._spec_dict[specObjID][0]
		
		# Use StandardScaler to normalize the flux
		scaler = preprocessing.StandardScaler()
		norm_flux = scaler.fit_transform(raw_flux.reshape(-1, 1))
		
		# Update the normalized flux in the _spec_dict
		self._spec_dict[specObjID][0] = norm_flux.reshape(-1,)

def remove_outliers(self):
	"""Remove outliers with negative flux.
	
	Note:
		Avoid calling normalize_flux() before remove_outliers() as normalisation will transform many flux values into the negatives.
	"""
	for specObjID in self._spec_dict.keys():
		# Get flux and wavelength for the current specObjID
		flux = self._spec_dict[specObjID][0]
		wave = self._spec_dict[specObjID][1]
		
		# Filter flux for positive values
		mask = flux >= 0 
		
		# Update _spec_dict with filtered flux and wavelength
		self._spec_dict[specObjID] = [flux[mask], wave[mask]]

def interpolate(self, specObjID, arr_wavelength):
	"""Interpolates flux as a function of wavelength for the given specObjID.

	Args:
		specObjID (int): Object ID for the spectrum.
		arr_wavelength (array-like): Array of wavelengths for interpolation.

	Returns:
		numpy.ndarray: Interpolated flux values.

	Raises:
		ValueError: If an unsupported specObjID is provided.
    	"""
	if specObjID not in self._spec_dict.keys():
		raise ValueError("Given specObjID not part of the dataset.")
		
	flux, wave = self._spec_dict[specObjID]
	return np.interp(arr_wavelength, wave, flux)

def redshift_correction(self):
	"""Corrects observed wavelength into wavelength on Earth and appends the corrected wavelength to the dataframe as 'lambda_earth'.
	
	Note: 
		In general wavelength_earth = observed_wavelength / (1 + redshift)
	
	"""
	df = self.get_data()
	
	# Calculate redshift-corrected wavelength on Earth
	z = df['z']
	lambda_eff = df['lambdaEff']
	lambda_earth = lambda_eff / (1 + z)
	
	# Append 'lambda_earth' column to the DataFrame
	df['lambda_earth'] = lambda_earth
