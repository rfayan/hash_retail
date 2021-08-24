import logging
from os import environ

import grpc

from hash_retail.core.grpc import discount_pb2, discount_pb2_grpc

GRPC_SERVER_ADDRESS = f"{environ['GRPC_HOST']}:{environ['GRPC_PORT']}"


async def get_discount_percentage(product_id: int) -> float:
    async with grpc.aio.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = discount_pb2_grpc.DiscountStub(channel)
        response = await stub.GetDiscount(discount_pb2.GetDiscountRequest(productID=product_id))

    discount_percentage = round(response.percentage, 2)
    logging.debug("Discount percentage: %s", discount_percentage)

    return discount_percentage
