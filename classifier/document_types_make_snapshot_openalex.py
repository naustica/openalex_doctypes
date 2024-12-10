import gzip
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count
import os
import uuid
import pickle
import re


model_path = '/usr/users/haupka/model.pkl'
input_directory = '/scratch/users/haupka/openalex-snapshot/data/works'
output_directory = '/scratch/users/haupka/openalex_document_types'

model_file = open(model_path, 'rb')
model = pickle.load(model_file)

def page_counter(page_str: str) -> int:
    page_int = 1
    if '-' in str(page_str):
        try:
            page_str = re.sub(r'(\.e)[\d]*', '', page_str)
            page_str = re.sub(r'(\.)[\d]*', '', page_str)
            page_str = re.sub(r'(?<=\d)(e)(\d)*', '', page_str)
            page_str = re.sub(r'[^\d-]', '', page_str)
            page_int = int(abs(eval(page_str)))
            page_int += 1
        except:
            pass

    return page_int

def get_label(proba: float) -> bool:
    if proba >= 0.5:
        label = True # 'research_discourse'
        return label
    else:
        label = False # 'editorial_discourse'
        return label


def transform_file(input_file_path: str, output_file_path: str) -> None:
    new_data = []

    with gzip.open(input_file_path, 'r') as file:
        for line in file:

            new_item = json.loads(line)
            if isinstance(new_item, dict):

                source_type = None

                primary_location = new_item.get('primary_location')
                if primary_location:
                    source = primary_location.get('source')
                    if source:
                        source_type = source.get('type')

                item_type = new_item.get('type')
                publication_year = new_item.get('publication_year')


                if source_type == 'journal' and item_type in ['article', 'review'] and publication_year >= 2014:

                    doi = new_item.get('doi')
                    openalex_id = new_item.get('id')
                    authors = new_item.get('authorships')
                    has_license = bool(new_item.get('license'))
                    is_referenced_by_count = new_item.get('cited_by_count')
                    references_works = new_item.get('referenced_works')
                    has_funder = bool(new_item.get('grants'))
                    first_page = new_item.get('biblio').get('first_page')
                    last_page = new_item.get('biblio').get('last_page')
                    issue = new_item.get('biblio').get('issue')
                    is_paratext = bool(new_item.get('is_paratext'))
                    has_abstract = bool(new_item.get('abstract_inverted_index'))
                    title = new_item.get('title')
                    inst_count = new_item.get('institutions_distinct_count')
                    has_oa_url = bool(new_item.get('open_access').get('is_oa'))

                    if doi:
                        doi = doi.lstrip('https://doi.org/')
                    
                    if authors:
                        author_count = len(authors)
                    else:
                        author_count = 0
    
                    if references_works:
                        references_count = len(references_works)
                    else:
                        references_count = 0
    
                    if first_page:
                        if last_page:
                            page_count = page_counter(str(first_page) + '-' + str(last_page))
                        else:
                            page_count = page_counter(str(first_page))
                    else:
                        page_count = 1
                    
                    if title:
                        title_word_length = len(title.split())
                    else:
                        title_word_length = 0
    
                    if not inst_count:
                        inst_count = 0
                        
                    
                    probas = model.predict_proba([[int(author_count),
                                                   int(has_license),
                                                   int(is_referenced_by_count),
                                                   int(references_count),
                                                   int(has_funder),
                                                   int(page_count),
                                                   int(has_abstract),
                                                   int(title_word_length),
                                                   int(inst_count),
                                                   int(has_oa_url)]])
    
                    proba = probas[:, 1][0]

                    if issue:
                        issue = str(issue)
                        # credits to https://compareopenalexanddimensions.streamlit.app
                        if 'sup' in issue.lower() or 'meet' in issue.lower():
                            proba = 0.0

                    if is_paratext:
                        proba = 0.0
    
                    label = get_label(proba)
    
                    new_data.append(dict(openalex_id=openalex_id, 
                                         doi=doi,
                                         is_research=label, 
                                         proba=proba))

        write_file(new_data, output_file_path)


def write_file(data, output_file_path: str) -> None:

    with gzip.open(output_file_path, 'w') as output_file:
        result = [json.dumps(record, ensure_ascii=False).encode('utf-8') for record in data]
        for line in result:
            output_file.write(line + bytes('\n', encoding='utf8'))


def transform_snapshot(max_workers: int = cpu_count()) -> None:
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        for directory in os.listdir(input_directory):
            if os.path.isdir(input_directory + '/' + directory):
                os.makedirs(output_directory + '/' + directory, exist_ok=True)
                for input_file in os.listdir(input_directory + '/' + directory):
                    output_file_path = os.path.join(output_directory + '/' + directory + os.path.basename(input_file) + 'l.gz')
                    future = executor.submit(transform_file,
                                             input_file_path=input_directory + '/' + directory + '/' + input_file,
                                             output_file_path=output_file_path)
                    futures.append(future)

        for future in as_completed(futures):
            future.result()


transform_snapshot()
