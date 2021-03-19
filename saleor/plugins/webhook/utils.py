from typing import TYPE_CHECKING

from ...payment import TransactionKind
from ...payment.interface import GatewayResponse, PaymentData, PaymentMethodInfo

if TYPE_CHECKING:
    from requests.models import Response as RequestsResponse


def webhook_response_to_gateway_response(
    payment_information: "PaymentData", response: "RequestsResponse"
) -> "GatewayResponse":
    response_json = response.json()

    error = response_json.get("error")
    is_success = response.status_code == 200 and not error

    payment_method_info = PaymentMethodInfo(
        brand=response_json.get("payment_method_brand"),
        exp_month=response_json.get("payment_method_exp_month"),
        exp_year=response_json.get("payment_method_exp_year"),
        last_4=response_json.get("payment_method_last_4"),
        name=response_json.get("payment_method_name"),
        type=response_json.get("payment_method_type"),
    )

    return GatewayResponse(
        action_required=response_json.get("action_required", False),
        action_required_data=response_json.get("action_required_data"),
        amount=payment_information.amount,
        currency=payment_information.currency,
        customer_id=response_json.get("customer_id"),
        error=error,
        is_success=is_success,
        kind=TransactionKind.CAPTURE,
        transaction_id=response_json.get("transaction_id"),
        payment_method_info=payment_method_info,
        raw_response=response_json,
    )
