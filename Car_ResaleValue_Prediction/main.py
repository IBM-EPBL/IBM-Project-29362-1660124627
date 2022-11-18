import pandas as pd
import numpy as np
from flask import Flask, render_template, Response, request
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
filename = 'resale_model.sav'
model_rand = pickle.load(open(filename, 'rb'))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/getQuote')
def getQuote():
    brands = np.load('./Data/classesbrand.npy', allow_pickle=True)
    model = np.load('./Data/classesmodel.npy', allow_pickle=True)
    return render_template('UserForm.html', brands=brands, models=model)

@app.route('/y_predict', methods=['GET', 'POST'])
def y_predict():
    regyear1 = request.form['regyear']
    regyear = regyear1[0:4]
    powerps = request.form.get('powerps')
    kms = request.form.get('kms')
    regmonth = regyear1[5:]
    gearbox = request.form.get('gearbox')
    damage = request.form.get('damage')
    model = request.form.get('model')
    brand = request.form.get('brand')
    fuelType = request.form.get('fuel')
    vehicleType = request.form.get('vehicle')
    print(regyear)
    new_row = {'yearOfRegistration': regyear, 'powerPS': powerps, 'kilometer': kms, 'monthOfRegistration': regmonth, 'gearbox':gearbox, 'notRepairedDamage':damage, 'model': model, 'brand': brand, 'fuelType': fuelType, 'vehicleType': vehicleType}
    print(new_row)

    new_df = pd.DataFrame(columns=['vehicleType', 'yearOfRegistration', 'gearbox', 'powerPS', 'model', 'kilometer', 'monthOfRegistration', 'fuelType', 'brand', 'notRepairedDamage'])
    new_df = new_df.append(new_row, ignore_index=True)
    labels = ['gearbox', 'notRepairedDamage', 'model', 'brand', 'fuelType', 'vehicleType']
    mapper = {}
    print(new_df)
    for i in labels:
        mapper[i] = LabelEncoder()
        mapper[i].classes_ = np.load(str('./Data/classes' + i + '.npy'), allow_pickle=True)
        tr = mapper[i].fit_transform(new_df[i])
        new_df.loc[:, i + '_labels'] = pd.Series(tr, index=new_df.index)
    labeled = new_df[['yearOfRegistration', 'powerPS', 'kilometer', 'monthOfRegistration'] + [x + "_labels" for x in labels]]
    X = labeled.values
    print(new_df)
    print(X)
    y_prediction = model_rand.predict(X)
    print(y_prediction)
    return render_template('price.html', y_pred='The Resale Value is {:.2f}$'.format(y_prediction[0]), brand=brand, model=model)

if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=False)