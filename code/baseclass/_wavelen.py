import numpy as np

def align_wavelength(self, min_val, max_val, num_of_points):
	"""Aligns wavelength of all spectral objects. 
	
	Args:
		min_val (int, float): Lower bound for interpolation.
		max_val (int, float): Upper bound for interpolation.
		num_of_points (int): Number of equispaced points to interpolate within bounds. 
		
	Returns: 
		Dictionary with interpolated flux and common wavelength grid.
		
	Raises:
		ValueError: If min_val >= max_val.
		ValueError: If num_of_points is non-positive.
	"""

	# check if min_val is less than max_val and num_of_points is greater than 0
	if min_val >= max_val or num_of_points <= 0:
		raise ValueError("Error: Please ensure min wavelength is less than max wavelength and number of points is greater than 0.")

	wavelength_array = np.linspace(min_val, max_val, num_of_points)
	interpolated_data = {}

	for obj_id in self._spec_dict.keys():  # need to use self._spec_dict
		interpolated_flux = self.interpolate(obj_id, wavelength_array)
		interpolated_data[obj_id] = {'wavelength': wavelength_array, 'flux': interpolated_flux}
		
	return interpolated_data
