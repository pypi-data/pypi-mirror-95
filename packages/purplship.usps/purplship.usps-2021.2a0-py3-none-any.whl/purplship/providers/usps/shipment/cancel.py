from typing import Tuple, List
from usps_lib.evs_cancel_request import eVSCancelRequest
from usps_lib.evs_cancel_response import eVSCancelResponse
from usps_lib.evsi_cancel_request import eVSICancelRequest
from usps_lib.evsi_cancel_response import eVSICancelResponse
from purplship.core.utils import Serializable, Element, XP
from purplship.core.models import (
    ShipmentCancelRequest,
    ConfirmationDetails,
    Message
)

from purplship.providers.usps.error import parse_error_response
from purplship.providers.usps.utils import Settings


def parse_shipment_cancel_response(response: Element, settings: Settings) -> Tuple[ConfirmationDetails, List[Message]]:
    errors: List[Message] = parse_error_response(response, settings)
    if response.tag == 'eVSCancelResponse':
        cancel_response = XP.build(eVSCancelResponse, response)
    else:
        cancel_response = XP.build(eVSICancelResponse, response)

    if cancel_response.Status != "Cancelled":
        errors.append(Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            message=cancel_response.Reason,
            code=cancel_response.Status
        ))

    details = (
        ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            operation="Shipment Cancel",
            success=True,
        )
        if not any(errors) else None
    )

    return details, errors


def shipment_cancel_request(payload: ShipmentCancelRequest, settings: Settings) -> Serializable:

    if 'international' in payload.service:
        request = eVSICancelRequest(
            USERID=settings.username,
            BarcodeNumber=payload.shipment_identifier
        )
    else:
        request = eVSCancelRequest(
            USERID=settings.username,
            BarcodeNumber=payload.shipment_identifier
        )

    return Serializable(request)
