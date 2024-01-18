# Milestone 4: Software Organization and Licensing 

## Directory/Test Suite Structure
```
API_project_root/
│
├── README.md
├── LICENSE
├── AC207_Mileston 2.pdf
├── .github/
│   ├── workflows/
│       ├── coverage.yml
│       └──test.yml
├── .gitignore
├── API_draft/
│   ├── APIdiagram
│   └── README.md
├── code/
│   ├── baseclass/
│       ├── __init__.py
│       ├── _prepro.py
│       ├── _wavelen.py
│       └── _aug.py
│   ├── viz.py
│   ├── ml.py
│   └── spectral.py
├── tests/
│   ├── test1.py
│   ├── test2.py
│   └── ...
├── docs/
│   ├── milestone4.md
│   ├── doc1
│   └── ...

```


## Package Distribution

We have decided to distribute the package via PyPI. 

## Other Considerations

Our implementation expects the client to only interact with the public class `SpectralData`, which is a child class of our base class `Extractor`. The `Extractor` base class contains private methods to carry out individual tasks. It also imports additional modules for preprocessing, wavelength alignment, and data augmentation. Additional modules for visualization and machine learning also use the `Extractor` base class.

## License Choice

We used the GNU General Public License, a copyleft license, as guided in the Software Development Agreement. The contract can be found in the root of our directory, named `LICENSE.txt`.
