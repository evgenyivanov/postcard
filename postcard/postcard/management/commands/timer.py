from django.core.management.base import BaseCommand, CommandError
from postcard.models import Send, Body
from postcard.views import sending
import datetime

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        list = Send.objects.filter(send=0)
        for i in list:
            sending(str(i.id))
            self.stdout.write(str(i.send))
        list = Body.objects.all()
        for i in list:
            delta=(datetime.datetime.now()-i.date).seconds
            ls = Send.objects.filter(id = i.id)
            self.stdout.write(str(i.id))
            self.stdout.write(str(delta))
            if (len(ls)==0) and (delta > 500):
                i.delete()