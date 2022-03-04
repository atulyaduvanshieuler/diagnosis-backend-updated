"""
This file will feed input to can and
will receive and validate serial output.
"""

import time
import can
from ..shared import (ser,can_bus ,stark_general_logger, stark_data_logger, stark_error_logger)
from ..shared.constants import (CAN_INPUT_ID)
from .validate_stark_output import verify_serial


def send_receive_validate(input_msg, _uuid):
    """This function will send to can,receive and validate the serial ouput.

    Args:
        can_bus (_object_): can connection object
        ser (_object_): serial connection object
        input_msg (_string_): What input to send to can
    """
    try:

        can_msg=can.Message(
            arbitration_id = CAN_INPUT_ID,
            data = input_msg,
            is_extended_id = False,
        )


        try:
            can_bus.send(can_msg)
        except can.CanError:
            stark_error_logger.error("uuid - %s message - CAN Message Not Sent" %_uuid)
        
        time.sleep(5)


        msg_buffer_size = ser.inWaiting()
        data = ser.read(msg_buffer_size)



        try:
            info = data.decode("UTF-8")
        except:

            stark_data_logger.info(str(info))
            stark_error_logger.error("uuid - %s message - Stark Output can be decoded in UTF-8. Following output received: %s" %(_uuid, str(info)))

            return False


        try:
            stark_data_logger.info(str(info))
        except:
            stark_error_logger.error("uuid - %s message - Stark logs not added" %_uuid )

        if info.count("DIAG_STARK_START") == 1:
            res = verify_serial(info, _uuid)
            if res==True:
                stark_general_logger.info("uuid - %s message - Stark output verified." %_uuid )
                return True
            else:
                stark_error_logger.warning("uuid - %s message - Stark output not verified.(Reasons may be anything. Check above reasons to see reason." %_uuid )
                return False
        else:
            stark_data_logger.critical("uuid - %s message - Wrong  Stark Input received: %s"  %(_uuid, str(info)))

    except Exception as e:
        stark_error_logger.error(e)
        return False