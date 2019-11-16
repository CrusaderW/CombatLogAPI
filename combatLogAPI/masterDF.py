import json
import numpy as np
import pandas as pd


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class masterDF(metaclass=Singleton):

    def __init__(self):
	    self.df = pd.DataFrame()

#Only a permanent solutions until calculation of live data will be done on masterDF...
    def getDataFrame(self):
        return pd.DataFrame(self.df, copy=True)

    def append(self, df):
        self.df = self.df.append(df)
        return


def getDamageDone(df):
    res = df.groupby('source').agg('sum').skillAmount.to_json()
    return (json.loads(res))

