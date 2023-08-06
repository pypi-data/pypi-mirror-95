# slacki

[![Python](https://img.shields.io/pypi/pyversions/slacki)](https://img.shields.io/pypi/pyversions/slacki)
[![PyPI Version](https://img.shields.io/pypi/v/slacki)](https://pypi.org/project/slacki/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/slacki/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/slacki)](https://pepy.tech/project/slacki)
[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)

	Star it if you like it!

* Slacki is Python package for reading and posting in slack groups.

### Contents
- [Installation](#-installation)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

### Installation
* Install slacki from PyPI (recommended). slacki is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* A new environment can be created as following:

```python
conda create -n env_slacki python=3.7
conda activate env_slacki
```

```bash
pip install slacki
```

* Alternatively, install slacki from the GitHub source:
```bash
# Directly install from github source
pip install -e git://github.com/erdogant/slacki.git@0.1.0#egg=master
pip install git+https://github.com/erdogant/slacki#egg=master

# By cloning
pip install git+https://github.com/erdogant/slacki
git clone https://github.com/erdogant/slacki.git
cd slacki
python setup.py install
```  

#### Import slacki package
```python
from slacki import slacki
```

#### Example:
```python

# Import library
from slacki import slacki

from slacki import slacki
sc = slacki(channel='new_channel', token='xoxp-123234234235-123234234235-123234234235-adedce74748c3844747aed48499bb')

# Get some info about the channels
channels = sc.get_channels()

# Get some info about the users
users = sc.get_users()

# Send messages
queries=['message 1','message 2']
sc.post(queries)

# Snoozing
sc.snooze(minutes=1)

# Post file
sc.post_file(file='./data/slack.png', title='Nu ook met figuren uploaden :)')

# listen (retrieve only last message)
out = sc.retrieve_posts(n=3, retrieve_names=True)

```


#### Citation
Please cite slacki in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2020slacki,
  title={slacki},
  author={Erdogan Taskesen},
  year={2020},
  howpublished={\url{https://github.com/erdogant/slacki}},
}
```

#### References
* https://github.com/erdogant/slacki

### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* Contributions are welcome.
* If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated :)
