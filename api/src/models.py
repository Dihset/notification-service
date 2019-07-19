import datetime
from schematics.models import Model
from schematics.types import StringType, EmailType, DateTimeType
from schematics.exceptions import ValidationError


class Notification(Model):

    name = StringType(required=True, max_length=100)
    text = StringType(required=True)
    email = EmailType(required=True)
    date = DateTimeType(required=True)

    def validate_date(self, data, value):
        if value >= datetime.datetime.now():
            return value
        else:
            raise ValidationError(u'Date and time less than the current')
