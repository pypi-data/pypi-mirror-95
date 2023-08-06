# Welcome to Ketos, a deep learning package for underwater acoustics

Ketos provides a unified, high-level interface for working with acoustic data and deep neural networks. 
Its main purpose is to support the development of deep learning models for solving challenging 
detection and classification problems in underwater acoustics.

Ketos is written in Python and utilizes a number of powerful software packages 
including NumPy, HDF5, and Tensorflow. It is licensed under the [GNU GPLv3 licens](https://www.gnu.org/licenses/) 
and hence freely available for anyone to use and modify. The project is hosted on GitLab at 
[gitlab.meridian.cs.dal.ca/public_projects/ketos](https://gitlab.meridian.cs.dal.ca/public_projects/ketos). 
For more information, please consult [Ketos' Documentation Page](https://docs.meridian.cs.dal.ca/ketos/).

Ketos was developed by the [MERIDIAN](http://meridian.cs.dal.ca/) Data Analytics Team at the 
[Institute for Big Data Analytics](https://bigdata.cs.dal.ca/) at Dalhousie University. 
We are greatful to Amalis Riera and Francis Juanes at the University of Victoria, 
Kim Davies and Chris Taggart at Dalhousie University, and Kristen Kanes at Ocean Networks Canada 
for providing us with annotated acoustic data sets, which played a key role in the development work.
The first version of Ketos was released in April 2019. 

The intended users of Ketos are primarily researchers and data scientists working with (underwater) acoustics data. 
While Ketos comes with complete documentation and comprehensive step-by-step tutorials, some familiarity with 
Python and especially the NumPy package would be beneficial. A basic understanding of 
the fundamentals of machine learning and neural networks would also be an advantage.

The name Ketos was chosen to highlight the package's main intended application, underwater acoustics.
In Ancient Greek, the word ketos denotes a large fish, whale, shark, or sea monster. The word ketos 
is also the origin of the scientific term for whales, cetacean.


## Installation

Ketos is available on the Python package index repository and the latest version can be installed with pip:

   ```bash 
   pip install ketos
   ``` 

Because Ketos uses TensorFlow as the deep learning framework, at this time it requires pip 20.0 or higher and python 3.6 or 3.7.

Note that GPU support depends on CUDA enabled graphics cards and the necessary drivers and libraries. 
Refer to  https://www.tensorflow.org/install/gpu for more information further instructions.


Depending on your operating system, you might have to install other dependencies (like hdf5lib).
If you try the steps above and receive errors due to missing dependencies and don't want to install them yourself, you might find Anaconda helpful. 

Anaconda is freely available from [docs.anaconda.com/anaconda/install](https://docs.anaconda.com/anaconda/install/). 
Make sure you get the Python 3.7 version and make sure to pick the installer appropriate for your OS (Linux, macOS, Windows) 

 1. Create and activate a new Anaconda environment:
    ```bash
    conda create --name ketos_env
    conda activate ketos_env
    ```

 2. Install the pip package manager and Jupyter Notebook:
    ```bash
    conda install pip
    conda install jupyter #if you want to run the executable jupyter notebooks in the tutorials 
    ```

 3. Install the latest version of Ketos:
    ```bash
    pip install ketos
    ```

## Jupyter notebook tutorials

 * [Creating a training database (Basic)](docs/source/tutorials/create_database_simpler/create_database_simpler.ipynb)
 * [Creating a training database (Extended)](docs/source/tutorials/create_database/create_database.ipynb)
 * [Training a ResNet classifier](docs/source/tutorials/train_a_narw_classifier/train_a_narw_classifier_part_1.ipynb)
