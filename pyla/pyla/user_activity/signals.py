from django.db.models import signals as signals
from django.dispatch import receiver
from django.http import HttpResponse

from pyla.manage_profiles.models import ContactUs


@receiver(signals.pre_save, sender=ContactUs)
def feedback_sent(**kwargs):
    print("")
