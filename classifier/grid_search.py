import pandas as pd
import re
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegression


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

df_publisher = pd.read_csv('cr_publisher.csv', sep=',')

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

df['type'] = df['type'].replace(to_replace='research_discourse', value='1')
df['type'] = df['type'].replace(to_replace='editorial_discourse', value='0')
df['type'] = df['type'].astype(int)

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

X = df[['author_count', 'has_license', 'is_referenced_by_count',
        'references_count', 'has_funder', 'page_count', 'has_abstract', 
        'title_word_length', 'inst_count', 'has_oa_url']].values
y = df[['type']].values.ravel()

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)

classifier = LogisticRegression(random_state=42, 
                                n_jobs=-1)
 
param_grid_lr = {
    'penalty': ['l2'],
    'class_weight': ['balanced'],
    'max_iter': [2000, 2500, 3000, 4000]
}

cv_lr = GridSearchCV(estimator=classifier, n_jobs=-1, param_grid=param_grid_lr, cv=5)
cv_lr.fit(X_train, y_train)

print('Best params: LR')
print(cv_lr.best_params_)

clf = RandomForestClassifier(n_jobs=-1, 
                             random_state=42)

param_grid_clf = {
    'criterion': ['gini'],
    'max_depth': [None],
    'max_features': ['sqrt'],
    'class_weight': ['balanced'],
    'n_estimators': [100, 150, 200, 250]
}

cv_clf = GridSearchCV(estimator=clf, n_jobs=-1, param_grid=param_grid_clf, cv=5)
cv_clf.fit(X_train, y_train)

print('Best params: RF')
print(cv_clf.best_params_)

knn = KNeighborsClassifier(n_jobs=-1)

param_grid_knn = {
    'n_neighbors': [20, 40, 50, 60, 100, 200],
    'weights': ['uniform'],
    'algorithm': ['auto'],
    'leaf_size': [20, 30, 40, 50, 100],
    'p': [1]
}

cv_knn = GridSearchCV(estimator=knn, n_jobs=-1, param_grid=param_grid_knn, cv=5)
cv_knn.fit(X_train, y_train)

print('Best params: KNN')
print(cv_knn.best_params_)

abc = AdaBoostClassifier(random_state=42)

param_grid_abc = {
    'n_estimators': [20, 50, 100, 200, 300, 500],
    'algorithm': ['SAMME'],
    'learning_rate': [1]
}

cv_abc = GridSearchCV(estimator=abc, n_jobs=-1, param_grid=param_grid_abc, cv=5)
cv_abc.fit(X_train, y_train)

print('Best params: ABC')
print(cv_abc.best_params_)