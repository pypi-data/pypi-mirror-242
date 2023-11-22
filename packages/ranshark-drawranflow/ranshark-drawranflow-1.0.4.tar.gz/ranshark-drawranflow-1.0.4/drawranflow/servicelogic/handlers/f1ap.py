from . import confighandler
from drawranflow.models import MainTable, Associations, Messages
from .confighandler import ConfigHandler as Ch


# Handling F1AP messages
class F1APHandler:
    def __init__(self, data_frame, upload_id):
        self.f1ap_packet = data_frame

        self.upload_id = upload_id

    import pandas as pd

    # Step 1: Filter DataFrame to select rows with "f1ap" in the Protocol
    f1ap_messages = df[df['Protocol'].str.contains('f1ap', case=False, na=False)]

    # Step 2: Iterate through the selected F1AP messages and process them
    for index, row in f1ap_messages.iterrows():
        if row['Message'] == 'RRC Setup Request':
            # Step 3: Save C_RNTI and GNB_DU_UE_F1AP_ID to Identifier model
            identifier = Identifiers(
                C_RNTI=row['C_RNTI'],
                GNB_DU_UE_F1AP_ID=row['GNB_DU_UE_F1AP_ID']
            )
            identifier.save()

        # Step 4: Save the remaining data to the Message model
        message = Message(
            FrameNumber=row['FrameNumber'],
            FrameTime=row['FrameTime'],
            IpSrc=row['IpSrc'],
            IpDst=row['IpDst'],
            Protocol=row['Protocol'],
            F1_Proc=row['F1_Proc'],
            Message=row['Message']
        )
        message.identifiers = identifier  # Associate the message with the identifier
        message.save()

    def findF1OperationCode(self):
        rrcPrcedureName = "None"
        procedureCode = self.f1ap_packet.get('f1ap.procedureCode')
        config_handler = Ch(intName="f1ap", procCode=procedureCode, packetLayer=self.f1ap_packet)
        procedureName, rrcPrcedureName = config_handler.getProcedureName()
        if rrcPrcedureName is None:
            rrcPrcedureName = "None"
        if rrcPrcedureName != "unknownMessage" and rrcPrcedureName != "None":
            srcNode, dstNode = config_handler.getDirection(rrcPrcedureName)
        else:
            srcNode, dstNode = config_handler.getDirection(procedureName)

        return procedureName, rrcPrcedureName, srcNode, dstNode

    def create_association(self, main_table, assoc_key, src, dst, srcNode, dstNode):

        association, created = Associations.objects.get_or_create(assoc_key=assoc_key, src=src, dst=dst,
                                                                  src_type=srcNode, dst_type=dstNode, main=main_table)
        association.save()
        return association, created

    def create_message(self, main_table, message_key, f1ap_packet, assoc):

        message = Messages(message_key=message_key, association=assoc, message_json=f1ap_packet, main=main_table)
        message.save()
        return message

    def getRequiredKeysFromPacket(self, newFlag=False):
        c_rnti = self.f1ap_packet.get('f1ap.C_RNTI')
        du_f1ap_id = self.f1ap_packet.get('f1ap.GNB_DU_UE_F1AP_ID')
        cu_f1ap_id = self.f1ap_packet.get('f1ap.GNB_CU_UE_F1AP_ID')

        data = {
            "du_f1ap_id": du_f1ap_id,
            "cu_f1ap_id": cu_f1ap_id,
            "cp_e1ap_id": None,
            "up_e1ap_id": None,
            "cu_ngap_id": None,
            "amf_ngap_id": None,
            "cu_xnap_id": None,
            "nbr_xnap_id": None,
            "main_id": self.upload_id
        }

        if newFlag:
            data["crnti"] = c_rnti
            data["pci"] = self.f1ap_packet.get('nr-rrc.pdcch_DMRS_ScramblingID')

        return data

    def find_main_table_by_crnti_duid_cuid(self, crnti, duid, message_id):
        try:
            association = None
            main_table = MainTable.objects.get(crnti=crnti, du_f1ap_id=duid, cu_f1ap_id__isnull=False)

            if main_table:
                association = Associations.objects.filter(main=main_table).exclude(assoc_key=message_id).exists()
            return main_table, association
        except MainTable.DoesNotExist:
            return None, None

    def get_main_and_association(self, duid, message_id):
        try:
            main_table = MainTable.objects.get(du_f1ap_id=duid, cu_f1ap_id__isnull=True)
            # Check if the Associations table doesn't contain the specified message_id
            association = Associations.objects.filter(main=main_table, assoc_key=message_id).exists()
            if main_table and not association:
                return main_table, association
        except MainTable.DoesNotExist:
            return None, None

    def get_main_and_association_for_cuid_duid(self, duid, cuid, message_id):
        try:
            main_table = MainTable.objects.get(du_f1ap_id=duid, cu_f1ap_id=cuid)

            # Get associations that don't match the provided message_id
            associations = Associations.objects.filter(main=main_table).exclude(assoc_key=message_id).exists()

            if associations:
                return main_table, associations
            else:
                return None, None
        except MainTable.DoesNotExist:
            return None, None

    def handleAllF1AP(self):

        f1apProc, rrcProc, srcNode, dstNode = self.findF1OperationCode()

        if rrcProc != "None" and rrcProc != "unknownMessage":
            message_id = f'{rrcProc[0]}_{self.frame_number}_{self.frame_time}'
        elif rrcProc == "unknownMessage":
            infProcedure = f'{f1apProc}({rrcProc})'
            message_id = f'{infProcedure}_{self.frame_number}_{self.frame_time}'
        else:
            message_id = f'{f1apProc}_{self.frame_number}_{self.frame_time}'

        crnti = self.f1ap_packet.get('f1ap.C_RNTI')
        duid = self.f1ap_packet.get('f1ap.GNB_DU_UE_F1AP_ID')
        cuid = self.f1ap_packet.get('f1ap.GNB_CU_UE_F1AP_ID')
        src = self.f1ap_packet.get('ip.src')
        dst = self.f1ap_packet.get('ip.dst')

        main_table = None
        assoc = None

        # Check condition 1: CRNTI = crnti, DU_F1AP_ID = duid, CU_F1AP_ID = None
        if crnti and duid and message_id and not cuid:
            main_table, association = self.find_main_table_by_crnti_duid_cuid(crnti, duid, message_id)

        # Check condition 3: DU_F1AP_ID = duid, CU_F1AP_ID = cuid and message is not there
        if not main_table and duid and cuid:
            main_table, association = self.get_main_and_association_for_cuid_duid(duid, cuid, message_id)

        # Check condition 2: CRNTI = None, DU_F1AP_ID = duid, CU_F1AP_ID = cuid and message already not there

        if not main_table and not crnti and duid and cuid:
            main_table, association = self.get_main_and_association(duid, message_id)

        if rrcProc[0] == 'rrcSetupRequest':

            data = self.getRequiredKeysFromPacket(newFlag=True)

            if not main_table and not association:
                try:
                    main_table = MainTable.objects.get(**data)

                # Record already exists
                except MainTable.DoesNotExist:

                    # Record doesn't exist, create it
                    main_table = MainTable(**data)
                    main_table.save()
        else:
            data = self.getRequiredKeysFromPacket()

            if main_table:
                # Update the fields of the existing record if the data fields are not None
                for field, value in data.items():

                    if value is not None:
                        setattr(main_table, field, value)
                main_table.save()

        if main_table:

            # Check for duplicate associations and messages
            association_exists = Associations.objects.filter(main=main_table, assoc_key=message_id).exists()
            message_exists = Messages.objects.filter(main=main_table, message_key=message_id).exists()

            if not association_exists or not message_exists and association:
                assoc, created = self.create_association(main_table, message_id, src, dst, srcNode, dstNode)
                if assoc:
                    self.create_message(main_table, message_id, self.f1ap_packet, assoc=assoc)
