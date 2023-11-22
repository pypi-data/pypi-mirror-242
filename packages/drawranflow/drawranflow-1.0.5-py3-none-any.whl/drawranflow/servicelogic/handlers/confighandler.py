import json


def open_file(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return f"File Nor found {file_name}"
    return data


class ConfigHandler:
    procedureName = None

    def __init__(self,intName,procCode,packetLayer):
        self.intName = intName
        self.procCode = procCode
        self.packetLayer = packetLayer


    def getProcedureName(self):
        config_file = f'drawranflow/servicelogic/intfconfig/{self.intName}_proc.json'

        data = open_file(file_name=config_file)
        # Load JSON data from a file
        procCode = f'{self.procCode}'
        # Value to check
        if procCode in data[self.intName]:

            proc_names = data[self.intName].get(self.procCode)
            procedureName = (name for name in proc_names if name in self.packetLayer.values())
            for procedureName in procedureName:
                if "nr-rrc.message" in self.packetLayer.keys():
                    rrcProcedureName = self.getrrcNAS()

                    return procedureName, rrcProcedureName

                else:
                    return procedureName, None
        else:
            return "No proc code found"
        del data

    def getNgapMessages(self):
        nas_file = f'drawranflow/servicelogic/intfconfig/nas_proc.json'
        ngap_file = f'drawranflow/servicelogic/intfconfig/ngap_proc.json'
        mm = self.packetLayer.get("nas-5gs.mm.message_type", "").upper()

        sm = self.packetLayer.get("nas_5gs.sm.message_type", "").upper()
        nas = open_file(nas_file)
        ng = open_file(ngap_file)
        print(mm,sm)
        mm = f'{mm}'
        sm = f'{sm}'
        procCode = f'{self.procCode}'

        if nas.get(mm) is not None:
            return nas[mm]
        elif nas.get(sm) is not None:
            return nas[sm]
        else:
            proc_names = ng.get(procCode)
            if proc_names:
                procedureName = (name for name in proc_names if name in self.packetLayer.values())
                for procedureName in procedureName:
                    if procedureName in self.packetLayer.values():
                        procedureName = procedureName
                        break
            return f'ngap{procedureName}'

    def getDirection(self,message):
        direction = f'drawranflow/servicelogic/intfconfig/msg_directions.json'

        direct = open_file(direction)

        if isinstance(message, list):
            message = message[0]
        directions = direct.get(message)

        return directions["src"], directions["dst"]

    def getrrcNAS(self):
        rrc_config = f'drawranflow/servicelogic/intfconfig/rrc_proc.json'
        rrc = open_file(rrc_config)
        for key, value in self.packetLayer.items():
            modified_value = value.replace('-', '_')
            if modified_value in rrc.keys():
                c1_value = self.packetLayer.get('nr-rrc.c1')
                c2_value = self.packetLayer.get('nr-rrc.c2')
                if c1_value is not None:
                    rrcProcedure = rrc[modified_value].get('c1').get(c1_value)

                    return rrcProcedure
                elif c2_value is not None:
                    rrcProcedure = rrc[modified_value].get('c2').get(c2_value)
                    return rrcProcedure
                else:
                    return "unknownMessage"
