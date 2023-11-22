from . import confighandler
from drawranflow.models import MainTable, Associations, Messages
from django.db.models import Q
from .confighandler import ConfigHandler as Ch
# Handling E1AP messages
class E1APHandler:
    def __init__(self, e1ap_packet, frameNumber, frameTime):
        self.e1ap_packet = e1ap_packet
        self.frame_time = frameTime
        self.frame_number = frameNumber

    def findE1OperationCode(self):

        rrcPrcedureName = "None"
        procedureCode = self.e1ap_packet.get('e1ap.procedureCode')
        config_handler = Ch(intName="e1ap", procCode=procedureCode, packetLayer=self.e1ap_packet)

        procedureName, rrcPrcedureName = config_handler.getProcedureName()

        if rrcPrcedureName is None:
            rrcPrcedureName = "None"
            srcNode, dstNode = config_handler.getDirection(procedureName)

        return procedureName, rrcPrcedureName, srcNode, dstNode

    def find_main_table_by_cpe1ap_id(self, cpe1ap_id, message_id):
        try:
            main_table = MainTable.objects.get(cp_e1ap_id=cpe1ap_id, up_e1ap_id__isnull=True)
            # Check if the Associations table doesn't contain the specified message_id
            association = Associations.objects.filter(
                Q(main=main_table) &
                (~Q(assoc_key=message_id) & Q(assoc_key__startswith='BearerContextSetupRequest_'))
            ).exists()
            if main_table and association:
                return main_table, association
        except MainTable.DoesNotExist:
            return None, None

    def get_main_and_association(self, cpe1ap, message_id):
        try:
            main_table = MainTable.objects.get(cu_f1ap_id=cpe1ap, cp_e1ap_id__isnull=True)

            # Check if the Associations table doesn't contain the specified message_id
            association = Associations.objects.filter(
                Q(main=main_table) &
                Q(assoc_key__startswith='ngapInitialContextSetupRequest_')
                & (~Q(assoc_key=message_id))
            ).exists()
            if main_table and association:
                return main_table, association
        except MainTable.DoesNotExist:
            return None, None

    def get_e1ap_main_table_assoc(self, cpe1ap, message_id, upe1ap):
        try:
            main_table = MainTable.objects.get(cp_e1ap_id=cpe1ap, up_e1ap_id=upe1ap)
            # Check if the Associations table doesn't contain the specified message_id
            association = Associations.objects.filter(main=main_table, assoc_key=message_id).exists()
            if main_table and not association:
                return main_table, association
        except MainTable.DoesNotExist:
            return None, None

    def create_association(self, main_table, assoc_key, src, dst, srcNode, dstNode):
        association, created = Associations.objects.get_or_create(assoc_key=assoc_key, src=src, dst=dst,
                                                                  src_type=srcNode, dst_type=dstNode, main=main_table)
        association.save()
        return association, created

    def create_message(self, main_table, message_key, f1ap_packet, assoc):
        message = Messages(message_key=message_key, association=assoc, message_json=f1ap_packet, main=main_table)
        message.save()
        return message

    def handleAllE1AP(self):

        e1apProc, rrcProc, srcNode, dstNode = self.findE1OperationCode()
        message_id = f'{e1apProc}_{self.frame_number}_{self.frame_time}'

        cp_e1ap_id = self.e1ap_packet.get('e1ap.GNB_CU_CP_UE_E1AP_ID')
        up_e1ap_id = self.e1ap_packet.get('e1ap.GNB_CU_UP_UE_E1AP_ID')
        src = self.e1ap_packet.get('ip.src')
        dst = self.e1ap_packet.get('ip.dst')
        main_table = None
        association = None

        if cp_e1ap_id and message_id and not up_e1ap_id:
            main_table, association = self.get_main_and_association(cpe1ap=cp_e1ap_id, message_id=message_id)
        if not main_table and cp_e1ap_id:
            main_table, association = self.find_main_table_by_cpe1ap_id(cpe1ap_id=cp_e1ap_id, message_id=message_id)

        if not main_table and cp_e1ap_id and up_e1ap_id:
            main_table, association = self.get_e1ap_main_table_assoc(cpe1ap=cp_e1ap_id, upe1ap=up_e1ap_id,
                                                                     message_id=message_id)

        if e1apProc == 'BearerContextSetupRequest':
            if main_table and association:
                try:
                    setattr(main_table, "cp_e1ap_id", cp_e1ap_id)
                    main_table.save()
                except MainTable.DoesNotExist:
                    pass
        else:
            setattr(main_table, "up_e1ap_id", up_e1ap_id)
            main_table.save()

        if main_table:
            # Check for duplicate associations and messages
            association_exists = Associations.objects.filter(main=main_table, assoc_key=message_id).exists()
            message_exists = Messages.objects.filter(main=main_table, message_key=message_id).exists()

            if not association_exists or not message_exists and association:
                assoc, created = self.create_association(main_table, message_id, src, dst, srcNode, dstNode)
                if assoc:
                    self.create_message(main_table, message_id, self.e1ap_packet, assoc=assoc)
