from flask import Flask , request , render_template , jsonify 
from src.pipeline.prediction_pipeline import CustomData , PredictPipeline

application = Flask(__name__)

app = application 

@app.route('/') 
def home_page() :
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def predict_datapoints():
    if request.method == "GET" :
        return render_template('form.html')
    
    else :
        data=CustomData(
            Delivery_person_Age=float(request.form.get('Delivery_person_Age')),
            Delivery_person_Ratings=float(request.form.get('Delivery_person_Ratings')),
            Restaurant_latitude=float(request.form.get('Restaurant_latitude')),
            Restaurant_longitude=float(request.form.get('Restaurant_longitude')),
            Delivery_location_latitude=float(request.form.get('Delivery_location_latitude')),
            Delivery_location_longitude=float(request.form.get('Delivery_location_longitude')),
            Weather_conditions=request.form.get('Weather_conditions'),
            Road_traffic_density=request.form.get('Road_traffic_density'),
            Vehicle_condition=float(request.form.get('Vehicle_condition')),
            Type_of_order=request.form.get('Type_of_order'),
            Type_of_vehicle=request.form.get('Type_of_vehicle'),
            multiple_deliveries=request.form.get('multiple_deliveries'),
            Festival=request.form.get('Festival'),
            City=request.form.get('City'),
            Day=float(request.form.get('Day')),
            Month=float(request.form.get('Month')),
            Year=float(request.form.get('Year')),
            orderd_hours=float(request.form.get('orderd_hours')),
            orderd_minutes=float(request.form.get('orderd_minutes')),
            picked_hours=float(request.form.get('picked_hours')),
            picked_minutes=float(request.form.get('picked_minutes')),
        )

        final_new_df = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        final_prediction = predict_pipeline.predict(final_new_df)

        result = round(final_prediction[0],2)

        return render_template('result.html' , final_result = result)

if __name__ == "__main__" :
    app.run(debug=True)