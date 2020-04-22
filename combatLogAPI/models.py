import mongoengine as me

class RawLogs(me.Document):
    username = me.StringField()
    logs = me.ListField()

class CombatLogSchema(me.EmbeddedDocument):
    username = me.StringField()

    logId = me.StringField(primary_key=True)
    skillAction = me.StringField()
    skillName = me.StringField()
    dateTime = me.DateTimeField()
    skillBy = me.StringField()
    skillTarget = me.StringField()
    damageType = me.StringField()
    skillAmount = me.IntField()
    skillCritical = me.BooleanField()

class LocationSchema(me.EmbeddedDocument):
    campaign = me.StringField()
    zone = me.StringField()
    POI = me.StringField()

class FightSchema(me.Document):
    logs = me.ListField(me.EmbeddedDocumentField(CombatLogSchema))
    location = me.EmbeddedDocumentField(LocationSchema)

    datetimeStart = me.DateTimeField()
    datetimeEnd = me.DateTimeField()
    teams = me.ListField(me.StringField())
