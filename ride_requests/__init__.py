from flask import Flask
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

mydb = mysql.connector.connect(
  host="cca498db.csntci1mpxkj.us-east-1.rds.amazonaws.com",
  user="cca498",
  passwd="cca498pass",
  database="yellow_tripdata"
)

mycursor = mydb.cursor()

class RideReplay(Resource):
    def get(self):
        return {'message':'get success'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("VendorID")
        parser.add_argument("tpep_pickup_datetime")
        parser.add_argument("tpep_dropoff_datetime")
        parser.add_argument("passenger_count")
        parser.add_argument("trip_distance")
        parser.add_argument("RatecodeID")
        parser.add_argument("store_and_fwd_flag")
        parser.add_argument("PULocationID")
        parser.add_argument("DOLocationID")
        parser.add_argument("payment_type")
        parser.add_argument("fare_amount")
        parser.add_argument("extra")
        parser.add_argument("mta_tax")
        parser.add_argument("tip_amount")
        parser.add_argument("tolls_amount")
        parser.add_argument("improvement_surcharge")
        parser.add_argument("total_amount")

        args = parser.parse_args()

        sql = "INSERT INTO yellow_tripdata_2018_12 (VendorID, tpep_pickup_datetime, tpep_dropoff_datetime , passenger_count, trip_distance, RatecodeID, "\
            "store_and_fwd_flag, PULocationID, DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, "\
            "improvement_surcharge, total_amount) VALUES (%d,%s,%s,%d,%f,%d,%s,%d,%d,%d,%f,%f,%f,%f,%f,%f,%f)"
        val = (args["VendorID"],args["tpep_pickup_datetime"],args["tpep_dropoff_datetime"],args["passenger_count"],args["trip_distance"],args["RatecodeID"], \
            args["store_and_fwd_flag"],args["PULocationID"],args["DOLocationID"],args["payment_type"],args["fare_amount"],args["extra"],args["mta_tax"], \
            args["tip_amount"],args["tolls_amount"],args["improvement_surcharge"],args["total_amount"])
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        return {'message':'post success'}, 200

    def put(self):
        return {'message':'put success'}, 200
    
    def delete(self):
        return {'message':'delete success'}, 200


api.add_resource(RideReplay,'/ride')





