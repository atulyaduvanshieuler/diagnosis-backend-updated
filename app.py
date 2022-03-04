#TODO: Add timout in multiprocessing for collecting data
import time
from flask import Flask, request, jsonify, send_file
from testing_module import test_all_parts
from testing_module import test_bms
from testing_module import test_controller
from testing_module import test_stark
from testing_module import collect_can_data
from testing_module import parse_can_data
import multiprocessing
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)

can_data_collection_process = multiprocessing.Process(target=collect_can_data)
#print(test_all_parts())

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/testall", methods=["GET", "POST"])
def run_tests():
    if request.method == "GET":
        res = test_all_parts()
        res = jsonify(res)
        return res


@app.route("/testbms", methods=["GET", "POST"])
def run_bms_test():
    if request.method == "GET":
        res = test_bms()
        res = jsonify(res)
        return res


@app.route("/testcontroller", methods=["GET", "POST"])
def run_controller_test():
    if request.method == "GET":
        res = test_controller()
        res = jsonify(res)
        return res


@app.route("/teststark", methods=["GET", "POST"])
def run_stark_test():
    if request.method == "GET":
        res = test_stark()
        res = jsonify(res)
        return res
        
@app.route("/collectcandata", methods=["GET", "POST"])
def collect_can_data():
    if request.method == "GET":
        global can_data_collection_process
        can_data_collection_process.start()

@app.route("/sendcandata", methods=["GET", "POST"])
def send_can_data():
    if request.method == "GET":
        global can_data_collection_process
        can_data_collection_process.stop()
        time.sleep(1)
        parse_can_data()
        time.sleep(1)
        csv_file = "testing_module/can_data_collection_and_parsing/parsed_can_data.csv"
        return send_file(csv_file)

 
