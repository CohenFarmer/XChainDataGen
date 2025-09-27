MAX_NUMERIC_30 = 10 ** 30

def extract_amount(payload_hex: str) -> int:
    payload = bytes.fromhex(payload_hex)

    payload_id = payload[0]
    amount_bytes = None

    if (payload_id == 1 or payload_id == 3):
        amount_bytes = payload[1:33]

    if amount_bytes is None:
        return None
    
    amount = int.from_bytes(amount_bytes, "big")
    if amount >= MAX_NUMERIC_30:
        return None
    # convert to integer
    return amount
