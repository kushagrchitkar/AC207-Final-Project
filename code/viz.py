from baseclass import Extractor
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.widgets import RectangleSelector, Button
from scipy.integrate import trapz

class Visualization():
    """This class provides specialised plotting features to visualise the spectrum of stellar objects contained within an Extractor class instance."""

    def __init__(self, extractor: Extractor):
        """Creates instance of Visualization class. 

        Args:
            extractor (Extractor): The Extractor class instance to enhance.
        """
        self.extractor = extractor
        self.df = None

    def onselect(self, eclick, erelease):
        """Prints integrated flux via the inferred continuum within selected region. 

        Args:
            eclick (motion): motion trigger
            erelease (motion): motion trigger

        Note:
            If selected bound is beyond wavelength range, integrated flux will evaluate to 'nan'
        """
        # Get x,y values of selected region
        x_start, x_end = eclick.xdata, erelease.xdata

        # Get wavelength and inferred continuum
        df = self.df.copy()
        wave = df['wavelength'].values
        incont = df['inferred_continuum'].values

        # Apply masks to isolate values within x-bounds
        mask = wave >= x_start
        wave_removelow, incont__removelow = wave[mask], incont[mask]
        mask2 = wave_removelow <= x_end
        wave_inbound , incont_inbound = wave_removelow[mask2], incont__removelow[mask2]

        # Print integrated flux value
        if len(wave_inbound) != 0:
            integrated_flux = trapz(incont_inbound, wave_inbound)
            print(f"Integrated flux for wavelength in [{x_start:.2f}, {x_end:.2f}]: {integrated_flux:.2f}")

    def visualize(self, specObjID, moving_window_size=100, interactive=False):
        """Generates plot of given object's spectrum.

        Args:
            specObjID (int): The stellar object to generate spectral plot for.
            moving_window_size (int): Window size to use in calculating the inferred continuum.
            interactive (bool): True for interactive mode, False otherwise.

        Raises:
            ValueError: If given specObjID is not contained in class instance.
            ValueError: If moving_window_size is not a positive integer.
        """
        # Check specObjID is in current Extractor instance
        if specObjID not in self.extractor._spec_dict.keys():
            raise ValueError("Given specObjID not part of the dataset.")
        
        # Check for valid moving_window_size
        if moving_window_size <= 0 or moving_window_size % 1 != 0:
            raise ValueError("'moving_window_size' must be positive integer.")

        # Extract wavelength and flux
        wavelength = self.extractor.get_wavelength(specObjID)
        flux = self.extractor.get_flux(specObjID)

        # Calculate inferred continuum
        df = pd.DataFrame({'wavelength': wavelength, 'flux': flux})
        df['inferred_continuum'] = df['flux'].rolling(moving_window_size).mean()
        self.df = df

        # Plot the flux over wavelength
        plt.plot(df['wavelength'], df['flux'], label='Flux', color='blue')

        # Plot the inferred continuum
        plt.plot(df['wavelength'], df['inferred_continuum'], label='Inferred Continuum', color='red')
        plt.title(f"Object ID: {specObjID}")
        plt.xlabel(f'Wavelength ($\\AA$)')
        plt.ylabel(f'Flux\n($10^{-17}$ erg/s/cm$^2$/Å)')
        plt.legend()

        if interactive:
            self.visualize_interactive()
        else:
            plt.show()

    def visualize_interactive(self):
        """Generates interactive plot of an object's spectrum according to selected region.

        Note:
            Y-values have no affect on the integration results.
        """
        # Create a RectangleSelector
        rs = RectangleSelector(plt.gca(), self.onselect, useblit=True, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)

        # Show the plot
        plt.show()