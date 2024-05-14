import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np


df = pd.read_csv('oal_dt_dataset.csv',
                 usecols=['type', 'abstract', 'page', 'author_count',
                          'has_license', 'is_referenced_by_count',
                          'references_count', 'has_funder'],
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
                        'has_funder': int
                  }, nrows=1000000)

def page_counter(page_str):
    page_int = 1
    if '-' in str(page_str):
        try:
            page_int = int(abs(eval(page_str)))
        except:
            pass
        
    return page_int
    
def has_abstract(abstract_str):
    if pd.isna(abstract_str):
        return 0
    else:
        return 1

df['page_count'] = df.page.apply(page_counter)
df['has_abstract'] = df.abstract.apply(has_abstract)

df = df[df['type'] != 'not assigned']
df.drop(['abstract', 'page'], axis=1, inplace=True)
df[['author_count', 'has_license', 'is_referenced_by_count',
    'references_count', 'has_funder', 'page_count', 'has_abstract']] = df[['author_count', 'has_license', 'is_referenced_by_count',
        'references_count', 'has_funder', 'page_count', 'has_abstract']].apply(pd.to_numeric)

df = df.reset_index(drop=True)

X = df[['author_count', 'has_license', 'is_referenced_by_count',
        'references_count', 'has_funder', 'page_count', 'has_abstract']].values
y = df[['type']].values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25)

clf = RandomForestClassifier(n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)
 
param_grid = {
    'n_estimators': [200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [8, 10, 12],
    'criterion' :['gini', 'entropy']
}

cv_rfc = GridSearchCV(estimator=clf, n_jobs=-1, param_grid=param_grid, cv=5)
cv_rfc.fit(X_train, y_train)

print(cv_rfc.best_params_)
