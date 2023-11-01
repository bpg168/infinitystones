import datetime

import pytz
from celery import shared_task
from infinitystones.models import Activation
from infinitystones.utils.terminal_color import TerminalColor


@shared_task()
def activate_power(activation_entry_id):
    activation = Activation.objects.get(id=activation_entry_id)
    activation.start_time = datetime.datetime.now()
    activation.end_time = datetime.datetime.now() + datetime.timedelta(seconds=activation.duration)
    activation.status = 'A'
    activation.save()
    comment = f"Activated power for the stone; duration: {activation.duration}, end_time: {activation.end_time}"
    print(TerminalColor.OKGREEN + comment + TerminalColor.ENDC)


@shared_task()
def batch_deactivate_power():
    print(TerminalColor.HEADER + "Periodic power deactivation status..." + TerminalColor.ENDC)
    updated_row_count = Activation.objects.filter(end_time__lt=datetime.datetime.now(tz=pytz.UTC), status='A').update(status='S')

    if updated_row_count > 0:
        print(TerminalColor.OKGREEN + f"Number activation tasks completed and marked as Success: {updated_row_count}" + TerminalColor.ENDC)
    else:
        print(TerminalColor.OKCYAN + "Zero outdated activations found" + TerminalColor.ENDC)
    print(TerminalColor.HEADER + "Periodic power deactivation completed..." + TerminalColor.ENDC)
