class R_Expr:
    def __init__(self,r_type,r_restrictions,r_set):
        self.expression_type = r_type
        self.restrictions = r_restrictions
        self.target_set = r_set
    def show(self,key):
        #always need this just to be able to retrieve things from database
        result = "from %s.models import %s\n" % (self.target_set.app,self.target_set.model)
        result += "qs = %s.objects.all()\n" % self.target_set.model
        result += self.restrictions.show()
        result += self.expression_type.showImports(self.target_set)
        result += self.expression_type.show(key,self.target_set)

        return result
        

class R_Type:
    def __init__(self,t):
        self.type_symbol = t

    def showImports(self, ts):
        if self.type_symbol == 'S':
            return "from %s.views import get%s\n" % (ts.app,ts.model)
        if self.type_symbol == 'F':
            return "from %s.forms import %sForm\n" % (ts.app,ts.model)

    def show(self,key,ts):
        result = "from django.template import RequestContext\n"
        result += "d['%s'] = " % key
        if self.type_symbol == 'S':
            result += "get%s(qs)\n" % ts.model
        if self.type_symbol == 'F':
            result += "render_to_string('form.html', {'title':'Create %s','action':'/api/%s/%s/create/','formFields':%sForm().as_p()},context_instance=RequestContext(request))\n" % (ts.model,ts.app,ts.model,ts.model)

        return result

class R_Restrictions:
    def __init__(self,restrictions):
        self.restrictions = restrictions

    def showEquality(self, r):
        """TODO: Needs to eventually deal with types"""
        return "qs = qs.filter(%s=%s)\n" % (r[0],r[2].replace('%','u_'))

    def show(self):
        #restrictions are a tuple (field,op,value) different ops imply different logic
        result = ""
        for restriction in self.restrictions:
            if restriction[1] == '=':
                result += self.showEquality(restriction)

        return result

class R_Set:
    def __init__(self,app,model):
        self.app = app
        self.model = model

    def show(self):
        return "(%s->%s)" %(self.app, self.model)

    
