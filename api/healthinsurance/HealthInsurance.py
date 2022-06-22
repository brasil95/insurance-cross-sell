import pickle
import numpy as np
import pandas

class HealthInsurance(object):
    def __init__(self):
        self.home_path = 'D:/Users/victor/sejaumdatascientist/04_pa_health_insurance/insurance-cross-sell/'
        self.age_scaler = pickle.load(open(self.home_path + 'parameters/age_scaler.pkl', 'rb'))
        self.annual_premium_scaler = pickle.load(open(self.home_path + 'parameters/annual_premium_scaler.pkl', 'rb'))
        self.policy_sales_channel_scaler = pickle.load(open(self.home_path + 'parameters/policy_sales_channel_scaler.pkl', 'rb'))
        self.region_code_scaler = pickle.load(open(self.home_path + 'parameters/region_code_scaler.pkl', 'rb'))
        self.vintage_scaler = pickle.load(open(self.home_path + 'parameters/vintage_scaler.pkl', 'rb'))
        
    def feature_engineering(self, df2):
        # vehicle_age
        df2['vehicle_age'] = df2['vehicle_age'].apply(lambda x: 'below_1_year' if x == '< 1 Year' else 'between_1_2_years' if x == '1-2 Year' else 'over_2_years')

        # vehicle_damage
        df2['vehicle_damage'] = df2['vehicle_damage'].apply(lambda x: 1 if x == 'Yes' else 0)

        return df2
    
    def data_preparation(self, df5):
        # transformations
        df5['vintage'] = self.vintage_scaler.transform(df5[['vintage']].values)
        df5['annual_premium'] = self.annual_premium_scaler.transform(df5[['annual_premium']].values)
        df5['age'] = self.age_scaler.transform(df5[['age']].values)
        df5.loc[:, 'region_code'] = df5['region_code'].map(self.region_code_scaler)
        df5.loc[:, 'policy_sales_channel'] = df5['policy_sales_channel'].map(self.policy_sales_channel_scaler)
        
        # feature selection
        cols_selected = ['vintage', 'annual_premium', 'age', 'region_code', 'policy_sales_channel', 'vehicle_damage', 'previously_insured']
        
        return df5[cols_selected]
    
    def get_prediction(self, model, original_data, test_data):
        
        # model prediction
        pred = model.predict_proba(test_data)
        
        # join prediction into original data and sort
        original_data['score'] = pred[:, 1].tolist()
        original_data = original_data.sort_values('score', ascending=False)
        
        return original_data.to_json(orient='records', date_format='iso')