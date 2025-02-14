import pandas as pd
import re
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


df = pd.read_csv('oal_doc_dataset_extended.csv', 
                 names=['doi', 'pm_grouptype', 'type', 'abstract', 'title', 'page', 'author_count',
                          'has_license', 'is_referenced_by_count',
                          'references_count', 'has_funder', 'country_count', 'inst_count', 'has_oa_url'],
                 dtype={'doi': str,
                        'pm_grouptype': str,
                        'type': str,
                        'abstract': str,
                        'title': str,
                        'page': str,
                        'author_count': int,
                        'has_license': int,
                        'is_referenced_by_count': int,
                        'references_count': int,
                        'has_funder': int,
                        'country_count': int,
                        'inst_count': int,
                        'has_oa_url': int
                 }, sep=',', quotechar='"', header=0)

df_publisher = pd.read_csv('datasets/cr_publisher.csv', sep=',')

def page_counter(page_str: str) -> int:
    page_int = 1
    if '-' in str(page_str):
        try:
            page_str = re.sub(r'(\.e)[\d]*', '', page_str)
            page_str = re.sub(r'(\.)[\d]*', '', page_str)
            page_str = re.sub(r'(?<=\d)(e)(\d)*', '', page_str)
            page_str = re.sub('[^\d-]', '', page_str)
            page_int = int(abs(eval(page_str)))
            page_int += 1
        except:
            pass
        
    return page_int
    
def has_abstract(abstract_str: str) -> int:
    if pd.isna(abstract_str):
        return 0
    else:
        return 1

df['page_count'] = df.page.apply(page_counter)
df['has_abstract'] = df.abstract.apply(has_abstract)

df['title_word_length'] = df['title'].str.split().str.len()
df['title_word_length'] = df['title_word_length'].fillna(0)

df = df[df['type'] != 'not assigned']

df['type'] = df['type'].replace(to_replace='research_discourse', value=1)
df['type'] = df['type'].replace(to_replace='editorial_discourse', value=0)

df[['page_count', 
    'has_abstract', 
    'type']] = df[['page_count', 
                   'has_abstract', 
                   'type']].astype(int)

df = df.reset_index(drop=True)

df_with_publisher = df.merge(df_publisher, on=['doi'])
df_pub_n = df_with_publisher.groupby(['publisher'])['doi'].count().reset_index().sort_values(by=['doi'], ascending=False)
df_pub_n.columns = ['publisher', 'n']
df_pub_n = df_pub_n[df_pub_n.n > 5000]
df = df_with_publisher.merge(df_pub_n, on=['publisher'])

X = df[['doi', 'author_count', 'has_license', 'is_referenced_by_count',
        'references_count', 'has_funder', 'page_count', 'has_abstract', 
        'title_word_length', 'inst_count', 'has_oa_url']].values
y = df[['type']].values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    stratify=y, 
                                                    test_size=0.25, 
                                                    random_state=42)

knn = KNeighborsClassifier(n_jobs=-1)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
 
param_grid = {
    'n_neighbors': [40, 45, 50, 55, 60, 100, 200],
    'weights': ['uniform'],
    'algorithm': ['auto'],
    'leaf_size': [30, 40, 50, 100],
    'p': [1]
}

cv_knn = GridSearchCV(estimator=knn, n_jobs=-1, param_grid=param_grid, cv=5)
cv_knn.fit(X_train, y_train)

print(cv_knn.best_params_)
