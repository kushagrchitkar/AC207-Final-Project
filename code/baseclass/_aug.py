import numpy as np
from scipy.special import binom

def calculate_fractional_derivative(self, flux, wave, degree, h=1):
    """Calculate the fractional derivative of a given function using the Grünwald-Letnikov approach.

    Args:
        flux (numpy.ndarray): Array of function values (y-values).
        wave (numpy.ndarray): Array of independent variable values (x-values).
        degree (float): The fractional degree of the derivative.
        h (float): The step size for calculation (default is 1).

    Returns:
        numpy.ndarray: Array of the fractional derivative values.
    """

    N = len(flux)
    fractional_derivative = np.zeros(N)

    # Adjust h based on the wavelength array, if necessary
    if len(wave) > 1:
        h = wave[1] - wave[0]

    for i in range(N):
        sum_series = 0
        for k in range(i + 1):
            binomial_coefficient = binom(degree, k)
            sum_series += ((-1) ** k) * binomial_coefficient * flux[i - k]

        fractional_derivative[i] = sum_series / (h ** degree)

    return fractional_derivative

def augment_data(self, degree):
    """Augment the data associated with the object ID using the specified degree of derivative.

    This method calculates the derivative (first, second, or fractional) of the spectroscopic data
    and appends it to the data in the Extractor's spec_dict.

    Args:
        degree (float, int): The degree of the derivative for augmentation.

    Raises:
        ValueError: If an unsupported degree is provided.
    """
    for specObj in self._spec_dict.keys():
        flux = self.get_flux(specObj)
        wave = self.get_wavelength(specObj)

        if isinstance(degree, int) and degree in [1, 2]:
            if degree == 1:
                derivative = np.gradient(flux, wave)
            elif degree == 2:
                first_derivative = np.gradient(flux, wave)
                derivative = np.gradient(first_derivative, wave)
        elif isinstance(degree, (float, int)) and degree > 0:
            derivative = self.calculate_fractional_derivative(flux, wave, degree)
        else:
            raise ValueError(f"Unsupported degree: {degree}. Degree must be a positive integer or float.")

        self._spec_dict[specObj].append(derivative)
