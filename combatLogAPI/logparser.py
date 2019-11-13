import sys
from datetime import datetime
from flask import jsonify
from combatLogAPI import models
from combatLogAPI.constants import ACTION_TYPES, SKILL_BY_ME, SKILL_TARGET_ME, \
        FOR_SPLITTER, EVENT_SPLITTER, CRITICAL_SUBSTRING

class LogStream:

    def __init__(self, json_data):
        self.datetimeStart = json_data['datetimeStart']
        self.datetimeEnd = json_data['datetimeEnd']
        self.username = json_data['username']
        self.logs = json_data['logs']

    def parse(self):
        parsedLogStream = []
        for log in self.logs:
            #try:
                logLine = LogLine(log['Value'], self.username)
                parsedLogLine = logLine.parse()
                #parsedLogStream.append(parsedLogLine)
            #except Exception as e:
            #    print(e)
            #    print('Skipped parsing the following line due to an error.')
                print(log['Value'])
                #TODO: Write unhandled lines to logfile.
        #response = jsonify(parsedLogStream)
        #print(response)
        response = {
            "friendly":[
                    {
                        "username": "GeneralMolan",
                        "total_damage": 196
                    }
            ]
        }
        return response

class LogLine():

    def __init__(self, log, username):
        #TODO: Create unified models for JSON and MongoDocument
        self.username = username
        self.log = log
        return

    def parse(self):

        self.skillAction = self.getSkillAction();
        #print(self.skillAction)
        if self.skillAction is None:
            print("[WARN] line was skipped cause action type not defined\n"+log)

        eventPart = self.log.split(EVENT_SPLITTER)[1].strip()[0:-1]
        #print(eventPart)
        [skillByAndSkillNamePart,skillTargetAndSkillAmountPart] = self.getSplittedBySkillAction(eventPart)
        #print([skillByAndSkillNamePart,skillTargetAndSkillAmountPart])
        self.skillBy = self.getSkillBy(skillByAndSkillNamePart)
        #print(self.skillBy)
        self.skillName = self.getSkillName(skillByAndSkillNamePart)
        #print(self.skillName)
        self.dateTime = self.getDateTime();
        #print(self.dateTime)
        self.skillTarget = self.getSkillTarget(skillTargetAndSkillAmountPart)
        #print(self.skillTarget)
        self.skillAmount = self.getSkillAmount(skillTargetAndSkillAmountPart)
        print(self.skillAmount)
        self.skillCritical = self.isCritical(eventPart);
        #print(self.skillCritical)
        return

    def getSkillAction(self):
        return 'HIT'

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
        return skillTargetAndSkillAmountPart.split(FOR_SPLITTER,1)[0]

    def getSkillAmount(self, skillTargetAndSkillAmountPart):
        return skillTargetAndSkillAmountPart.split(FOR_SPLITTER,1)[1].split(' ')[0]
