from handlers import jsonfilehandler

# Handling XNAP messages

class XNAPHandler:
    def __init__(self,xnap_packet) -> None:
        self.xnap_packet = xnap_packet
    
    def FindXNOperationCode(self):
        procedureCode = self.xnap_packet.get('xnap.procedureCode')
        procedureName =  jsonfilehandler.getProcedureName("xnap",procCode=procedureCode, packetLayer=self.xnap_packet,)
        
    
    def InitialUL(self):
        
        pass
    def UpLinkMessages(self):
        pass
    def DownLinkMessages(self):
        pass
    def UeCtxtRequestResponse(self):
        pass
    def UeCtxtModRequestResponse(self):
        pass
    def UeCtxtReleaseCommandAndComplete(self):
        pass
