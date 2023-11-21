from base64 import urlsafe_b64encode
from typing import Optional

from pytoniq_core import begin_cell

from .models import Transaction, TransactionMessage

__all__ = [
    "TONTransferTransaction",
    "NFTTransferTransaction",
]


class TONTransferTransaction(Transaction):
    """
    Create a TON (Telegram Open Network) transfer transaction.

    :param valid_until: The expiration timestamp for the transaction.
    :param address: The address to which the transfer is made.
    :param amount: The amount to be transferred.
    :param comment: An optional comment for the transaction.
    """

    def __init__(
            self,
            valid_until: int,
            address: str,
            amount: str,
            comment: Optional[str] = "",
    ) -> None:
        payload = urlsafe_b64encode(
            begin_cell()
            .store_uint(0, 32)
            .store_string(comment)
            .end_cell()
            .to_boc()
        ).decode()
        super().__init__(
            messages=[
                TransactionMessage(
                    address=address,
                    payload=payload,
                    amount=amount,
                ),
            ],
            valid_until=valid_until,
        )


class JettonTransferTransaction(Transaction):
    """
    Create a Jetton transfer transaction.

    :param valid_until: The expiration timestamp for the transaction.
    :param jetton_wallet_address: The address of the Jetton wallet.
    :param recipient_address: The recipient's address.
    :param response_address: The address for the response.
    :param jettons_amount: The amount of Jettons to be transferred.
    :param transfer_fee: The transfer fee amount.
    """

    def __init__(
            self,
            valid_until: int,
            jetton_wallet_address: str,
            recipient_address: str,
            response_address: str,
            jettons_amount: str,
            transfer_fee: str,
    ) -> None:
        payload = urlsafe_b64encode(
            begin_cell()
            .store_uint(0xf8a7ea5, 32)
            .store_uint(0, 64)
            .store_coins(jettons_amount)
            .store_address(recipient_address)
            .store_address(response_address or recipient_address)
            .store_uint(0, 1)
            .store_coins(1)
            .store_uint(0, 1)
            .end_cell()
            .to_boc()
        ).decode()
        super().__init__(
            messages=[
                TransactionMessage(
                    address=jetton_wallet_address,
                    payload=payload,
                    amount=transfer_fee,
                ),
            ],
            valid_until=valid_until,
        )


class NFTTransferTransaction(Transaction):
    """
    Create an NFT (Non-Fungible Token) transfer transaction.

    :param valid_until: The expiration timestamp for the transaction.
    :param nft_address: The address of the NFT.
    :param recipient_address: The recipient's address.
    :param response_address: The address for the response.
    :param transfer_fee: The transfer fee amount.
    """

    def __init__(
            self,
            valid_until: int,
            nft_address: str,
            recipient_address: str,
            response_address: str,
            transfer_fee: str,
    ) -> None:
        payload = urlsafe_b64encode(
            begin_cell()
            .store_uint(0x5fcc3d14, 32)
            .store_uint(0, 64)
            .store_address(recipient_address)
            .store_address(response_address or recipient_address)
            .store_uint(0, 1)
            .store_coins(1)
            .store_uint(0, 1)
            .end_cell()
            .to_boc()
        ).decode()
        super().__init__(
            messages=[
                TransactionMessage(
                    address=nft_address,
                    payload=payload,
                    amount=transfer_fee,
                ),
            ],
            valid_until=valid_until,
        )
