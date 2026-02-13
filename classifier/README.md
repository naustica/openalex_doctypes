# Document Type Classifier for OpenAlex

## Objective

- Minimise the amount of misclassified research publications in OpenAlex

## Blog Posts

### Scholarly Communication Analytics Blog of SUB Göttingen

- [Identifying journal article types in OpenAlex](https://subugoe.github.io/scholcomm_analytics/posts/oal_document_types_classifier/)

### Open Bibliometrics Blog of the Kompetenznetzwerk Bibliometrie

- [Identifying journal article types in OpenAlex using OPENBIB data](https://open-bibliometrics.de/posts/20250717-DocumentTypeClassifier/)

## Paper 

### Scientometrics

- [Presenting a classifier to improve the identification of research journal publications in OpenAlex](https://doi.org/10.1007/s11192-025-05524-7)

## Data

### Zenodo

Classified data can be found on Zenodo:

Haupka, N., Culbert, J., Donner, P., Jahn, N., Lenke, C., Mayr, P., Meier, A., Mittermaier, B., Scheidt, B., Stahlschmidt, S., & Taubert, N. (2026). 
OPENBIB: Selected curated open metadata based on OpenAlex (0.3) [Data set]. Kompetenznetzwerk Bibliometrie. 
https://doi.org/10.5281/zenodo.18429476

The classified data is licensed under [CCO](https://creativecommons.org/public-domain/cc0/).

## Structure

- [`Classifier.ipynb`](Classifier.ipynb) contains code for training and evaluating the classifier
- [`review_classifier.ipynb`](review_classifier.ipynb) contains large-scale evaluation of the classifier

- [`grid_search.py`](grid_search.py) contains code for optimising parameters 
- [`grid_search_hpc.sh`](grid_search_hpc.sh) contains code for running the grid search process on the HPC of the GWDG Göttingen

- [`train_model.py`](train_model.py) contains code for training the document type classifier
- [`train_model_hpc.sh`](train_model_hpc.sh) contains code for running the training process on the HPC of the GWDG Göttingen

- [`document_types_make_snapshot_openalex.py`](document_types_make_snapshot_openalex.py) contains code for predicting labels on a OpenAlex snapshot
- [`make_snapshot.sh`](make_snapshot.sh) contains code for running predictions on the HPC of the GWDG Göttingen

- [`create_table_oal_doctypes.sql`](create_table_oal_doctypes.sql): SQL statement for producing a table in the KB database
- [`json_posgres_oal_doctypes.sh`](json_posgres_oal_doctypes.sh): Load predictions into the KB infrastructure

- The [`paper/`](paper/) directory contains code used for the journal publication.

## License

Code for the classifier ist licensed under MIT.
