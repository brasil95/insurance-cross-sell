import pickle
import os
import pandas as pd
from flask import Flask, request, Response
from healthinsurance.HealthInsurance import HealthInsurance

# load model in memory
model = pickle.load(open('D:/Users/victor/sejaumdatascientist/04_pa_health_insurance/insurance-cross-sell/models/model_insurance_lr.pkl', 'rb'))

# initialize API
app = Flask(__name__)

# create endpoint
@app.route('/crosssell/predict', methods=['POST'])
def health_insurance_predict():
    test_json = request.get_json()

    if test_json: #there is data
        if isinstance(test_json, dict): #unique row
            test_raw = pd.DataFrame(test_json, index = [0])
        else: # multiple rows
            test_raw = pd.DataFrame(test_json, columns = test_json[0].keys())

        #needed cause test_raw will be overwritten on pipeline
        test_raw_original = test_raw.copy()

        # instantiate HealthInsurance class
        pipeline = HealthInsurance()

        # feature engineering
        df1 = pipeline.feature_engineering(test_raw)

        # data preparation
        df2 = pipeline.data_preparation(df1)

        # prediction
        df_response = pipeline.get_prediction(model, test_raw_original, df2)

        #returns a json
        return df_response

    else: #if empty:
        return Response('{}', status = 200, mimetype = 'application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run( host='192.168.15.50', port=port )