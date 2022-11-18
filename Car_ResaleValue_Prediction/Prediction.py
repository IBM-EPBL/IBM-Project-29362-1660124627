import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score, train_test_split

df = pd.read_csv("Data/autos.csv", header=0, sep=',', encoding='Latin1')

df = df[df.seller != 'gewerblich']
df = df.drop('seller', 1)

df = df[df.offerType != 'Gesuch']
df = df.drop('offerType', 1)

df = df[(df.powerPS > 50) & (df.powerPS < 900)]
df = df[(df.yearOfRegistration > 1950) & (df.yearOfRegistration < 2017)]

df.drop(['name', 'abtest', 'dateCrawled', 'nrOfPictures', 'lastSeen', 'postalCode', 'dateCreated'], axis='columns', inplace=True)

new_df = df.copy()
new_df = new_df.drop_duplicates(['price', 'vehicleType', 'yearOfRegistration', 'gearbox', 'powerPS', 'model', 'kilometer', 'monthOfRegistration', 'fuelType', 'notRepairedDamage'])

new_df.gearbox.replace (('manuell', 'automatik'), ('manual', 'automatic'),inplace=True)
new_df.fuelType. replace (('benzin', 'andere', 'elektro'), ('petrol', 'others', 'electric'),inplace=True)
new_df.vehicleType.replace(('kleinwagen', 'cabrio', 'kombi', 'andere'), ('small car', 'convertible', 'combination', 'others'), inplace=True)
new_df.notRepairedDamage.replace(('ja', 'nein'), ('Yes', 'No'), inplace=True)

new_df = new_df[(new_df.price >= 100) & (new_df.price <= 150000)]

new_df['notRepairedDamage'].fillna(value='not-declared', inplace=True)
new_df['fuelType'].fillna(value='not-declared', inplace=True)
new_df['gearbox'].fillna(value='not-declared', inplace=True)
new_df['vehicleType'].fillna(value='not-declared', inplace=True)
new_df['model'].fillna(value='not-declared', inplace=True)

new_df.to_csv("autos_preprocessed.csv")

labels = ['gearbox', 'notRepairedDamage', 'model', 'brand', 'fuelType', 'vehicleType']

mapper = {}
for i in labels:
    mapper[i] = LabelEncoder()
    mapper[i].fit(new_df[i])
    tr = mapper[i].transform(new_df[i])
    np.save(str('classes'+i+'.npy'), mapper[i].classes_)
    new_df.loc[:, i + '_labels'] = pd.Series(tr, index=new_df.index)
print('mapper', mapper)
labeled = new_df[['price', 'yearOfRegistration', 'powerPS', 'kilometer', 'monthOfRegistration'] + [x+"_labels" for x in labels]]
print(labeled.columns)
Y = labeled.iloc[:, 0].values
X = labeled.iloc[:, 1:].values

Y = Y.reshape(-1, 1)


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=3)

