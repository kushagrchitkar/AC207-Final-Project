"""
This runs test for the methods of Machine Learning class in ml.py
"""
import os
import sys
import numpy as np 

#get the absolute path of the "code" dir
code_path = os.path.abspath("code")

# add the absolute path to sys.path
sys.path.append(code_path)

from baseclass import Extractor
from ml import SpectralClassifier
import pandas as pd
import pytest

class TestSpectralClassifier:
    _query = "SELECT specObjID, lambdaEff, class, z, RUN2D, PLATE, MJD, FIBERID, ra, dec FROM SpecObj WHERE ra > 185 AND ra < 185.2 AND dec > 15 AND dec < 15.2"

    def test_ml(self):
        extractor = Extractor.from_query(self._query)
        ml = SpectralClassifier(extractor, n_features=100)
        
        # Test getting features and labels
        features, labels = ml.get_features_labels()
        assert isinstance(features, np.ndarray), "Features should be a numpy array"
        assert isinstance(labels, np.ndarray), "Labels should be a numpy array"
        assert len(features) == len(labels)
        X_train, X_test, y_train, y_test = ml.split_data(0.2)
        ml.fit(X_train, y_train)

        # Assertions to check if the model is trained, for example, by checking if it can make predictions
        assert len(ml.predict(X_test)) == len(y_test), "Predicted labels should match test set size"
        assert len(ml.predict_proba(X_test)[0]) == len(y_test)
