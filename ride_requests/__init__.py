from flask import Flask
from flask_restful import Resource, Api
import mysql.connector

app = Flask(__name__)
api = Api(app)

mydb = mysql.connector.connect(
  host="172.20.10.2",
  user="cca498mysql",
  passwd="cca498dbpass",
  database="yellow_tripdata"
)

mycursor = mydb.cursor()

class RideReplay(Resource):
    def get(self):
        return {'message':'get success'}, 200

    def post(self):
        sql = "INSERT INTO yellow_tripdata_2018_12 (VendorID, tpep_pickup_datetime, tpep_dropoff_datetime , passenger_count, trip_distance, RatecodeID, "\
            "store_and_fwd_flag, PULocationID, DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, "\
            "improvement_surcharge, total_amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = ("1","2018-12-01 00:28:22","2018-12-01 00:44:07","2","2.50","1","N","148","234","1","12","0.5","0.5","3.95","0","0.3","17.25")
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        return {'message':'post success'}, 200

    def put(self):
        return {'message':'put success'}, 200
    
    def delete(self):
        return {'message':'delete success'}, 200


api.add_resource(RideReplay,'/ride')



users = [
    {
        "name":"Gayan",
        "age": 30,
        "occupation": "software engineer"
    },
    {
        "name":"Supun",
        "age": 32,
        "occupation":"Doctor"
    }
]




