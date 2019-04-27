from datetime import datetime
from datetime import timedelta

from flask import Flask
from flask_restful import Resource, Api, reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

class Ride(Resource):


    def get(self):
        mydb = mysql.connector.connect(
            host="cca498db.csntci1mpxkj.us-east-1.rds.amazonaws.com",
            user="cca498",
            passwd="cca498pass",
            database="yellow_tripdata",
            autocommit=True
        )
        mycursor = mydb.cursor()

        parser = reqparse.RequestParser()
        parser.add_argument("pickup_datetime")
        parser.add_argument("pickup_location")
        parser.add_argument("dropoff_location")
        parser.add_argument("passenger_count")

        args = parser.parse_args()

        # Fetch all car data
        sql = "SELECT id, location, arrival FROM cars"
        mycursor.execute(sql)
        cars = mycursor.fetchall()

        car_id, distance_away = self._find_closest_available_car(int(args['pickup_location']), int(args['dropoff_location']), cars)
        if car_id:
            total_distance = distance_away + abs(int(args['pickup_location'])-int(args['dropoff_location']))
            next_available_at = datetime.utcnow() + timedelta(seconds=total_distance/2)
            next_location = int(args['dropoff_location'])

            update_sql = "UPDATE cars SET location = %s, arrival = %s WHERE id = %s"
            next_available_at.strftime('%Y-%m-%d %H:%M:%S')
            vals = (next_location, next_available_at.strftime('%Y-%m-%d %H:%M:%S'), car_id)
            mycursor.execute(update_sql, vals)
            mydb.commit()
            mycursor.close()
            return {'message': 'Ride reserved', 'ride': car_id, 'location': next_location, 'arrival': next_available_at.strftime('%Y-%m-%d %H:%M:%S')}, 200

        mycursor.close()
        return {'message': 'No rides available', 'args': args}, 200

    def _find_closest_available_car(self, pickup_location, dropoff_location, cars):
        dt_format = '%Y-%m-%d %H:%M:%S'
        closest_car = None
        closest_distance = 9999999999
        for car in cars:
            if car[2] <= datetime.utcnow() and abs(pickup_location-int(car[1])) < closest_distance:
                closest_distance = abs(pickup_location-int(car[1]))
                closest_car = int(car[0])
        return closest_car, closest_distance

    def post(self):
        mydb = mysql.connector.connect(
            host="cca498db.csntci1mpxkj.us-east-1.rds.amazonaws.com",
            user="cca498",
            passwd="cca498pass",
            database="yellow_tripdata"
        )
        mycursor = mydb.cursor()

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
            "improvement_surcharge, total_amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (args["VendorID"],args["tpep_pickup_datetime"],args["tpep_dropoff_datetime"],args["passenger_count"],args["trip_distance"],args["RatecodeID"], \
            args["store_and_fwd_flag"],args["PULocationID"],args["DOLocationID"],args["payment_type"],args["fare_amount"],args["extra"],args["mta_tax"], \
            args["tip_amount"],args["tolls_amount"],args["improvement_surcharge"],args["total_amount"])
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        mycursor.close()
        return {'message':'post success'}, 200

    def put(self):
        return {'message':'put success'}, 200

    def delete(self):
        return {'message':'delete success'}, 200


api.add_resource(Ride,'/ride')





