
class PropertyModel:
    def __init__(
            self,
            externalData: str,
            fieldResearch: str,
            salesContext: str,
    ): 
        self.externalData = externalData
        self.fieldResearch = fieldResearch
        self.salesContext = salesContext
    
    def to_dict(self):
        return {
            "externalData": self.externalData,
            "fieldResearch": self.fieldResearch,
            "salesContext": self.salesContext,
        }
    