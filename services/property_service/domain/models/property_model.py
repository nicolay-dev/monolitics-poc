
class PropertyModel:
    def __init__(
            self,
            external_data: str,
            field_research: str,
            sales_context: str,
            # id_property: int = None,
    ): 
        # self.id_property = id_property
        self.external_data = external_data
        self.field_research = field_research
        self.sales_context = sales_context
    
    def to_dict(self):
        return {
            # "id_property": self.id_property,
            "external_data": self.external_data,
            "field_research": self.field_research,
            "sales_context": self.sales_context,
        }
    