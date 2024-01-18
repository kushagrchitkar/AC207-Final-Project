"""
This runs test for the methods of Visualization class in viz.py
"""
import os
import sys
import numpy as np 

#get the absolute path of the "code" dir
code_path = os.path.abspath("code")

# add the absolute path to sys.path
sys.path.append(code_path)

from baseclass import Extractor
from viz import Visualization
import pandas as pd
import pytest
from unittest.mock import patch 
import matplotlib.pyplot as plt 

class TestVisualize:
    _query = "SELECT specObjID, lambdaEff, class, z, RUN2D, PLATE, MJD, FIBERID, ra, dec FROM SpecObj WHERE ra > 185 AND ra < 185.1 AND dec > 15 AND dec < 15.1"

    @patch("matplotlib.pyplot.show")
    def test_visualize(self, mock_show):
        extractor = Extractor.from_query(self._query)
        vis = Visualization(extractor)
        specObjID = 6077715550125185024
        vis.visualize(specObjID)
        extractor.normalize_flux()
        vis = Visualization(extractor)
        vis.visualize(specObjID)

    @patch("matplotlib.pyplot.show")
    def test_interactive_viz(self, mock_show):
        extractor = Extractor.from_query(self._query)
        vis = Visualization(extractor)
        specObjID = 6077715550125185024
        vis.visualize(specObjID, interactive=True)

    def test_valid_moving_window_size(self):
        with pytest.raises(ValueError, match="'moving_window_size' must be positive integer."):
            extractor = Extractor.from_query(self._query)
            vis = Visualization(extractor)
            specObjID = 6077715550125185024
            vis.visualize(specObjID, moving_window_size=1.2)

    def test_valid_specObjID(self):
        with pytest.raises(ValueError, match="Given specObjID not part of the dataset."):
            extractor = Extractor.from_query(self._query)
            vis = Visualization(extractor)
            specObjID = 6077715550125345024
            vis.visualize(specObjID)
    


