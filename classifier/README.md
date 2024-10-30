# Document Type Classifier for OpenAlex

## Objective

- Minimise the amount of incorrectly classified research publications in OpenAlex

## Blog Post

[Blog Post](https://subugoe.github.io/scholcomm_analytics/posts/oal_document_types_classifier/)

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


