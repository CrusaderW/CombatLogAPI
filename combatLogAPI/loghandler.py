import sys
import json
from datetime import datetime, date
from flask import jsonify
from combatLogAPI import masterDF
from combatLogAPI.constants import ACTION_TYPES, SKILL_BY_ME, SKILL_TARGET_ME, \
        FOR_SPLITTER, EVENT_SPLITTER, CRITICAL_SUBSTRING


class LogQuery:
    def __init__(self, mongo):
        self.mongo = mongo

    def getAllLogsInDateTimeWindow(self, date):
        response = []
        for entry in self.mongo.db.raw_logs.find({'date': date}):
            #print(f"{entry['username']}: {entry['filename']}")
            response.append({'username': entry['username'],'logs': entry['logs']})
        print(f'Returned {len(response)} chunks of raw logfiles')
        return {'data':response}

    def getAllParsedLogsInDateTimeWindow(self, date):
        response = {'logs': []}
        for entry in self.mongo.db.parsed_logs.find({'date': date}):
            #print(f"{entry['username']}: {entry['filename']}")
            response = {'logs': entry['logs']}
        print(f"Returned {len(response['logs'])} parsed loglines")
        return response

class LogStream:
    def __init__(self, json_data, mongo):
        self.mongo = mongo
        json_data = json.loads(json_data)
        self.username = json_data['username']
        self.filename = json_data['filename']
        self.logs = json_data['logs']
        self.response = {'username': self.username}
        self.parsedLogs = []

    def store(self):
        #store self.logs to MongoDB
        rawLogs = self.mongo.db.raw_logs.find_one({"username": self.username, "filename": self.filename})
        #print(rawLogs)
        if rawLogs is None:
            result = self.mongo.db.raw_logs.insert_one(
                {'username': self.username,
                'filename': self.filename,
                'date': self.logs[-1][:10],
                'logs': self.logs})
            if result.acknowledged:
                print(f"{self.username} uploaded {len(self.logs)} lines (new Logfile)")
            else:
                print('An error occured creating logs from {self.username}: {self.filename}')
        else:
            distinctLogs = list(set(rawLogs['logs'] + self.logs))
            result = self.mongo.db.raw_logs.replace_one({"username": self.username, "filename": self.filename},
                {'username': self.username,
                'filename': self.filename,
                'date': rawLogs['date'],
                'logs': distinctLogs})
            if result.acknowledged:
                print(f"{self.username} uploaded {len(distinctLogs)-len(rawLogs['logs'])} lines (total: {len(distinctLogs)})")
            else:
                print('An error occured appending logs from {self.username}: {self.filename}')
        return "Success"

    def parse(self):
        allParsedLogs = self.mongo.db.parsed_logs.find_one({"date": date.today().strftime('%Y-%m-%d')})
        for log in self.logs:
            try:
                logLine = LogLine(log, self.username)
                parsedLogLine = logLine.parse()
                print(parsedLogLine)
                self.parsedLogs.append(parsedLogLine)
            except Exception as e:
                print(f'\nSkipped parsing the following line due to an error: {e}')
                print(log)
        if allParsedLogs:
            self.parsedLogs = allParsedLogs['logs'] + self.parsedLogs
        response = self.mongo.db.parsed_logs.replace_one({"date": date.today().strftime('%Y-%m-%d')},
                {'date': date.today().strftime('%Y-%m-%d'),
                'logs': self.parsedLogs},
                upsert=True)
        return "Success"

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
        return int(skillTargetAndSkillAmountPart.split(' for ')[1].split(' ')[0])

    def getDamageType(self, skillTargetAndSkillAmountPart):
        return skillTargetAndSkillAmountPart.split(' for ')[1].split(' ')[1]
