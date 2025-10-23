import qrcode
from PIL import Image
import qrcode.constants
qr = qrcode.QRCode(version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_H,
                   box_size=10,border=12,)
qr.add_data("https://www.linkedin.com/in/krish-sharma-212325282?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")
qr.make(fit=True)
img=qr.make_image(back_color="grey",fill_color="blue")
img.save("kisu_likedin.png")