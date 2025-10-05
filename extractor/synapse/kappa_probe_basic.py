from eth_utils import keccak, to_hex

tx = "0x2100d2b8ef97ecc9b13733f5e23b1fa31e39b9b989d85a59c872ef9fd790abde"
kappa = "0x438cbedd92973efae2d8fb47895f574349b52df6e7e260a7dffdd022e8ad1ff2"

print(to_hex(keccak(text=tx.lower())))
