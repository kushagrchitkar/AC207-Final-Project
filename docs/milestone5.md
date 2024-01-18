# Milestone 5

## API Modifications

In our progress so far, we made improvements to our code organization without necessitating major changes to the API structure. 

Notably, we've eliminated the user class and adopted a more modular approach.

## Reasons for Modifications

Our new structure revolves around a base class, housing essential components such as `__init__.py`, `_prepro.py` for data preprocessing, `_wavelen.py` for wavelength alignment, and `_aug.py` for data augmentation. This modular arrangement allows for a cleaner and more maintainable codebase.

In addition to the base class, we've introduced several specialized classes that run parallel to it:

- `viz.py` (Visualization)
- `ml.py` (Machine Learning)

This reorganization not only streamlines our codebase but also enhances the overall maintainability and readability of our system. By distributing functionalities across these well-defined modules, we've created a more intuitive and scalable structure for our software.
