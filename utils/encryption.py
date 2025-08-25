def xor_encrypt_decrypt(data, key):
    """Simple XOR encryption/decryption"""
    key_bytes = key.encode("utf-8")
    data_bytes = data.encode("utf-8")
    encrypted_bytes = bytearray()
    for i, byte in enumerate(data_bytes):
        encrypted_bytes.append(byte ^ key_bytes[i % len(key_bytes)])
    return encrypted_bytes.decode("utf-8", errors="ignore")


