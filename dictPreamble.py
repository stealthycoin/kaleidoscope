class R_Expr:
    def __init__(self,r_type,r_restrictions,r_set):
        self.expression_type = r_type
        self.restrictions = r_restrictions
        self.target_set = r_set
class R_Type:
    def __init__(self,t):
        self.type_symbol = t
class R_Restrictions:
    def __init__(self,restrictions):
        self.restrictions = restrictions
class R_Set:
    def __init__(self,app,model):
        self.app = app
        self.model = model

    
