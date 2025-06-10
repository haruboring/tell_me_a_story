from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def main():
    for file_name in [
        "raw_dataset/tell-me-a-story-test_encrypted.jsonl",
        "raw_dataset/tell-me-a-story-train_encrypted.jsonl",
        "raw_dataset/tell-me-a-story-validation_encrypted.jsonl",
    ]:
        filename = file_name
        skey_file = "keys/skey.key"  # File containing the symmetrical key.
        pkey_file = "keys/private_key.pem"  # File containing the private key.

        # Load the private key.
        with open(pkey_file, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

        # Load the symmetrical key.
        with open(skey_file, "rb") as f:
            skey = f.read()

        # Load the file to decrypt.
        with open(filename, "rb") as f:
            data = f.read()

        # Decrypt the symmetrical key.
        unenc_skey = private_key.decrypt(  # type: ignore
            skey, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

        # Decrypt the data.
        f = Fernet(unenc_skey)
        decrypted = f.decrypt(data)

        # Write the data to file.
        out_file = filename.replace("_encrypted.jsonl", ".jsonl").replace("raw_dataset/", "dataset/")
        with open(out_file, "wb") as f:
            f.write(decrypted)


if __name__ == "__main__":
    main()
