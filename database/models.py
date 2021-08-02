from mongoengine import fields

import mongoengine
import datetime


class User(mongoengine.Document):
    discord_id = fields.LongField(required=True, primary_key=True)
    join_date = fields.DateTimeField(default=datetime.datetime.now)
    level = fields.IntField(default=1, min_value=0)
    experience = fields.IntField(default=0, min_value=0, max_value=100)
    on_server = fields.BooleanField(default=True)
    is_banned = fields.BooleanField(default=False)
    is_prisoned = fields.BooleanField(default=False)

    @property
    def bans(self):
        return Ban.objects(user=self.discord_id)\
            .order_by('-date')

    @property
    def imprisonments(self):
        return Imprisonment.objects(user=self.discord_id)\
            .order_by('-date')

    def update(self, **kwargs):
        super().update(**kwargs)
        self.reload()

    def ban(self, reason=None):
        if not self.is_banned:
            ban = Ban(user=self, reason=reason)
            ban.save()

            self.is_banned = True
            self.save()
        else:
            raise ValueError('User already banned')

    def unban(self):
        if self.is_banned:
            ban = self.bans[0]
            ban.set_inactive()
            self.is_banned = False
            self.save()
        else:
            raise ValueError('User is not banned')

    def imprison(self, reason=None):
        if not self.is_prisoned:
            imprisonment = Imprisonment(user=self, reason=reason)
            imprisonment.save()

            self.is_prisoned = True
            self.save()
        else:
            raise ValueError('User already prisoned')

    def end_imprisonment(self):
        if self.is_prisoned:
            imprisonment = self.imprisonments[0]
            imprisonment.set_inactive()

            self.is_prisoned = False
            self.save()
        else:
            raise ValueError('User is not prisoned')

    meta = {'db_alias': 'default', 'collection': 'users'}


class Ban(mongoengine.Document):
    date = fields.DateTimeField(default=datetime.datetime.now)
    end_date = fields.DateTimeField(null=True)
    reason = fields.StringField(null=True)
    is_active = fields.BooleanField(default=True)
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)

    def set_inactive(self):
        self.is_active = False
        self.end_date = datetime.datetime.now()
        self.save()

    meta = {'db_alias': 'default', 'collection': 'bans'}


class Imprisonment(mongoengine.Document):
    user = fields.ReferenceField(User, reverse_delete_rule=mongoengine.CASCADE)
    date = fields.DateTimeField(default=datetime.datetime.now)
    end_date = fields.DateTimeField(null=True)
    is_active = fields.BooleanField(default=True)
    reason = fields.StringField(null=True)

    def set_inactive(self):
        self.is_active = False
        self.end_date = datetime.datetime.now()
        self.save()

    meta = {'db_alias': 'default', 'collection': 'imprisonments'}
