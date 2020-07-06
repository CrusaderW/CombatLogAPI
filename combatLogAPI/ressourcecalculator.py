# Code goes here:

class SingleItem:
    def __init__(self, data, mongo):
        self.mongo = mongo

        #self.itemName = data.

        #self.options =
        self.response = {'reponse': 'success'}

    def calculate(self):
        print('This is a test')
        return self.response
