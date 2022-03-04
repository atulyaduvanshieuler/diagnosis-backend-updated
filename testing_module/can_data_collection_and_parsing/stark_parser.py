from datetime import datetime

"""
The relative order within the characters remains the same but order of string(in pair) gets reversed
Ex ==>> B7370000 -> 000037B7
"""

reverse_string_in_pair = lambda string: "".join(
    reversed([string[idx : idx + 2] for idx in range(0, len(string), 2)])
)

check_is_battery_latched = lambda string: convert_and_get_desired_value(string) == 1


hex_to_bin = lambda string: bin(int(string, 16))


def convert_and_get_temperature(string, roundabout=None):
    if not roundabout:
        roundabout = 0
    assert isinstance(roundabout, int), "`roundabout` value should be integer"
    temperature = int(string, 16) - roundabout
    return float(format(temperature, ".1f"))



def convert_and_get_temperatures(string):
    temp = ""
    temperatures = []
    for idx, _str in enumerate(string):
        temp += _str
        if idx % 2:
            temperatures.append(convert_and_get_temperature(temp))
            temp = ""
    return temperatures


def convert_and_get_current_val(string):
    new_string = reverse_string_in_pair(string)
    if new_string[0:2] == "FF":
        current = (
            int(hex(int("100000000", 16) - int(new_string, 16)), 16) / 1000
        ) * 0.01
        current *= -1
    else:
        current = (int(new_string, 16) / 1000) * 0.01
    return float(format(current, ".1f"))
    


def convert_and_get_desired_value(string, multiplier=None):
    string = reverse_string_in_pair(string)
    if not multiplier:
        multiplier = 1.0
    req = int(string, 16) * multiplier
    return float(format(req, ".1f"))



def convert_and_handle_negative_values(string, multiplier=None):
    new_string = reverse_string_in_pair(string)
    if new_string[0:2] == "FF":
        val = int("FFFF", 16) - int(new_string, 16)
        if multiplier:
            val *= multiplier
    else:
        val = convert_and_get_desired_value(string, multiplier=multiplier)

    return float(format(val, ".2f"))



def handle_datetime(date, time):
    request_date = datetime.strptime(date, "%y%m%d")
    request_time = datetime.strptime(time, "%H%M%S")
    request_date = request_date.replace(
        hour=request_time.hour, minute=request_time.minute, second=request_time.second
    )
    return request_date


def stark_parser_function(can_id, can_data):
    bmsData = {}

    ControllerDATA = {}
    response={}
    if can_data:
    
        can_data = can_data.rjust(16, "0")

        if can_id == "110":
            try:
                bmsData["balancingLimit"] = convert_and_get_desired_value(
                    string=can_data[:4], multiplier=0.1
                )

                bmsData["prechargeActive"] = convert_and_get_desired_value(
                    string=can_data[4:6]
                )

                bmsData["balancingActive"] = convert_and_get_desired_value(
                    string=can_data[6:8]
                )

                bmsData["Pack_I_Master"] = convert_and_get_desired_value(
                    string=can_data[8:], multiplier=0.01
                )
                response["BMS Balancing Limit"] = bmsData["balancingLimit"]
                response["BMS Pre charge Active"] = bmsData["prechargeActive"]
                response["BMS Balancing active"] =  bmsData["balancingActive"]
                response["bms pack i master"] = bmsData["Pack_I_Master"]

            except ValueError:
                bmsData["balancingLimit"] = bmsData["prechargeActive"] = bmsData[
                    "balancingActive"
                ] = bmsData["Pack_I_Master"] = 0

        elif can_id == "111":
            try:
                bmsData["Pack_Q_SOC_Trimmed"] = convert_and_get_desired_value(
                    string=can_data[0:4], multiplier=0.01
                )
                bmsData["SOH"] = convert_and_get_desired_value(
                    string=can_data[4:8], multiplier=0.01
                )
                bmsData["BMSStatus"] = convert_and_get_desired_value(
                    string=can_data[8:10]
                )
                bmsData["FullyChargeFlag"] = check_is_battery_latched(
                    string=can_data[10:12]
                )
                bmsData["Pack_V_Sum_of_Cells"] = convert_and_get_desired_value(
                    string=can_data[12:], multiplier=0.1
                )

                response["BMS Pack_Q_SOC_Trimmed"] = bmsData["Pack_Q_SOC_Trimmed"]
                response["BMS SOH"] = bmsData["SOH"]
                response["BMS BMSStatus"] = bmsData["BMSStatus"]
                response["BMS FullyChargeFlag"] = bmsData["FullyChargeFlag"]
                response["BMS Pack_V_Sum_of_Cells"] = bmsData["Pack_V_Sum_of_Cells"]
            except:
                bmsData["Pack_Q_SOC_Terminal"] = bmsData["SOH"] = bmsData[
                    "BMSStatus"
                ] = bmsData["FullyChargeFlag"] = bmsData["Pack_V_Sum_of_Cells"] = 0
        elif can_id == "112":
            try:
                bmsData["Aux_T"] = convert_and_get_temperatures(
                    string=can_data[0:12]
                )

                bmsData["BatteryCapacity"] = convert_and_get_desired_value(
                    string=can_data[12:], multiplier=0.1
                )
                response["BMS Aux_T"] = bmsData["Aux_T"]
                response["BMS BatteryCapacity"] = bmsData["BatteryCapacity"]
            except:
                bmsData["Aux_T"] = list()
                bmsData["BatteryCapacity"] = 0
        elif can_id == "113":
            try:
                bmsData["CMU1_Cell_Vtgs"] = []

                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU1_Cell_Vtgs cell_1"] = bmsData["CMU1_Cell_Vtgs"][0]
                response["BMS CMU1_Cell_Vtgs cell_2"] = bmsData["CMU1_Cell_Vtgs"][1]
                response["BMS CMU1_Cell_Vtgs cell_3"] = bmsData["CMU1_Cell_Vtgs"][2]
                response["BMS CMU1_Cell_Vtgs cell_4"] = bmsData["CMU1_Cell_Vtgs"][3]
            except:
                bmsData["CMU1_Cell_Vtgs"] = list()
        elif can_id == "114":
            try:
                bmsData["CMU1_Cell_Vtgs"] = []

                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU1_Cell_Vtgs cell_5"] = bmsData["CMU1_Cell_Vtgs"][0] 
                response["BMS CMU1_Cell_Vtgs cell_6"] = bmsData["CMU1_Cell_Vtgs"][1]
                response["BMS CMU1_Cell_Vtgs cell_7"] = bmsData["CMU1_Cell_Vtgs"][2]
                response["BMS CMU1_Cell_Vtgs cell_8"] = bmsData["CMU1_Cell_Vtgs"][3]
            except:
                bmsData["CMU1_Cell_Vtgs"] = list()
        elif can_id == "115":
            try:
                bmsData["CMU1_Cell_Vtgs"] = []

                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bmsData["CMU1_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU1_Cell_Vtgs cell_9"] = bmsData["CMU1_Cell_Vtgs"][0]
                response["BMS CMU1_Cell_Vtgs cell_10"] = bmsData["CMU1_Cell_Vtgs"][1]
                response["BMS CMU1_Cell_Vtgs cell_11"] = bmsData["CMU1_Cell_Vtgs"][2]
                response["BMS CMU1_Cell_Vtgs cell_12"] = bmsData["CMU1_Cell_Vtgs"][3]
            except:
                bmsData["CMU1_Cell_Vtgs"] = list()

        elif can_id == "116":
            try:
                bmsData["CMU2_Cell_Vtgs"] = []
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU2_Cell_Vtgs Cell 1"] = bmsData["CMU2_Cell_Vtgs"][0]
                response["BMS CMU2_Cell_Vtgs Cell 2"] = bmsData["CMU2_Cell_Vtgs"][1]
                response["BMS CMU2_Cell_Vtgs Cell 3"] = bmsData["CMU2_Cell_Vtgs"][2]
                response["BMS CMU2_Cell_Vtgs Cell 4"] = bmsData["CMU2_Cell_Vtgs"][3]
            except:
                bmsData["CMU2_Cell_Vtgs"] = list()
        elif can_id == "117":
            try:
                if "CMU2_Cell_Vtgs" not in bmsData:
                    bmsData["CMU2_Cell_Vtgs"] = []
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU2_Cell_Vtgs Cell 5"] = bmsData["CMU2_Cell_Vtgs"][0]
                response["BMS CMU2_Cell_Vtgs Cell 6"] = bmsData["CMU2_Cell_Vtgs"][1]
                response["BMS CMU2_Cell_Vtgs Cell 7"] = bmsData["CMU2_Cell_Vtgs"][2]
                response["BMS CMU2_Cell_Vtgs Cell 8"] = bmsData["CMU2_Cell_Vtgs"][3]
            except:
                bmsData["CMU2_Cell_Vtgs"] = list()
        elif can_id == "118":
            try:
                if "CMU2_Cell_Vtgs" not in bmsData:
                    bmsData["CMU2_Cell_Vtgs"] = []
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[0:4], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[8:12], multiplier=0.1)
                )
                bmsData["CMU2_Cell_Vtgs"].append(
                    convert_and_get_desired_value(can_data[12:], multiplier=0.1)
                )
                response["BMS CMU2_Cell_Vtgs Cell 9"] = bmsData["CMU2_Cell_Vtgs"][0]
                response["BMS CMU2_Cell_Vtgs Cell 10"] = bmsData["CMU2_Cell_Vtgs"][1]
                response["BMS CMU2_Cell_Vtgs Cell 11"] = bmsData["CMU2_Cell_Vtgs"][2]
                response["BMS CMU2_Cell_Vtgs Cell 12"] = bmsData["CMU2_Cell_Vtgs"][3]
            except:
                bmsData["CMU2_Cell_Vtgs"] = list()            
        elif can_id == "11c":
            try:
                bmsData["PACK_Q_DESIGN"] = convert_and_get_desired_value(
                    can_data[0:4], multiplier=0.1
                )
                bmsData["PACK_Q_FULL"] = convert_and_get_desired_value(can_data[4:8], multiplier=0.1)
                bmsData["CMU1_CELL_BITMASK"] = convert_and_get_desired_value(can_data[8:12])
                bmsData["CMU2_CELL_BITMASK"] = convert_and_get_desired_value(can_data[12:])
                
                response["BMS PACK_Q_DESIGN"] = bmsData["PACK_Q_DESIGN"]
                response["BMS PACK_Q_FULL"] = bmsData["PACK_Q_FULL"]
                response["BMS CMU1_CELL_BITMASK"] = bmsData["CMU1_CELL_BITMASK"]
                response["BMS CMU2_CELL_BITMASK"] = bmsData["CMU2_CELL_BITMASK"]
            except:
                bmsData["PACK_Q_DESIGN"] = bmsData["PACK_Q_FULL"] = bmsData["CMU1_CELL_BITMASK"] = bmsData["CMU2_CELL_BITMASK"] = 0
        elif can_id == "12a":
            try:
                bmsData["dynamic_in_limit"] = convert_and_get_desired_value(
                    can_data[:4], multiplier=0.1
                )
                bmsData["dynamic_out_limit"] = convert_and_get_desired_value(
                    can_data[4:8], multiplier=0.1
                )
                response["BMS dynamic_in_limit"] = bmsData["dynamic_in_limit"]
                response["BMS dynamic_out_limit"] = bmsData["dynamic_out_limit"]
            except:
                bmsData["dynamic_in_limit"] = bmsData["dynamic_out_limit"] = 0

        elif can_id == "705":
            try:
                ControllerDATA["MotorTemp"] = convert_and_get_temperature(
                    string=can_data[0:2], roundabout=50
                )
                ControllerDATA["Controller_Temp"] = convert_and_get_temperature(
                    string=can_data[2:4], roundabout=50
                )
                ControllerDATA["SOC"] = convert_and_get_desired_value(can_data[4:6])
                ControllerDATA[
                    "Batt_Discharge_Current_Rate"
                ] = convert_and_get_desired_value(can_data[6:8])
                ControllerDATA["Odometer"] = convert_and_get_desired_value(
                    string=can_data[8:], multiplier=0.1
                )
                response["Controller MotorTemp"] = ControllerDATA["MotorTemp"]
                response["Controller Controller_Temp"] = ControllerDATA["Controller_Temp"] 
                response["Controller SOC"] = ControllerDATA["SOC"]
                response["Controller Batt_Discharge_Current_Rate"] = ControllerDATA["Batt_Discharge_Current_Rate"]
                response["Controller Odometer"] = ControllerDATA["Odometer"] 
            except:
                ControllerDATA["MotorTemp"] = ControllerDATA[
                    "Controller_Temp"
                ] = ControllerDATA["SOC"] = ControllerDATA[
                    "Batt_Discharge_Current_Rate"
                ] = ControllerDATA[
                    "Odometer"
                ] = 0
        elif can_id == "706":
            try:
                ControllerDATA["Vehicle_Status"] = convert_and_get_desired_value(
                    can_data[0:2]
                )
                ControllerDATA["AssistLevelGear"] = convert_and_get_desired_value(
                    can_data[4:6]
                )
                ControllerDATA["AlarmFault"] = convert_and_get_desired_value(
                    can_data[6:8]
                )
                ControllerDATA["SpeedLowHigh"] = convert_and_handle_negative_values(
                    string=can_data[8:12], multiplier=0.1
                )
                ControllerDATA["TripLowHigh"] = convert_and_get_desired_value(
                    string=can_data[12:]
                )
                response["Controller Vehicle_Status"] = ControllerDATA["Vehicle_Status"]
                response["Controller AssistLevelGear"] = ControllerDATA["AssistLevelGear"]
                response["Controller AlarmFault"] = ControllerDATA["AlarmFault"]
                response["Controller SpeedLowHigh"] = ControllerDATA["SpeedLowHigh"]
                response["Controller TripLowHigh"] = ControllerDATA["TripLowHigh"] 
            except:
                ControllerDATA["Vehicle_Status"] = ControllerDATA[
                    "controller_mode"
                ] = ControllerDATA["AssistLevelGear"] = ControllerDATA[
                    "AlarmFault"
                ] = ControllerDATA[
                    "SpeedLowHigh"
                ] = ControllerDATA[
                    "TripLowHigh"
                ] = 0
        elif can_id == "708":
            try:
                ControllerDATA["FaultStatus"] = [
                    convert_and_get_desired_value(can_data[0:2]),
                    convert_and_get_desired_value(can_data[2:4]),
                    convert_and_get_desired_value(can_data[4:6]),
                    convert_and_get_desired_value(can_data[6:8]),
                    convert_and_get_desired_value(can_data[8:10]),
                    convert_and_get_desired_value(can_data[10:12]),
                    convert_and_get_desired_value(can_data[12:14]),
                    convert_and_get_desired_value(can_data[14:16]),
                ]
                response["Controller Fault Status"] = ControllerDATA["FaultStatus"]
            except:
                ControllerDATA["FaultStatus"] = list()
        elif can_id == "710":
            try:
                ControllerDATA["ThrottleCommand"] = convert_and_get_desired_value(
                    string=can_data[0:2]
                )
                ControllerDATA["ThrottleMultiplier"] = convert_and_get_desired_value(string=can_data[2:4])
                ControllerDATA["MappedThrottle"] = convert_and_get_desired_value(
                    string=can_data[4:6]
                )
                ControllerDATA["ThrottlePotentiometer"] = convert_and_get_desired_value(
                    string=can_data[6:8], multiplier=0.1
                )
                ControllerDATA["BrakeCommand"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                ControllerDATA["MappedBrake"] = convert_and_get_desired_value(
                    string=can_data[10:12], multiplier=1
                )
                ControllerDATA["Potential2Row"] = convert_and_get_desired_value(
                    string=can_data[12:14], multiplier=0.1
                )
                response["Controller ThrottleCommand"] = ControllerDATA["ThrottleCommand"]
                response["Controller ThrottleMultiplier"] = ControllerDATA["ThrottleMultiplier"]
                response["Controller MappedThrottle"] = ControllerDATA["MappedThrottle"]
                response["Controller ThrottlePotentiometer"] = ControllerDATA["ThrottlePotentiometer"]
                response["Controller BrakeCommand"] = ControllerDATA["BrakeCommand"]
                response["Controller MappedBrake"] =  ControllerDATA["MappedBrake"]
                response["Controller Potential2Row"] = ControllerDATA["Potential2Row"]

            except:
                ControllerDATA["ThrottleCommand"] = ControllerDATA[
                    "ThrottleMultiplier"
                ] = ControllerDATA["MappedThrottle"] = ControllerDATA[
                    "ThrottlePotentiometer"
                ] = ControllerDATA[
                    "BrakeCommand"
                ] = ControllerDATA[
                    "MappedBrake"
                ] = ControllerDATA[
                    "Potential2Row"
                ] = 0
        elif can_id == "715":
            try:
                ControllerDATA["BatteryCapacityVoltage"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                ControllerDATA["BatteryKeyswitchVoltage"] = convert_and_get_desired_value(
                    string=can_data[10:12], multiplier=1
                )
                ControllerDATA["MotorRPM"] = convert_and_handle_negative_values(
                    string=can_data[12:], multiplier=1
                )
                response["Controller BatteryCapacityVoltage"] = ControllerDATA["BatteryCapacityVoltage"]
                response["Controller BatteryKeyswitchVoltage"] = ControllerDATA["BatteryKeyswitchVoltage"]
                response["Controller MotorRPM"] = ControllerDATA["MotorRPM"]
            except:
                ControllerDATA["BatteryCapacityVoltage"] = ControllerDATA[
                    "BatteryKeyswitchVoltage"
                ] = ControllerDATA["MotorRPM"] = 0
        elif can_id == "716":
            try:
                ControllerDATA["ControllerMasterTimer"] = convert_and_get_desired_value(
                    string=can_data[2:10], multiplier=0.1
                )
                ControllerDATA["ControllerCurrentRMS"] = convert_and_get_desired_value(
                    string=can_data[12:14], multiplier=1
                )
                ControllerDATA["ControllerModulationDepth"] = convert_and_get_desired_value(
                    string=can_data[14:], multiplier=1
                )
                response["Controller ControllerMasterTimer"] = ControllerDATA["ControllerMasterTimer"]
                response["Controller ControllerCurrentRMS"] = ControllerDATA["ControllerCurrentRMS"]
                response["Controller ControllerModulationDepth"] = ControllerDATA["ControllerModulationDepth"]

            except:
                ControllerDATA["ControllerMasterTimer"] = ControllerDATA[
                    "ControllerCurrentRMS"
                ] = ControllerDATA["ControllerModulationDepth"] = 0
        elif can_id == "717":
            try:
                ControllerDATA["ControllerFrequency"] = convert_and_get_desired_value(
                    string=can_data[0:4], multiplier=1
                )
                ControllerDATA["ControllerMainState"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=1
                )
                response["Controller ControllerFrequency"] = ControllerDATA["ControllerFrequency"]
                response["Controller ControllerMainState"] = ControllerDATA["ControllerMainState"]
            except:
                ControllerDATA["ControllerFrequency"] = ControllerDATA[
                    "ControllerMainState"
                ] = 0
        elif can_id == "724":
            try:
                ControllerDATA["MotorTorqueEstimated"] = convert_and_handle_negative_values(
                    string=can_data[0:4], multiplier=0.1
                )

                ControllerDATA["BatteryPowerConsumed"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=0.1
                )
                ControllerDATA["BatteryEnergyConsumed"] = convert_and_get_desired_value(
                    string=can_data[6:8], multiplier=0.1
                )
                ControllerDATA["VehiclePowerMode"] = convert_and_get_desired_value(
                    string=can_data[8:10]
                )
                response["Controller MotorTorqueEstimated"] = ControllerDATA["MotorTorqueEstimated"]
                response["Controller BatteryPowerConsumed"] = ControllerDATA["BatteryPowerConsumed"]
                response["Controller BatteryEnergyConsumed"] = ControllerDATA["BatteryEnergyConsumed"]
                response["Controller VehiclePowerMode"] = ControllerDATA["VehiclePowerMode"]
            except:
                ControllerDATA["MotorTorqueEstimated"] = ControllerDATA[
                    "BatteryPowerConsumed"
                ] = ControllerDATA["BatteryEnergyConsumed"] = ControllerDATA[
                    "VehiclePowerMode"
                ] = 0
        elif can_id == "725":
            try:
                ControllerDATA["AccelerationRate"] = convert_and_get_desired_value(
                    string=can_data[0:2], multiplier=0.1
                )
                ControllerDATA[
                    "AccelerationReleaseRate"
                ] = convert_and_get_desired_value(
                    string=can_data[2:4], multiplier=0.1
                )
                ControllerDATA["BrakeRate"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=0.1
                )
                ControllerDATA["DriveCurrentLimit"] = convert_and_get_desired_value(
                    string=can_data[6:8], multiplier=1
                )
                ControllerDATA["RegenCurrentLimit"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                ControllerDATA["BrakeCurrentLimit"] = convert_and_get_desired_value(
                    string=can_data[10:12], multiplier=1
                )
                ControllerDATA["RegenOff"] = 0 if can_data[12:14] == "FF" else 1
                ControllerDATA["ControllerResetCANBaudRate"] = convert_and_get_desired_value(
                    string=can_data[14:], multiplier=1
                )
                response["Controller AccelerationRate"] = ControllerDATA["AccelerationRate"]
                response["Controller AccelerationReleaseRate"] = ControllerDATA["AccelerationReleaseRate"]
                response["Controller BrakeRate"] = ControllerDATA["BrakeRate"]
                response["Controller DriveCurrentLimit"] = ControllerDATA["DriveCurrentLimit"]
                response["Controller RegenCurrentLimit"] = ControllerDATA["RegenCurrentLimit"]
                response["Controller BrakeCurrentLimit"] =  ControllerDATA["BrakeCurrentLimit"] 
                response["Controller RegenOff"] = ControllerDATA["RegenOff"]
                response["Controller ControllerResetCANBaudRate"] = ControllerDATA["ControllerResetCANBaudRate"]
            except:
                ControllerDATA["AccelerationRate"] = ControllerDATA[
                    "AccelerationReleaseRate"
                ] = ControllerDATA["BrakeRate"] = ControllerDATA[
                    "DriveCurrentLimit"
                ] = ControllerDATA[
                    "RegenCurrentLimit"
                ] = ControllerDATA[
                    "BrakeCurrentLimit"
                ] = ControllerDATA[
                    "RegenOff"
                ] = ControllerDATA[
                    "ControllerResetCANBaudRate"
                ] = 0
        elif can_id == "726":
            try:
                ControllerDATA["ControllerSerialNumber"] = convert_and_get_desired_value(can_data[0:8])
                ControllerDATA["VCLVersion"] = convert_and_get_desired_value(
                    can_data[8:10]
                )
                ControllerDATA["VCLBuildNumber"] = convert_and_get_desired_value(
                    can_data[10:12]
                )
                ControllerDATA["OSVersion"] = convert_and_get_desired_value(
                    can_data[12:14]
                )
                ControllerDATA["OSBuildNumber"] = convert_and_get_desired_value(
                    can_data[14:]
                )
                response["Controller ControllerSerialNumber"] = ControllerDATA["ControllerSerialNumber"]
                response["Controller VCLVersion"] = ControllerDATA["VCLVersion"]
                response["Controller VCLBuildNumber"] = ControllerDATA["VCLBuildNumber"]
                response["Controller OSVersion"] =  ControllerDATA["OSVersion"]
                response["Controller OSBuildNumber"] = ControllerDATA["OSBuildNumber"]
            except:
                ControllerDATA["ControllerSerialNumber"] = ControllerDATA[
                    "VCLVersion"
                ] = ControllerDATA["VCLBuildNumber"] = ControllerDATA[
                    "OSVersion"
                ] = ControllerDATA[
                    "OSBuildNumber"
                ] = 0
        elif can_id == "258":
            try:
                ControllerDATA["Number_of_Active_Errors"] = convert_and_get_desired_value(
                    string=can_data[8:12], multiplier=1
                )
                response["Number_of_Active_Errors"] = ControllerDATA["Number_of_Active_Errors"]
            except:
                ControllerDATA["Number_of_Active_Errors"] = 0
        elif can_id == "259":
            try:
                ControllerDATA["Sum_of_error_since_boot"] = convert_and_get_desired_value(
                    string=can_data[8:], multiplier=1
                )
                response["Sum_of_error_since_boot"] = ControllerDATA["Sum_of_error_since_boot"]
            except:
                ControllerDATA["Sum_of_error_since_boot"]  = 0
        elif can_id == "1806e5f4":
            try:
                ControllerDATA["Ch_V"] = convert_and_get_desired_value(
                    string=can_data[:4], multiplier=1
                )
                ControllerDATA["Ch_C"] = convert_and_get_desired_value(
                    string=can_data[4:8], multiplier=1
                )
                ControllerDATA["Ch_S"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                response["Ch_V"] = ControllerDATA["Ch_V"]
                response["Ch_C"] = ControllerDATA["Ch_C"]
                response["Ch_S"] = ControllerDATA["Ch_S"]
            except:
                ControllerDATA["Ch_C"]  =ControllerDATA["Ch_V"]  =ControllerDATA["Ch_S"]  = 0
        elif can_id == "7a0":
            try:
                ControllerDATA["Device_id_VCU"] = convert_and_get_desired_value(
                    string=can_data[:2], multiplier=1
                )
                ControllerDATA["Version_Major"] = convert_and_get_desired_value(
                    string=can_data[2:4], multiplier=1
                )
                ControllerDATA["Version_Minor"] = convert_and_get_desired_value(
                    string=can_data[4:6], multiplier=1
                )
                ControllerDATA["Patch"] = convert_and_get_desired_value(
                    string=can_data[6:8], multiplier=1
                )
                ControllerDATA["Build_Type_and_Production_Build"] = convert_and_get_desired_value(
                    string=can_data[8:10], multiplier=1
                )
                response["Device_id_VCU"] = ControllerDATA["Device_id_VCU"]
                response["Version_Major"] = ControllerDATA["Version_Major"]
                response["Version_Minor"] = ControllerDATA["Version_Minor"]
                response["Patch"] = ControllerDATA["Patch"]
                response["Build_Type_and_Production_Build"] = ControllerDATA["Build_Type_and_Production_Build"]
            except:
                ControllerDATA["Ch_C"]  =ControllerDATA["Ch_V"]  =ControllerDATA["Ch_S"]  = 0

    return response
        


# can_ids = ['20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '20', '110', '111', '20', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '258', '259', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '725', '20', '20', '110', '111', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '258', '259', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '110', '111', '20', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '258', '259', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '725', '20', '20', '110', '111', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '258', '259', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '110', '111', '20', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '258', '259', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '725', '20', '20', '20', '110', '111', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '258', '259', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '110', '111', '20', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '258', '259', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '725', '20', '20', '20', '110', '111', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '258', '259', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '110', '111', '20', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '20', '726', '258', '259', '20', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '725', '20', '20', '20', '110', '111', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '258', '259', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '20', '110', '111', '20', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '258', '259', '20', '20', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '725', '20', '20', '20', '110', '111', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '258', '259', '20', '20', '20', '20', '705', '706', '708', '710', '715', '20', '716', '717', '724', '726', '20', '20', '110', '111', '20', '112', '113', '114', '115', '116', '117', '118', '1806E5F4', '12A', '11C', '20', '20', '20', '705', '706', '708', '710', '715', '716', '717', '724', '726', '20', '20', '258', '259', '20', '20']

# vehicle_data = ['8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010500', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '00EE734F00000200', '00000A0000000000', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E000000000000', '0922102703002C03', '8000A00348010600', '161715151414E205', '5000549E579E599E', '5A9E5A9E569E569E', '599E559E00000000', 'B19EB29EB09EB39E', 'B29EB29EB39EB29E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '0000000000000000', '0000000000000000', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '00F3734F00000300', '00000A0000000000', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '00F8734F00000200', '00000A0000000000', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010500', '0000006464000F02', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '161715151414E205', '5000549E599E5A9E', '5B9E5A9E569E569E', '599E559E00000000', 'B29EB19EB19EB19E', 'B29EB39EB39EB39E', '0000B49E00000100', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '0000000000000000', '0000000000000000', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '00FD734F00000200', '00000A0000000000', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0001744F00000200', 'FFFF0A0000000300', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '8000A00348010600', '161715151414E205', '5000549E589E599E', '5A9E5B9E549E569E', '599E549E00000000', 'B19EB19EAF9EB19E', 'B09EB19EB29EB19E', '0000B39E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010500', '8000A00348010600', '0000000000000000', '0000000000000000', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0006744F00000300', '00000A0000000300', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010500', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '000B744F00000300', '00000A000000F8FF', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '0000006464000F02', '8000A00348010600', '8000A00348010600', 'B59E0000AC15FFFF', '0922102703002C03', '161715151414E205', '5100539E589E599E', '5A9E5B9E559E559E', '5A9E559E00000000', 'B29EB19EB09EB29E', 'B19EB29EB39EB39E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '0000000000000000', '0000000000000000', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0010744F00000300', 'FFFF0A000000F8FF', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0015744F00000300', '00000A0000000300', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '8000A00348010600', '161715151414E205', '5000539E589E5A9E', '5B9E5C9E569E569E', '599E559E00000000', 'B19EB29EB09EB19E', 'B19EB19EB39EB29E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '0000000000000000', '0000000000000000', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0019744F00000300', '00000A0000000100', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010500', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '001E744F00000200', 'FFFF0A000000F8FF', '0000000001000000', '02870100010E2500', '8000A00348010600', '0000006464000F02', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '161715151414E205', '5000539E589E5A9E', '5A9E5B9E569E569E', '599E559E00000000', 'B19EB19EAF9EB29E', 'B29EB29EB49EB29E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0023744F00000200', '00000A0000000300', '0000000001000000', '02870100010E2500', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0028744F00000300', '00000A0000000100', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '8000A00348010600', '161715151414E205', '5000549E599E5A9E', '5C9E5A9E559E569E', '5A9E549E00000000', 'B19EB09EB19EB19E', 'B09EB29EB49EB49E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '002D744F00000300', '00000A0000000100', '0000000001000000', '02870100010E2500', '8000A00348010600', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0032744F00000200', '00000A0000000100', '0000000001000000', '02870100010E2500', '0000006464000F02', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '161715151414E205', '5000529E589E599E', '5A9E5A9E559E559E', '589E549E00000000', 'B19EB09EB09EB19E', 'B19EB19EB39EB39E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0036744F00000300', '00000A0000000100', '0000000001000000', '02870100010E2500', '8000A00348010600', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '003B744F00000200', 'FFFF0A000000FAFF', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B39E0000AC15FFFF', '0922102703002C03', '8000A00348010600', '161715151414E205', '4F00519E579E599E', '5A9E5B9E559E559E', '5A9E559E00000000', 'B19EB09EAF9EB19E', 'B19EB29EB39EB39E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0040744F00000300', '00000A000000FBFF', '0000000001000000', '8000A00348010600', '02870100010E2500', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010500', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0045744F00000200', 'FFFF0A000000FAFF', '0000000001000000', '02870100010E2500', '0000006464000F02', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '161715151414E205', '5000539E5A9E5A9E', '5B9E5B9E559E569E', '599E549E00000000', 'B29EB29EB09EB19E', 'B29EB29EB39EB39E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '004A744F00000200', '00000A0000000100', '0000000001000000', '02870100010E2500', '8000A00348010600', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010500', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '004E744F00000300', 'FFFF0A0000000100', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B59E0000AC15FFFF', '0922102703002C03', '8000A00348010500', '161715151414E205', '5100529E589E5A9E', '5A9E599E559E559E', '599E549E00000000', 'B19EB09EAF9EB09E', 'B09EB29EB39EB39E', '0000B59E00000000', '0348010500000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0053744F00000300', '00000A000000FBFF', '0000000001000000', '02870100010E2500', '8000A00348010600', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0058744F00000200', '00000A0000000300', '0000000001000000', '02870100010E2500', '0000006464000F02', '8000A00348010600', '8000A00348010600', '8000A00348010600', 'B49E0000AC15FFFF', '0922102703002C03', '161715151414E205', '5000539E579E5B9E', '5B9E5C9E579E559E', '599E539E00000000', 'B19EB19EB19EB29E', 'B29EB29EB29EB29E', '0000B39E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010500', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '005D744F00000300', '00000A0000000400', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600', '8000A00348010600', '8000A00348010600', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '8000A00348010600', '0062744F00000300', '00000A0000000400', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010600', 'B39E0000AC15FFFF', '0922102703002C03', '8000A00348010600', '161715151414E205', '4F00529E599E599E', '5B9E5B9E559E549E', '589E539E00000000', 'B09EB19EAF9EB19E', 'B19EB29EB29EB39E', '0000B49E00000000', '0348010600000000', 'C603C40900000000', 'C006C00602053242', '8000A00348010600', '8000A00348010500', '8000A00348010500', '4A590000F80C0000', '0420000000004C01', '0000000100000000', '000000071313D900', '0000000051510000', '0066744F00000200', 'FFFF0A000000F9FF', '0000000001000000', '02870100010E2500', '8000A00348010600', '8000A00348010500', '0000000000000000', '0000000000000000', '8000A00348010600', '8000A00348010600']
