# Analysis of the Publication and Document Types in OpenAlex, Web of Science, Scopus, Pubmed and Semantic Scholar

## Overview

This repository contains code used for the journal publications:

Haupka, N., Culbert, J., Schniedermann, A., Jahn, N., Mayr, P. (2025). 
Analysis of the Publication and Document Types in OpenAlex, Web of Science, Scopus, Pubmed and Semantic Scholar. Quantitative Science Studies. 

[https://doi.org/10.1162/QSS.a.406](https://doi.org/10.1162/QSS.a.406)

Haupka, N. (2026). 
Presenting a classifier to improve the identification of research journal publications in OpenAlex. Scientometrics. 

[https://doi.org/10.1007/s11192-025-05524-7](https://doi.org/10.1007/s11192-025-05524-7)

## Analysis

- [`Codebook.ipynb`](Codebook.ipynb) contains the exploratory analysis of publication and document types
- [`Characteristics.ipynb`](Characteristics.ipynb) contains the analysis of document types based on shared corpus

- The [`queries/`](queries/) directory contains all SQL queries that were used during the analysis.
- The [`media/`](media/) directory contains all images that were used for comparison.

- The [`classifier/`](classifier/) directory contains code used for the OpenAlex document type classifier.

## License

Code for the classifier is licensed under the MIT license.

Classified data is available via Zenodo and licensed under [CCO](https://creativecommons.org/public-domain/cc0/):

Haupka, N., Culbert, J., Donner, P., Jahn, N., Lenke, C., Mayr, P., Meier, A., Mittermaier, B., Scheidt, B., Stahlschmidt, S., & Taubert, N. (2026). 
OPENBIB: Selected curated open metadata based on OpenAlex (0.3) [Data set]. Kompetenznetzwerk Bibliometrie. 
https://doi.org/10.5281/zenodo.18429476

## Acknowledgment

This work was funded by the Federal Ministry of Education and Research (grant funding number: 16WIK2301B / 16WIK2301E, The OpenBib project; grant funding number: 01PU17017, The FuReWiRev project). We acknowledge the support from the Federal Ministry of Education and Research, Germany under grant number 01PQ17001, the Competence Network for Bibliometrics.

## Contact

Nick Haupka, SUB Göttingen. nick.haupka@sub.uni-goettingen.de
