import qrcode
import qrcode.constants
qrcode=qrcode.QRCode(
    version=12,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    border=12,
    box_size=16
)
qrcode.make(fit=True)
qrcode.add_data("https://www.linkedin.com/in/krish-sharma-212325282?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app")
img = qrcode.make_image(fill_color="black",back_color="white")
img.save("myInfo.png")