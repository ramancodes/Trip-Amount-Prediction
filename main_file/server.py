from flask import Flask, render_template, request
# complete this page with a new template
from Model import predictionModel
from datetime import datetime

mod = predictionModel()
app = Flask(__name__)

def getCurrentDate():
    now = datetime.now()
    current = now.date()
    date = str(current)
    return date

def getDay(date):
    d = datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
    pos = d.weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days[pos]

# if the string contains any integer
def has_num(s):
    return any(i.isdigit() for i in s)


@app.route('/')
def home(): 
    return render_template('index.html')


@app.route('/roadways', methods =["GET", "POST"])
def getRoadwaysdetails():
    data = []
    if request.method=='POST':
        source = request.form.get('src').capitalize()
        destination = request.form.get('dest').capitalize()
        v_type = int(request.form.get('road_vechile_type'))

        #check the places name 
        if not has_num(source) and not has_num(destination):
            try:
                distance = mod.getDistance(source=source, destination=destination)
                pos=source.find(',')
                if pos!=-1:
                    source=source[:pos]
                pos=destination.find(',')
                if pos!=-1:
                    destination=destination[:pos]
                data=[v_type, source, destination, distance]
                try:
                    model_fare = round(mod.predictFare(data), 2)
                    data.append(model_fare)
                    print(data)
                except:
                    data = [-1, 'Model Error']
            except:
                data = [-1, 'Distance Error: Enter Valid Source And Destination / Connection Error']
        else:
            data = [-1, 'Name Error: Enter Valid Source And Destination']
            
    return render_template('roadways.html', data=data)


@app.route('/flight', methods =["GET", "POST"])
def getFlightdetails():
    data = []
    currentDate = getCurrentDate()
    if request.method=='POST':
        source = request.form.get('src').capitalize()
        destination = request.form.get('dest').capitalize()
        if not has_num(source) and not has_num(destination):
            pos=source.find(',')
            if pos!=-1:
                source=source[:pos]
            pos=destination.find(',')
            if pos!=-1:
                destination=destination[:pos]
            date = request.form.get('dateInput')
            day = getDay(date)
            airline = request.form.get('airline')
            seat_type = request.form.get('seat_type')
            stops = request.form.get('stops')
            flight_code = request.form.get('flight_code')
            departure = request.form.get('departure_time')
            arrival = request.form.get('arrival_time')
            duration = float(request.form.get('duration'))
            data=[3, date, day, airline, seat_type, source, destination, stops, flight_code, departure, arrival, duration]
            try:
                print(data)
                model_fare = round(mod.predictFare(data), 2)
                data = [3, source, destination, model_fare]
            except:
                print(data)
                data = [-1, 'Model Error']
            print(data)
        else:
            data = [-1, 'Name Error: Enter Valid Source And Destination']
            
    return render_template('flight.html', data=data, currentDate=currentDate)

@app.route('/train', methods =["GET", "POST"])
def getTraindetails():
    data = []
    currentDate = getCurrentDate()
    if request.method=='POST':
        source = request.form.get('src')
        destination = request.form.get('dest')
        if not has_num(source) and not has_num(destination):
            pos=source.find(',')
            if pos!=-1:
                source=source[:pos]
            pos=destination.find(',')
            if pos!=-1:
                destination=destination[:pos]
            date = request.form.get('dateInput')
            day = getDay(date)
            seat_type = request.form.get('seat_type')
            departure = request.form.get('departure_time')
            arrival = request.form.get('arrival_time')
            data=[4, date, day, seat_type, source, destination, departure, arrival]
            try:
                print(data)
                model_fare = round(mod.predictFare(data), 2)
                data = [4, source, destination, model_fare]
            except:
                print(data)
                data = [-1, 'Model Error']
            print(data)
        else:
            data = [-1, 'Name Error: Enter Valid Source And Destination']
            
    return render_template('train.html', data=data, currentDate=currentDate)

if __name__ == "__main__":
    app.run(debug=True)


