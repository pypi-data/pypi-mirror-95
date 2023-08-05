from pvoutput_api.constants import ADD_STATUS_SERVICE_NAME, ADD_BATCH_STATUS_SERVICE_NAME
from pvoutput_api.services.common.common import Service
from pvoutput_api.services.status.add_batch_status_service import AddBatchStatusService
from pvoutput_api.services.status.add_status_service import AddStatusService


def create_service(name: str) -> Service:
    if name == ADD_STATUS_SERVICE_NAME:
        return AddStatusService()
    elif name == ADD_BATCH_STATUS_SERVICE_NAME:
        return AddBatchStatusService()
    else:
        raise TypeError("No service for name {}".format(name))
