import datetime
import json

from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from infinitystones.helpers.power_activation_helper import view_payload_validator, stone_current_status_check
from infinitystones.models import Stone, Activation
from infinitystones.tasks import activate_power


class StonesView(APIView):
    model = Stone
    permission_classes = [
        IsAuthenticated
    ]

    def get(self, *args, **kwargs):
        stones = Stone.objects.all()

        if not stones:
            stones = []

        data = serialize("json", stones, fields=["name"])
        return HttpResponse(data, content_type="applications/json")

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)

        if "name" not in data:
            return HttpResponseBadRequest("missing parameter name")

        comment = "New stone created"

        try:
            stone = Stone.objects.get(name=data['name'])
            comment = "stone already exists, not creating again"
        except Stone.DoesNotExist:
            stone = Stone.objects.create(**data)

        data = json.dumps({
            "comment": comment,
            "stone_id": stone.id,
            "name": stone.name
        })
        return HttpResponse(data, content_type="applications/json")


class ActivationView(APIView):
    model = Activation
    permission_classes = [
        IsAuthenticated
    ]

    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)

        # there is no need to do user validation, as it is part of the authenticated request itself.
        validation_comment = view_payload_validator(data)

        if validation_comment:
            return HttpResponseBadRequest(json.dumps({"comment": validation_comment}))

        stone = Stone(id=data['stone_id'])
        current_status_comment = stone_current_status_check(stone)

        if current_status_comment:  # if any comment was returned, it means stone is not in terminal state
            return HttpResponseBadRequest(json.dumps({"comment": current_status_comment}))

        # create new db entry
        activation = Activation.objects.create(
            stone_id=stone,
            duration=data['duration'],
            user=self.request.user,
            status='B',

            start_time=datetime.datetime.now(),
            end_time=datetime.datetime.now()
        )

        data = json.dumps({
            "comment": "successfully accepted stone activation request",
            "task_id": activation.id
        })
        activate_power.delay(activation_entry_id=activation.id)

        return HttpResponse(data, content_type="application/json")
