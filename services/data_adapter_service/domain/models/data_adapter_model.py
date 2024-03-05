
class DataAdapterModel:
    def __init__(
            self,
            external_data: str,
            id_adapter: int = None,
    ): 
        self.id_adapter = id_adapter
        self.external_data = external_data
    
    def to_dict(self):
        return {
            "id_adapter": self.id_adapter,
            "external_data": self.external_data,
        }
    