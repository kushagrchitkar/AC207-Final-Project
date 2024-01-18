from SciServer import SkyQuery, SkyServer
from astropy.io import fits
import warnings
warnings.filterwarnings("ignore")
import os
import pandas as pd
import numpy as np

class Extractor:
	"""This class extracts spectral data from SDSS server based on input dataframe with parameters. This extractor class includes constructors and relevant specific functions for preprocessing, wavelength alignment, and data augmentation.
	
	Attributes:
		data (pandas dataframe): The dataframe that contains the meta data information. 

	"""
	_params = ["specObjID", "class", "ra", "dec", "z", "RUN2D", "PLATE", "MJD", "FIBERID", "lambdaEff"]
	_DataRelease = "DR18" # user is restricted to DR18 since we are extracting spectral data for DR18. 
    
	@staticmethod
	def _valid_df(df):
		"""Checks if the dataframe is not empty, of correct type, and contains necessary params.
		
		Parameters:
			df (pandas dataframe): The dataframe to validate.
		
		Raises:
			TypeError: If the input is not a dataframe.
			ValueError: If the dataframe is empty or lacks necessary parameters.

		"""
		if not isinstance(df, pd.DataFrame):
			raise TypeError("Please input a dataframe")
		if len(df) == 0:
			raise ValueError("Query range does not contain any objects--try again!")
		for param in Extractor._params:
			if param not in df.columns:
				raise ValueError(f"Query did not include necessary '{param}' parameter--try again!")

	def __init__(self, data):
		"""Constructs an instance of the class with the given dataframe.
		
		Parameters:
			data (pandas dataframe): The input dataframe containing spectral data parameters.
		
		Raises:
			TypeError: If the input data is not a dataframe.
			ValueError: If the dataframe is empty or lacks necessary parameters.
		
		Note:
			The constructor extracts wavelength and flux from FITS files corresponding to the input dataframe's specObjID, PLATE, MJD, and FIBERID.
			The extracted spectral data is stored in a dictionary (_spec_dict) with specObjID as keys and lists of flux and wavelength arrays as values.
		
		"""
		self._valid_df(data)
		self._data = data[Extractor._params]

		# Extract wavelength and flux from FITS file
		spec_dict = {}
		for index, row in self._data.iterrows():
			spec_obj_id = row['specObjID']
			plate = row['PLATE']
			mjd = row['MJD']
			fiber_id = row['FIBERID']
			base_url = 'http://dr18.sdss.org/optical/spectrum/view/data/'
			url = f"{base_url}format=fits/spec=full?plateid={plate}&mjd={mjd}&fiberid={fiber_id}"
			try:
				desired_timeout = 10  # 10 seconds
				print(f"Attempting to open URL: {url}")
				file = fits.open(url, timeout=desired_timeout)
				data = file[1].data
				flux = np.array(data['flux'])
				wave = np.array(10**data['loglam'])
				spec_dict[spec_obj_id] = [flux, wave]
			except TimeoutError as e:
				print(f"TimeoutError for specObjID {spec_obj_id}: {e}")
			except Exception as e:
				print(f"Error processing specObjID {spec_obj_id}: {e}")

		self._spec_dict = spec_dict
      
	@classmethod
	def from_query(cls, query):
		"""Executes given ADQL query from DR18 and constructs an instance of the class.
		
		Parameters:
			query (str): The ADQL query string.
		
		Raises:
			TypeError: If the input query is not a string.
		
		Returns:
			Extractor: An instance of the Extractor class constructed from the query results.
		
		"""
		# Check if query is string
		if not isinstance(query, str):
			raise TypeError("Query should be a string")
		# Execute given query
		df = SkyServer.sqlSearch(sql=query, dataRelease=Extractor._DataRelease)
		# Call constructor
		return cls(df)
    
	@classmethod
	def from_params(cls, min_ra, max_ra, min_dec, max_dec):
		"""Executes ADQL query based on input constraints and constructs an instance of the class.
		
		Parameters:
			min_ra, max_ra, min_dec, max_dec (float): Constraints for the query.
		
		Raises:
			TypeError: If any of the input parameters are not floats.
		
		Returns:
			Extractor: An instance of the Extractor class constructed from the query results.
		
		"""
		for param in [min_ra, max_ra, min_dec, max_dec]:
			if not isinstance(param, float):
				raise TypeError(f"'{param}' should be a float")
		query = "SELECT " + ', '.join(Extractor._params) + f" FROM SpecObj WHERE ra > {min_ra} AND ra < {max_ra} AND dec > {min_dec} AND dec < {max_dec}"
		df = SkyServer.sqlSearch(sql=query, dataRelease=Extractor._DataRelease)
		# Call constructor
		return cls(df)
    
	# The Extractor class getter functions. These functions facilitate external access to private or protected attributes, promoting encapsulation and offering a controlled means to interact with an instance object's internal state.
    
	def get_data(self):
		"""Getter for dataframe containing params.
		
		Returns:
			pandas.DataFrame: The dataframe containing parameters.

		"""
		return self._data
    
	def get_params(self):
		"""Getter params of interest list.
		
		Returns:
			list: The list of parameters of interest.

		"""
		return Extractor._params
    
	def get_spec_dict(self):
		"""Getter for spectral data. Note this returns a dictionary.
		
		Returns:
			dict: A dictionary containing spectral data.

		"""
		return self._spec_dict
    
	def get_wavelength(self, specObjID):
		"""Getter for wavelength of a particular object. Note the object is expected to be in the dataframe.
		
		Parameters:
			specObjID: The identifier for the spectral object.
		
		Returns:
			numpy array: The wavelength data for the specified object.
		
		Raises:
			ValueError: If the given specObjID is not part of the dataframe.

		"""
		if specObjID not in self._spec_dict.keys():
			raise ValueError("Given specObjID not part of dataframe.")
		return self._spec_dict[specObjID][1]
    
	def get_flux(self, specObjID):
		"""Getter for flux of a particular object. Note the object is expected to be in the dataframe.
		
		Parameters:
			specObjID: The identifier for the spectral object.
		
		Returns:
			numpy array: The flux data for the specified object.
		
		Raises:
			ValueError: If the given specObjID is not part of the dataframe.
        
		"""
		if specObjID not in self._spec_dict.keys():
			raise ValueError("Given specObjID not part of dataframe.")
		return self._spec_dict[specObjID][0]
    
	# These functions can not imported outside of this Extractor module in the baseclass subdirectory. By importing here inside our Extractor class user has access to it once they import Extractor. 
    
	# Preprocessing specific functions to use after extracting spectral data. 
	from ._prepro import normalize_flux, remove_outliers, redshift_correction, interpolate
    
	# Wavelenght Alignment specific functions to use after extracting spectral data. 
	from ._wavelen import align_wavelength
    
	# Data Augmentation specific functions to use after extracting spectral data. 
	from ._aug import calculate_fractional_derivative, augment_data
