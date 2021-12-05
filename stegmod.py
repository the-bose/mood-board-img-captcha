from stegano import lsbset
from stegano.lsbset import generators
from io import BytesIO
import base64

def encode(image, secret_message):
    secret = lsbset.hide(image, secret_message, generators.eratosthenes())
    new_fname = f"static/outputs/encoded_{image.split('/')[-1]}"
    secret.save(new_fname)
    # b64 of encoded image
    buffered = BytesIO()
    secret.save(buffered, format='PNG')
    b64_bytes = base64.b64encode(buffered.getvalue())
    b64_str = b64_bytes.decode('ascii')
    return (new_fname, b64_str)

def decode(new_fname):
    clear_message = lsbset.reveal(new_fname, generators.eratosthenes())
    return clear_message

if __name__ == '__main__':
    image = input("Enter the filename(with extension) to be encoded : ")
    secret_message = input("Enter the secret message : ")
    (new_fname, _) = encode(image, secret_message)
    # new_fname = "static/outputs/encoded_7ffccfbc35714c44a6a172e85e274f22.jpg"
    print(decode(new_fname))
