import datetime

import pytz
from celery import shared_task
from infinitystones.models import Activation
from infinitystones.utils.terminal_color import TerminalColor

# TODO: move all the ORM logic to a different package for easy code maintenance
batch_tasks = 0

@shared_task()
def activate_power(activation_entry_id):
    activation = Activation.objects.get(id=activation_entry_id)
    activation.start_time = datetime.datetime.now(tz=pytz.UTC)
    activation.end_time = datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(seconds=activation.duration)
    activation.status = 'A'
    activation.save()
    comment = f"Activated power for the stone: {activation.stone_id.id}; duration: {activation.duration}, end_time: {activation.end_time}"
    print(TerminalColor.OKGREEN + comment + TerminalColor.ENDC)


@shared_task()
def batch_deactivate_power():
    global batch_tasks
    updated_row_count = Activation.objects.filter(end_time__lt=datetime.datetime.now(tz=pytz.UTC), status='A').update(status='S')

    if updated_row_count > 0:
        print(TerminalColor.HEADER + f"Stone power deactivation, number of stones deactivated: {updated_row_count}" + TerminalColor.ENDC)
        batch_tasks = 0
    else:
        batch_tasks += 1
        if batch_tasks % 30 == 0:
            print(TerminalColor.HEADER + f"No stones found for deactivation, processed deactivation empty tasks: {batch_tasks}" + TerminalColor.ENDC)
