import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


df = pd.read_csv('oal_dt_dataset.csv', 
                 names=['doi', 'pm_grouptype', 'type', 'abstract', 
                        'title', 'page', 'author_count',
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
                 }, sep=',', quotechar='"', header=0)

def page_counter(page_str):
    page_int = 1
    if '-' in str(page_str):
        try:
            page_int = int(abs(eval(page_str)))
            if page_int > 1000:
                page_int = 1000
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

df['title_word_length']  = df['title'].str.split().str.len()
df['abstract_word_length']  = df['abstract'].str.split().str.len()
df['title_string_length']  = df['title'].str.len()
df['abstract_string_length']  = df['abstract'].str.len()

df['title_string_length'] = df['title_string_length'].fillna(0)
df['abstract_string_length'] = df['abstract_string_length'].fillna(0)
df['title_word_length'] = df['title_word_length'].fillna(0)
df['abstract_word_length'] = df['abstract_word_length'].fillna(0)

df = df[df['type'] != 'not assigned']
df.drop(['pm_grouptype', 'abstract', 'page'], axis=1, inplace=True)

df['type'] = df['type'].replace(to_replace='research_discourse', value=1)
df['type'] = df['type'].replace(to_replace='editorial_discourse', value=0)

df[['page_count', 
    'has_abstract', 
    'title_string_length', 
    'abstract_string_length',
    'title_word_length', 
    'abstract_word_length', 
    'type']] = df[['page_count', 
                   'has_abstract', 
                   'title_string_length', 
                   'abstract_string_length', 
                   'title_word_length', 
                   'abstract_word_length', 
                   'type']].astype(int)

df = df.reset_index(drop=True)

X = df[['author_count', 'has_license', 'is_referenced_by_count',
        'references_count', 'has_funder', 'page_count', 
        'has_abstract', 'title_string_length', 
        'abstract_string_length', 'title_word_length', 
        'abstract_word_length']].values
y = df[['type']].values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    stratify=y, 
                                                    test_size=0.25, 
                                                    random_state=42)

clf = RandomForestClassifier(n_jobs=-1, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print(classification_report(y_test, 
                            y_pred, 
                            zero_division=1, 
                            target_names=['editorial_discourse', 'research_discourse']))
 
param_grid = {
    'n_estimators': [200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [8, 10, 12],
    'criterion' :['gini', 'entropy']
}

cv_rfc = GridSearchCV(estimator=clf, n_jobs=-1, param_grid=param_grid, cv=5)
cv_rfc.fit(X_train, y_train)

print(cv_rfc.best_params_)
