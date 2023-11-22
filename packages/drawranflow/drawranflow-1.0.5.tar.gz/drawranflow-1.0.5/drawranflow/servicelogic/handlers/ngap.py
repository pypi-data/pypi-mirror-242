from . import confighandler
from drawranflow.models import MainTable, Associations, Messages
from django.db.models import Q
from .confighandler import ConfigHandler as Ch


# Handling NGAP messages
class NGAPHandler:
    def __init__(self, ngap_packet, frameNumber, frameTime):
        self.ngap_packet = ngap_packet
        self.frame_time = frameTime
        self.frame_number = frameNumber

# findNgOperationCode finding Operation Code and descriptive Name
    def findNgOperationCode(self):

        procedureCode = self.ngap_packet.get('ngap.procedureCode')
        config_handler = Ch(intName="", procCode=procedureCode, packetLayer=self.ngap_packet)
        procedureName = config_handler.getNgapMessages()
        srcNode, dstNode = config_handler.getDirection(procedureName)

        return procedureName, srcNode, dstNode

# find_main_table_by_cpngap_id Getting the main table based on RAN NGAP and Message ID to Update AMF ID

    def find_main_table_by_cpngap_id(self, cu_ngap_id, message_id):
        try:
            main_table = MainTable.objects.get(cu_ngap_id=cu_ngap_id, amf_ngap_id__isnull=True)
            # Check if the Associations table doesn't contain the specified message_id
            association = Associations.objects.filter(
                Q(main=main_table) &
                (~Q(assoc_key=message_id) &
                 (Q(assoc_key__startswith='serviceRequest_') | Q(assoc_key__startswith='registrationRequest_')
                  )
                 )
            ).exists()
            if main_table and association:
                return main_table, association
        except MainTable.DoesNotExist:
            return None, None
# get_main_and_association Finding association and maintable based on RAN NGAP and Message ID to update RAN NGAP ID
    def get_main_and_association(self, cu_ngap_id, message_id):
        try:
            main_table = MainTable.objects.get(cu_f1ap_id=cu_ngap_id, amf_ngap_id__isnull=True)
            # Check if the Associations table doesn't contain the specified message_id
            association = Associations.objects.filter(
                Q(main=main_table) &
                (~Q(assoc_key=message_id) & Q(assoc_key__startswith='rrcSetupComplete_'))
            ).exists()
            if main_table and association:
                return main_table, association
        except MainTable.DoesNotExist:
            return None, None
# get_ngap_main_table_assoc Checking main and Assoc tables to find RAN and AMF NGAP IDs to process other NGAP messages

    def get_ngap_main_table_assoc(self, cu_ngap_id, message_id, amf_ngap_id):
        try:
            main_table = MainTable.objects.get(cu_ngap_id=cu_ngap_id, amf_ngap_id=amf_ngap_id)
            # Check if the Associations table doesn't contain the specified message_id
            association = Associations.objects.filter(main=main_table, assoc_key=message_id).exists()
            if main_table and not association:
                return main_table, association
        except MainTable.DoesNotExist:
            return None, None
# create_association Adding the Association related to flow
    def create_association(self, main_table, assoc_key, src, dst, srcNode, dstNode):
        association, created = Associations.objects.get_or_create(assoc_key=assoc_key, src=src, dst=dst,
                                                                  src_type=srcNode, dst_type=dstNode, main=main_table)
        association.save()
        return association, created
# create_message Adding the message
    def create_message(self, main_table, message_key, f1ap_packet, assoc):
        message = Messages(message_key=message_key, association=assoc, message_json=f1ap_packet, main=main_table)
        message.save()
        return message

# handleAllNGAP Handling all NGAP messages based on filters defined.
    def handleAllNGAP(self):

        ngapProc, srcNode, dstNode = self.findNgOperationCode()
        message_id = f'{ngapProc}_{self.frame_number}_{self.frame_time}'

        cu_ngap_id = self.ngap_packet.get('ngap.RAN_UE_NGAP_ID')
        amf_ngap_id = self.ngap_packet.get('ngap.AMF_UE_NGAP_ID')
        src = self.ngap_packet.get('ip.src')
        dst = self.ngap_packet.get('ip.dst')

        main_table = None
        association = None

        if cu_ngap_id and message_id and not amf_ngap_id:
            main_table, association = self.get_main_and_association(cu_ngap_id=cu_ngap_id, message_id=message_id)

        if not main_table and cu_ngap_id:
            main_table, association = self.find_main_table_by_cpngap_id(cu_ngap_id=cu_ngap_id, message_id=message_id)

        if not main_table and cu_ngap_id and amf_ngap_id:
            main_table, association = self.get_ngap_main_table_assoc(cu_ngap_id=cu_ngap_id, amf_ngap_id=amf_ngap_id,
                                                                     message_id=message_id)

        if ngapProc in ['serviceRequest', 'registrationRequest']:
            if main_table and association:
                try:
                    setattr(main_table, "cu_ngap_id", cu_ngap_id)
                    main_table.save()

                except MainTable.DoesNotExist:
                    pass
        else:
            setattr(main_table, "amf_ngap_id", amf_ngap_id)
            main_table.save()

        if main_table:

            # Check for duplicate associations and messages
            association_exists = Associations.objects.filter(main=main_table, assoc_key=message_id).exists()
            message_exists = Messages.objects.filter(main=main_table, message_key=message_id).exists()

            if not association_exists or not message_exists:
                assoc, created = self.create_association(main_table, message_id, src, dst, srcNode, dstNode)
                if assoc:
                    self.create_message(main_table, message_id, self.ngap_packet, assoc=assoc)
