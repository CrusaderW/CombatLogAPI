import sys
import json
from datetime import datetime
from flask import jsonify
from combatLogAPI import models, masterDF
from combatLogAPI.constants import ACTION_TYPES, SKILL_BY_ME, SKILL_TARGET_ME, \
        FOR_SPLITTER, EVENT_SPLITTER, CRITICAL_SUBSTRING


class LogStream:
    def __init__(self, json_data):
        json_data = json.loads(json_data)
        self.username = json_data['username']
        self.logs = json_data['logs']
        self.response = {'username': self.username}
        self.masterdf = masterDF.masterDF()
        self.df = masterDF.pd.DataFrame()

    def store(self):
        #store self.logs to MongoDB
        rawLogs = models.RawLogs(username=self.username, logs=self.logs)
        response = rawLogs.save()
        print(f'{self.username} uploaded {len(self.logs)} lines')
        return "Success"

    def parse(self):
        for log in self.logs:
            try:
                logLine = LogLine(log, self.username)
                parsedLogLine = logLine.parse()
                self.df = self.df.append(parsedLogLine, ignore_index = True)
            except Exception as e:
                print(e)
                print('Skipped parsing the following line due to an error.')
                print(log)
                #TODO: Write unhandled lines to logfile.
        self.masterdf.append(self.df)
        self.response['lines_parsed'] = len(self.df)
        self.response['lines_skipped'] = len(self.logs)-len(self.df)
        return self.response

    def get_response(self):
        self.response['parsed_logs'] = {}
        self.response["parsed_logs"]['damage_done'] = masterDF.getDamageDone(self.masterdf.getDataFrame())
        self.response["parsed_logs"]['damage_recieved'] = masterDF.getDamageRecieved(self.masterdf.getDataFrame())
        self.response["parsed_logs"]['healing_done'] = masterDF.getHealingDone(self.masterdf.getDataFrame())
        self.response["parsed_logs"]['healing_recieved'] = masterDF.getHealingRecieved(self.masterdf.getDataFrame())
        return self.response

class LogLine():

    def __init__(self, log, username):
        #TODO: Create unified models for JSON and MongoDocument
        self.username = username
        self.log = log
        self.model = {'columns': ['timestamp',
                                  'action',
                                  'source',
                                  'target',
                                  'skillName',
                                  'skillAmount',
                                  'damageType',
                                  'skillCritical',
                                  'username'],
                     }

        return

    def parse(self):
        eventPart = self.log.split(EVENT_SPLITTER)[1].strip()[0:-1]
        self.skillAction = self.getSkillAction(eventPart);
        if self.skillAction is None:
            print("[WARN] line was skipped cause action type not defined\n"+log)

        [skillByAndSkillNamePart,skillTargetAndSkillAmountPart] = self.getSplittedBySkillAction(eventPart)
        self.skillBy = self.getSkillBy(skillByAndSkillNamePart)
        self.skillName = self.getSkillName(skillByAndSkillNamePart)
        self.dateTime = self.getDateTime()
        self.skillTarget = self.getSkillTarget(skillTargetAndSkillAmountPart)
        self.skillAmount = self.getSkillAmount(skillTargetAndSkillAmountPart)
        self.skillCritical = self.isCritical(eventPart)
        self.damageType = self.getDamageType(skillTargetAndSkillAmountPart)
        self.json = self.get_json()
        return self.json

    def get_json(self):
        json_data = {}
        json_data['timestamp'] = self.dateTime
        json_data['action'] = self.skillAction
        json_data['source'] = self.skillBy
        json_data['target'] = self.skillTarget
        json_data['skillName'] = self.skillName
        json_data['skillAmount'] = self.skillAmount
        json_data['damageType']= self.damageType
        json_data['skillCritical'] = self.skillCritical
        json_data['username'] = self.username
        return json_data

    def getSkillAction(self, eventPart):
        for actionType in ACTION_TYPES:
            if (0 < eventPart.find(ACTION_TYPES[actionType])):
                return actionType
        print(f'ActionType not found: {eventPart}')
        return None

    def getSplittedBySkillAction(self, eventPart):
        return eventPart.split(ACTION_TYPES[self.skillAction])

    def isCritical(self, eventPart):
        return (0 < eventPart.find(CRITICAL_SUBSTRING))

    def getSkillBy(self, skillByAndSkillNamePart):
        if (skillByAndSkillNamePart.split(' ')[0] == SKILL_BY_ME):
            return self.username
        else:
            return skillByAndSkillNamePart.split(' ',1)[0]

    def getSkillName(self, skillByAndSkillNamePart):
        return skillByAndSkillNamePart.split(' ',1)[1]

    def getDateTime(self):
        return datetime.fromisoformat(self.log.split(' ',1)[0][0:-1])

    def getSkillTarget(self, skillTargetAndSkillAmountPart):
        if skillTargetAndSkillAmountPart.startswith('for '):
            return 'unknown'
        else:
            return skillTargetAndSkillAmountPart.split(FOR_SPLITTER,1)[0]

    def getSkillAmount(self, skillTargetAndSkillAmountPart):
        return int(skillTargetAndSkillAmountPart.split(' ')[1])

    def getDamageType(self, skillTargetAndSkillAmountPart):
        return skillTargetAndSkillAmountPart.split(' ')[2]
