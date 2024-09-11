unpigz -c -p 8 openalex_document_types/*.gz | parallel --pipe --jobs 8 --recend '}\n' "jq -c '{openalex_id: .openalex_id, doi: .doi, label: .label, proba: .proba}' | spyql -Otable=classification_article_reviews_august_2024 'IMPORT json AS js SELECT json->openalex_id, json->doi, json->label, json->proba FROM json TO sql' | psql postgresql://$KB_USERNAME:$KB_PASSWORD@biblio-p-db03.fiz-karlsruhe.de:6432/kbprod"

