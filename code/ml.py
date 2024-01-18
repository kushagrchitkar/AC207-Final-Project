from baseclass import Extractor
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

class SpectralClassifier():
    """A classifier that predicts the class (e.g., star, galaxy) based on spectral data.

    Uses logistic regression from scikit-learn for prediction.
    """

    def __init__(self, extractor: Extractor, n_features = 100):
        """Initializes the SpectralClassifier with a data extractor and a specified number of features.

        Args:
            extractor (Extractor): An instance of the Extractor class for handling spectral data.
            n_features (int): Number of features to use for model training.
        """
        self.extractor = extractor
        self.model = make_pipeline(StandardScaler(), LogisticRegression())
        self.n_features = n_features


    def fit(self, X, y):
        """Fit the logistic regression model using the spectral data.

        Args:
            X (numpy.ndarray): The features (e.g., spectral fluxes).
            y (numpy.ndarray): The target values (e.g., class labels).
        """
        self.model.fit(X, y)

    def predict(self, X):
        """Predicts the class labels for the provided spectral data.

        Args:
            X (numpy.ndarray): The features (e.g., spectral fluxes) for prediction.

        Returns:
            numpy.ndarray: An array of predicted class labels.
        """
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Predicts the class probabilities for the provided spectral data.

        Args:
            X (numpy.ndarray): The features (e.g., spectral fluxes) for which to predict probabilities.

        Returns:
            numpy.ndarray: An array of predicted class probabilities.
        """
        return self.model.predict_proba(X)
    
    def get_confusion_matrix(self, X, y):
        """Computes the confusion matrix for the given true and predicted labels.

        Args:
            X (numpy.ndarray): The features (e.g., spectral fluxes) of the test data.
            y (numpy.ndarray): The true labels for the test data.

        Returns:
            numpy.ndarray: The confusion matrix.
        """
        y_pred = self.predict(X)
        return confusion_matrix(y, y_pred)
        
    def preprocess_data(self):
        """Preprocesses the data by applying several cleaning and normalization steps.

        This method sequentially calls the methods to remove outliers, apply redshift correction, 
        and normalize the flux values in the dataset.

        The preprocessing steps are applied directly to the data within the Extractor object, 
        modifying its state.

        No arguments are taken and no values are returned, as the function operates directly on 
        the Extractor's data.
        """
        # preprocessing steps
        self.extractor.remove_outliers()
        self.extractor.redshift_correction()
        self.extractor.normalize_flux()

    def get_features_labels(self):
        """Extracts features and labels for model training from the Extractor object.

        This method preprocesses the data and extracts the spectral fluxes as features and astronomical object classes as labels.

        Returns:
            tuple: A tuple containing two numpy.ndarrays: features and labels.
        """
        features = []
        labels = []
        min_flux = []
        max_flux = []
        label_mapping = {'STAR': 0, 'GALAXY': 1, 'QSO': 2}
        self.preprocess_data()

        common_specObjIDs = set(self.extractor.get_data()['specObjID']) & set(self.extractor.get_spec_dict().keys())
        for specObjID in common_specObjIDs:
        
            flux = self.extractor.get_flux(specObjID)
            min_flux.append(min(flux))
            max_flux.append(max(flux))
            # Compute statistical features for each flux array
            class_label = self.extractor.get_data().loc[self.extractor.get_data()['specObjID'] == specObjID, 'class'].iloc[0]
            # Convert the class label to its corresponding integer
            encoded_label = label_mapping[class_label]
            labels.append(encoded_label)
        inter_data = self.extractor.align_wavelength(max(min_flux), min(max_flux), num_of_points=self.n_features)
        for specObjID in common_specObjIDs:
            features.append(inter_data[specObjID]['flux'])
        return np.array(features), np.array(labels)


    def split_data(self, test_size=0.2, random_state=None):
        """Splits the spectral data into training and test sets.

        This method uses the extracted features and labels to create a training set and a test set. The size of the test set is determined by the test_size argument.

        Args:
            test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.2.
            random_state (int, optional): Controls the shuffling applied to the data before applying the split. Defaults to None.

        Returns:
            tuple: A tuple containing the training data split (features and labels) and the test data split (features and labels).
        """
        features, labels = self.get_features_labels()
        return train_test_split(features, labels, test_size=test_size, random_state=random_state)

