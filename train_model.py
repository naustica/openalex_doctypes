import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pickle


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
                  })

def page_counter(page_str):
    page_int = 1
    if '-' in str(page_str):
        try:
            page_int = abs(eval(page_str))
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
df.where(df.author_count <= 5000, 5000, inplace=True)
df.where(df.is_referenced_by_count <= 5000, 5000, inplace=True)
df.where(df.references_count <= 5000, 5000, inplace=True)
df.where(df.page_count <= 5000, 5000, inplace=True)
df[['author_count', 'has_license', 'is_referenced_by_count',
    'references_count', 'has_funder', 'page_count', 'has_abstract']] = df[['author_count', 'has_license', 'is_referenced_by_count',
        'references_count', 'has_funder', 'page_count', 'has_abstract']].apply(pd.to_numeric)

df = df.reset_index(drop=True)

X = df[['author_count', 'has_license', 'is_referenced_by_count',
        'references_count', 'has_funder', 'page_count', 'has_abstract']].values
y = df[['type']].values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.25)

clf = RandomForestClassifier(criterion='gini', 
                             max_depth=10, 
                             max_features='sqrt', 
                             n_estimators=200, 
                             n_jobs=-1,
                             random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred, zero_division=1))

with open('model.pkl', 'wb') as f:
    pickle.dump(clf, f)
