equilibrator-pathway
====================
[![pipeline status](https://gitlab.com/equilibrator/equilibrator-pathway/badges/master/pipeline.svg)](https://gitlab.com/equilibrator/equilibrator-pathway/commits/master)
[![codecov](https://codecov.io/gl/equilibrator/equilibrator-pathway/branch/master/graph/badge.svg)](https://codecov.io/gl/equilibrator/equilibrator-pathway)
[![PyPI version](https://badge.fury.io/py/equilibrator-pathway.svg)](https://badge.fury.io/py/equilibrator-pathway)
[![conda-forge](https://anaconda.org/conda-forge/equilibrator-pathway/badges/version.svg)](https://anaconda.org/conda-forge/equilibrator-pathway)

Pathway analysis tools based on thermodynamic and kinetic models.
This package can run two different pathway analysis methods:
- Max-min Driving Force (MDF)<sup>1</sup>: 
  objective ranking of pathways by the degree to which their flux is constrained by low thermodynamic driving force.
- [Enzyme Cost Minimization (ECM)](https://www.metabolic-economics.de/enzyme-cost-minimization/)<sup>2, 3</sup>: 
  estimating the specific cost in enzymes for sustaining a flux, given a kinetic model.


## Installation

The easiest way to install equilibrator-pathway is PyPI (and we recommend using a virtual environment):
```
virtualenv -p python3 equilibrator
source equilibrator/bin/activate
pip install equilibrator-pathway
```
or, if you prefer installing with conda:
```
conda install -c conda-forge equilibrator-pathway
```

The following [example Jupyter notebook](https://gitlab.com/equilibrator/equilibrator-pathway/-/tree/develop/examples)
can help you get started.

If you only want to try out MDF or ECM without installing anything locally, we have
a simple web interface for you at [eQuilibrator](http://equilibrator.weizmann.ac.il/pathway/) <sup>4</sup>.


References
----------
1. E. Noor, A. Bar-Even, A. Flamholz, E. Reznik, W. Liebermeister, R. Milo (2014), *Pathway Thermodynamics Highlights Kinetic Obstaclesin Central Metabolism*, PLOS Comp. Biol., [DOI: 10.1371/journal.pcbi.1003483](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3930492/)
2. [https://www.metabolic-economics.de/enzyme-cost-minimization/](https://www.metabolic-economics.de/enzyme-cost-minimization/)
3. E. Noor, A. Flamholz, A. Bar-Even, D. Davidi, R. Milo, W. Liebermeister (2016), *The Protein Cost of Metabolic Fluxes: Prediction from Enzymatic Rate Laws and Cost Minimization*, PLOS Comp. Biol., [DOI: 10.1371/journal.pcbi.1005167](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5094713/)
4. Flamholz, E. Noor, A. Bar-Even, R. Milo (2012) *eQuilibrator - the biochemical thermodynamics calculator*, Nucleic Acids Res, [DOI: 10.1093/nar/gkr874](http://bioinformatics.oxfordjournals.org/content/28/15/2037.long)
