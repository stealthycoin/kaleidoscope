

class Menu:
    """Represents a menu.... god knows what this will entail"""


    def __init__(self):
        self.items = []

    def sortItems(self):
        self.items.sort(key=lambda x: x.placement)

    def addItem(self,item):
        self.items.append(item)

    def getItems (self):
        return self.items

    def show(self):
        """Render the menu"""
        html = "\n<ul id='nav'>\n"
        for item in self.items:
            html += item.show() + "\n"
        return html + "</ul>"

class MenuItem:
    """Represents a single menu item... god knows what this will entail"""

    def __init__(self, d):
        self.title = d["title"]
        self.link = d["link"]
        self.placement = d["placement"]
        
    def show(self):
        """Show a single menu item"""
        return "<li><a href=\"%s\">%s</a></li>" % (self.link, self.title)

