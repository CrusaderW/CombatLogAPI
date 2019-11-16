import json
import numpy as np
import pandas as pd
from combatLogAPI.constants import ACTION_TYPES


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
    res = df[df.action == "HIT"].groupby('source').agg('sum').skillAmount.to_json()
    print(res)
    return (json.loads(res))

def getDamageRecieved(df):
    res = df[df.action == "HIT"].groupby('target').agg('sum').skillAmount.to_json()
    print(res)
    return (json.loads(res))

def getHealingDone(df):
    res = df[df.action == "HEAL"].groupby('source').agg('sum').skillAmount.to_json()
    print(res)
    return (json.loads(res))

def getHealingRecieved(df):
    res = df[df.action == "HEAL"].groupby('target').agg('sum').skillAmount.to_json()
    print(res)
    return (json.loads(res))

