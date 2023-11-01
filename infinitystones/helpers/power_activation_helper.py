import datetime

import pytz
from django.db import connection


def view_payload_validator(data):
    comment = "missing parameter: "
    missing_params = False

    if "stone_id" not in data:
        comment += " stone_id"
        missing_params = True

    if "duration" not in data:
        comment += " duration"
        missing_params = True

    if missing_params:
        return comment

    return None


def stone_current_status_check(stone):
    # here we are accomplishing two things at once,
    # 1. check whether the given stone_id is valid or not
    # 2. if the stone_id is valid, is any non-terminal power activation request is already there in the db
    # currently just writing raw SQL query, however the same SQL logic maybe possible to be handled using Django ORM
    # TODO: check if the below SQL query can be converted to django orm query - Note: cannot make two db calls.
    with connection.cursor() as cursor:
        cursor.execute(f"""
            select s.id, a.status, a.end_time
            from infinitystones_stone s
            left join infinitystones_activation a on s.id = a.stone_id_id
            where s.id='{stone.id}'
            order by a.status, a.end_time desc
            limit 1
            -- status ordering A, F, S ; we only care about the first row
        """)

        row = cursor.fetchone()

        if not row:
            return f"Stone doesn't exist; stone_id: {stone.id}"

        status = row[1]
        end_time = row[2]

        if status == 'A':  # this stone is already activated
            filler = str((end_time - datetime.datetime.now(tz=pytz.UTC)).total_seconds()) + " seconds"
        elif status == 'B':  # another activation request is already received, but worker hasn't activated the stone yet.
            filler = "some"
        else:
            return None

        return f"stone is currently being processed by other request, please try after {filler} time"
