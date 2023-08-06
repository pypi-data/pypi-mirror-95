# tsdate <img align="right" width="145" height="90" src="https://github.com/tskit-dev/tsdate/blob/master/docs/_static/tsdate_logo.svg">

[![CircleCI](https://circleci.com/gh/tskit-dev/tsdate.svg?style=svg)](https://circleci.com/gh/tskit-dev/tsdate)
[![codecov](https://codecov.io/gh/tskit-dev/tsdate/branch/master/graph/badge.svg)](https://codecov.io/gh/tskit-dev/tsdate)
[![Documentation Status](https://readthedocs.org/projects/tsdate/badge/?version=latest)](https://tsdate.readthedocs.io/en/latest/?badge=latest)

``tsdate`` is a scalable method for estimating the age of ancestral nodes in a 
[tree sequence](https://www.youtube.com/watch?v=X1GEuQrF1jQ). The method uses a coalescent prior and updates node times on the basis of the number of mutations along each edge of the tree sequence (i.e. using the "molecular clock").

The method is designed to operate on the output of [tsinfer](https://tsinfer.readthedocs.io/en/latest/), which efficiently infers tree sequence *topologies* from large genetic datasets.

Please refer to the [documentation](https://tsdate.readthedocs.io/en/latest/) for information on installing and using the software.

