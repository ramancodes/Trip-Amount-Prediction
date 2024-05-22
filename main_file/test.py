# working with the dataframe
import pandas as pd
# saving and loading the saved models
import joblib
# filtering and avoiding the warnings
import warnings
warnings.filterwarnings("ignore")
# manipulating the string/object data to labels
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
# access the google distnace matrix
import requests

class predictionModel:
    def __init__(self):
        Road_Petrol_Filename = "Road_Petrol_Model.pkl"
        Road_Diesel_Filename = "Diesel_Model.pkl"
        Road_CNG_Filename = "CNG_Model.pkl"
        Flight_Filename = "Flight_Model.pkl"
        Train_Filename = "Train_Model.pkl"
        self.petrol_model = joblib.load(Road_Petrol_Filename)
        self.diesel_model = joblib.load(Road_Diesel_Filename)
        self.cng_model = joblib.load(Road_CNG_Filename)
        self.flight_model = joblib.load(Flight_Filename)
        self.train_model = joblib.load(Train_Filename)

    def __transformColumns(self, df):
        for i in df.columns:
            if df[i].dtype == 'object':
                df[i]=le.fit_transform(df[i])
        return df

    def getDistance(self, data):
        # distance matrix
        api_key = 'AIzaSyBxBIQwFcFFYQcUh8gWM2cyhUwfcEdlWHQ'
        origin = data[1].replace(' ', '%20')
        destination = data[2].replace(' ', '%20')
        distance_url = f'https://maps.googleapis.com/maps/api/distancematrix/json?destinations={destination}&origins={origin}&key={api_key}'
        distance_response = requests.get(url=distance_url)
        self.distance = distance_response.json()['rows'][0]['elements'][0]['distance']['value']/1000
        return self.distance

    def __createDataframe(self, data):
        new_data = {}
        if data[0]==0 or data[0]==1 or data[0]==2:
            new_data={'Source':[data[1]],'Destination':[data[2]], 'Distance':[data[3]]}
        elif data[0]==3:
            new_data={'Date_of_journey':[data[1]],'Journey_day':[data[2]], 'Airline':[data[3]], 'Class':[data[4]], 'Source':[data[5]] ,'Destination':[data[6]], 'Total_stops':[data[7]],'Flight_code':[data[8]],'Departure':[data[9]] ,'Arrival':[data[10]] ,'Duration_in_hours':[data[11]]}
        elif data[0]==4:
            new_data={'Date_of_journey':[data[1]],'Journey_day':[data[2]], 'Class':[data[3]], 'Source':[data[4]] ,'Destination':[data[5]],'Departure':[data[6]],'Arrival':[data[7]]}
        df = pd.DataFrame(new_data)
        df = self.__transformColumns(df)
        return df

    def __selectModel(self, type):
        model = self.petrol_model
        match type:
            case 1:
                model = self.diesel_model
            case 2:
                model = self.cng_model
            case 3:
                model = self.flight_model
            case 4:
                model = self.train_model
        return model

    def predictFare(self, data):
        df = self.__createDataframe(data)
        model = self.__selectModel(data[0])
        res=model.predict(df)
        return res[0]
    
beg = predictionModel()
# new_data=[3, '2024-06-15','Friday','SpiceJet','Economy','Ranchi','Delhi','non-stop','SG','Morning','Afternoon',2]
new_data = [3, '2024-05-31', 'Friday', 'GO FIRST', 'Business', 'Delhi', 'Roorkee', '1-stop', 'I5', 'Early Morning', 'Morning', 2.0]
print(beg.predictFare(new_data))