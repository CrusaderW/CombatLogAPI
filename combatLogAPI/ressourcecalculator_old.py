import pymongo
output,effect_found=dict(),False
client = pymongo.MongoClient("0.0.0.0")
mydb = client["Crowfall"]
mycol = mydb["Resources"]
full_dict=mycol.find_one({},{"_id": 0, "Items": 1})['Items']
rawResources=mycol.find_one({},{"_id": 0, "rawResources": 1})['rawResources']
class SingleItem:
    def __init__(self, data):
	#self.mongo=mongo
        self.item=data['item']
        self.options=data.get('options')
        self.final_output={}
        self.componentList=[]
    def calculate(self):
        def item_search(resource, effect=None):
            global effect_found
            if full_dict.get(resource)==None:
                retrieved=dict(filter(lambda item: resource in item[0], full_dict.items()))
            else:
                retrieved=full_dict.get(resource)
            if type(retrieved)==list: #This is only ever needed if a subdictionary value is an array.
                for element in retrieved:
                    if element in rawResources:
                        self.componentList.append([str(*element.keys()),element[str(*element.keys())]['amount']])
                    item_search(*element.keys(),effect)
            elif retrieved !={} and any(isinstance(value, int) for value in retrieved.values())==False: #Recursion end condition.
                for ingredient in retrieved:
                    try:
                        self.componentList.append([ingredient,retrieved[ingredient]['amount'],'P'])
                    except KeyError:
                        pass
                    try:
                        if (effect in retrieved[ingredient]):
                            effect_found=True
                            for key in retrieved[ingredient][effect]:
                                b=str(*key.keys())
                                if b in rawResources.keys():
                                    p_index=[i for i, item in enumerate(self.componentList) if 'P' in item]
                                    self.componentList.append([b,key[b]['amount']*self.componentList[p_index[-1]][1]] if p_index!=[] else [b,key[b]['amount']])
                        else:
                            if ingredient in rawResources.keys() or effect==None:
                                self.componentList.append([ingredient, retrieved[ingredient]['amount']])
                            try:
                                item_search(ingredient,effect)
                            except TypeError:
                                print('ErrorCode 1')
                                return f'{self.item} has no effect {self.options}'
                    except KeyError:
                        pass
            if (not effect_found) and (self.options !=None): return f'{self.item} has no effect {self.options}'
            else: return self.componentList #return self.put_in_dict(self.componentList)
        try:
            return self.put_in_dict(item_search(self.item,self.options))
        except IndexError:
            print('ErrorCode 2')
            return f'{self.item} has no effect {self.options}'
    def put_in_dict(self,array):
        master_array=[]
        for item in array:
            cleaned=[item[0],sum(x[1] for x in array if (x[0]==item[0] and 'P' not in x))]
            if cleaned not in master_array and cleaned[1]!=0: master_array.append(cleaned)
        for sub_array in master_array: output[sub_array[0]]=sub_array[1]
        self.final_output={self.item:output}
        return self.final_output
SingleItem({'item':'Longsword','options':'Attack Power &  Armor Pen Crushing'}).calculate()
#print(SingleItem({'item':'Longsword','options':'Attack Power &  Armor Pen Ice'}).calculate())
