import logging
from os import environ

import grpc

from hash_retail.core.grpc import discount_pb2, discount_pb2_grpc

GRPC_SERVER_ADDRESS = f"{environ['GRPC_HOST']}:{environ['GRPC_PORT']}"


async def get_discount_percentage(product_id: int) -> float:
    """Get product discount from gRPC service and return its percentage as a float value."""
    try:
        async with grpc.aio.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
            stub = discount_pb2_grpc.DiscountStub(channel)
            response = await stub.GetDiscount(discount_pb2.GetDiscountRequest(productID=product_id))
    except (grpc.aio.BaseError, grpc.RpcError) as grpc_error:
        # If gRPC Service is not available, log the error message and return 0% discount
        logging.warning("gRPC error: %s", grpc_error)
        return 0

    discount_percentage = round(response.percentage, 2)
    logging.debug("Discount percentage: %s", discount_percentage)

    return discount_percentage
