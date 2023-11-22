import time
import datetime
import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
import logging
import os

from drawranflow.models import Identifiers, Message


def configure_logging(log_file_path):
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),  # Add a FileHandler to write logs to a file
            logging.StreamHandler(),  # Add a StreamHandler to print logs to the console
        ]
    )


log_file_path = os.path.join('drawranflow/servicelogic/', 'debug.log')
configure_logging(log_file_path)


class E1apDataFrameProcessor:
    def __init__(self):
        pass
        # log_file_path = os.path.join('drawranflow', 'debug.log')
        # configure_logging(log_file_path)

    def process_dataframe(self,index,row):
        # Process "RRC Setup Request" messages

            gnb_cu_cp_ue_e1ap_id = row['e1ap.GNB_CU_CP_UE_E1AP_ID']
            gnb_cu_up_ue_e1ap_id = row['e1ap.GNB_CU_UP_UE_E1AP_ID']
            message_type = row['_ws.col.info']
            logging.debug(
                f"Processing row {index}: GNB_CU_CP_UE_E1AP_ID={gnb_cu_cp_ue_e1ap_id}, GNB_CU_UP_UE_E1AP_ID={gnb_cu_up_ue_e1ap_id}"
                f",Message Type={message_type}")

            match message_type:
                case 'BearerContextSetupRequest':
                    logging.debug("Processing BearerContextSetupRequest")
                    try:
                        # Check if the identifier exists
                        identifier_object = Identifiers.objects.get(
                            GNB_CU_UE_F1AP_ID=gnb_cu_cp_ue_e1ap_id,
                            GNB_CU_CP_UE_E1AP_ID__isnull=True,
                            GNB_CU_UP_UE_E1AP_ID__isnull=True
                        )

                        # Print messages associated with the identifier for debugging
                        associated_messages = Message.objects.filter(identifiers_id=identifier_object.id)
                        for msg in associated_messages:
                            logging.debug(f"Message for identifier {identifier_object.id}: {msg.Message}")

                        # Additional conditions after confirming that the identifier exists
                        # Additional conditions after confirming that the identifier exists
                        rrc_setup_complete_exists = Message.objects.filter(
                            identifiers_id=identifier_object.id,
                            Message__iexact='Service request'.strip()  # Case-insensitive and strip spaces
                        ).exists()
                        logging.debug(f"Message for identifier {identifier_object.id}: {Message.objects.filter(identifiers_id=identifier_object.id).values_list('Message', flat=True)}")

                        logging.debug(
                            f"Identifiers object {identifier_object.id}, rrc_setup_complete_exists: {rrc_setup_complete_exists}")

                        # service_request_exists = Message.objects.filter(
                        #     identifiers=identifier_object,
                        #     Message='Service Request'
                        # ).exists()
                        #
                        # registration_request_exists = Message.objects.filter(
                        #     identifiers=identifier_object,
                        #     Message='Registration Request'
                        # ).exists()
                        print(rrc_setup_complete_exists,"rrc_setup_complete_exists",identifier_object)
                        if rrc_setup_complete_exists:
                            #and (service_request_exists or registration_request_exists):
                            # All conditions are satisfied, proceed with the identifier update
                            identifier_object.GNB_CU_CP_UE_E1AP_ID = gnb_cu_cp_ue_e1ap_id
                            identifier_object.save()
                            self.save_messages(row, identifier_object)

                    except Identifiers.DoesNotExist:
                        logging.error("Identifier does not exist.")
                        pass
                    except Exception as e:
                        logging.error(f"Error processing BearerContextSetupRequest: {e}")
                        pass
                case 'BearerContextSetupResponse':
                    logging.debug("Processing BearerContextSetupResponse or BearerContextSetupFailure")

                    if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                        try:
                            existing_identifier = Identifiers.objects.get(
                                GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                                GNB_CU_UP_UE_E1AP_ID__isnull=True
                            )
                            if existing_identifier:
                                existing_identifier.GNB_CU_UP_UE_E1AP_ID = gnb_cu_up_ue_e1ap_id
                                existing_identifier.save()
                                self.save_messages(row, existing_identifier)
                        except ObjectDoesNotExist as e:
                            logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                            pass
                    else:
                        pass
                case  'BearerContextSetupFailure':
                    logging.debug("Processing BearerContextSetupResponse or BearerContextSetupFailure")

                    if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                        try:
                            existing_identifier = Identifiers.objects.get(
                                GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                                GNB_CU_UP_UE_E1AP_ID__isnull=True
                            )
                            if existing_identifier:
                                existing_identifier.GNB_CU_UP_UE_E1AP_ID = gnb_cu_up_ue_e1ap_id
                                existing_identifier.save()
                                self.save_messages(row, existing_identifier)
                        except ObjectDoesNotExist as e:
                            logging.error(f"ObjectDoesNotExist: {e}. Skipping...{index}")
                            pass
                    else:
                        pass
                case _:
                    if not pd.isnull(gnb_cu_cp_ue_e1ap_id) and not pd.isnull(gnb_cu_up_ue_e1ap_id):
                        try:
                            existing_identifier = Identifiers.objects.get(
                                GNB_CU_CP_UE_E1AP_ID=gnb_cu_cp_ue_e1ap_id,
                                GNB_CU_UP_UE_E1AP_ID=gnb_cu_up_ue_e1ap_id
                            )
                            if existing_identifier:
                                # Check if "RRC Setup Request" exists for the identifier
                                bearer_context_setup_response_exists = Message.objects.filter(
                                    identifiers=existing_identifier,
                                    Message='BearerContextSetupResponse'
                                ).exists()

                                if bearer_context_setup_response_exists:
                                    self.save_messages(row, existing_identifier)
                                else:
                                    logging.info(
                                        f"Skipping DB update/inserts for row {index}. 'BearerContextSetupResponse' not found in Messages for the identifier.")
                        except ObjectDoesNotExist as e:
                            logging.error(f"ObjectDoesNotExist: {e}. Skipping...")
                            pass
                    else:
                        pass

    def create_message_object(self, row, identifier):
        try:
            message = Message(
                FrameNumber=row['frame.number'],
                IpSrc=row['ip.src'],
                IpDst=row['ip.dst'],
                Protocol=row['frame.protocols'],
                F1_Proc=row['f1ap.procedureCode'],
                Message=row['_ws.col.info'],
                identifiers=identifier
            )
        except Exception as e:
            logging.error(f"Error creating message object: {e}, {row['_ws.col.info']},{row['frame.number']}, {identifier}")

        return message

    def save_messages(self, row, identifier):
        # Check if a message of the same type and frame number already exists for the identifier
        message_type = row['_ws.col.info']
        frame_number = row['frame.number']
        try:
            message_exists = Message.objects.filter(
                identifiers=identifier,
                Message=message_type,
                FrameNumber=frame_number
            ).exists()
        except Exception as e:
            logging.error(f"Failed to query save message , {e}, {row['_ws.col.info']},{identifier}")
        if not message_exists:
            # Process the message
            message = self.create_message_object(row, identifier)
            message.save()
            logging.debug(f"Saved message: {message}")
