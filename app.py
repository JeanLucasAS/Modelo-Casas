from flask import Flask, render_template, request
import joblib
import numpy as np
import os

app = Flask(__name__,
            template_folder='modelo_casas_master/templates',
            static_folder='modelo_casas_master/static')



model = joblib.load(open('modelo_casas.joblib', 'rb')) 

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        try:
            square_footage = float(request.form['Square_Footage'])
            num_bedrooms = int(request.form['Num_Bedrooms'])
            num_bathrooms = int(request.form['Num_Bathrooms'])
            year_built = int(request.form['Year_Built'])
            lot_size = float(request.form['Lot_Size'])
            garage_size = int(request.form['Garage_Size'])
            neighborhood_quality = int(request.form['Neighborhood_Quality'])
        

            features = np.array([[square_footage, num_bedrooms, num_bathrooms, year_built, lot_size, garage_size, neighborhood_quality]])
            price = model.predict(features)
            price = round(price[0], 2)
            formatted_price = f"R${price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


            return render_template('index.html', price=formatted_price)
        except ValueError:
            error_message = "Por favor ingrese valores numéricos válidos."
            return render_template('index.html', error_message=error_message)
        

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)