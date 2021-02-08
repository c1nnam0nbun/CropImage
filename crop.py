from PIL import Image

def crop_image_to_pdf():
    src_image: str = input("Name of source image: ")
    pdf_name: str = input("Name for created PDF: ")
    pg_amount: int = int(input("Amount of pages: "))

    im: Image = Image.open(r"D:\\screen\\" + src_image + ".png")

    width, height = im.size
    left, right, top, bottom = 0, 0, 0, 0

    pic_mode: str = input("Enter mode (normal, smaller, left, other): ")
    if pic_mode == "normal":
        incr: int = 706

        left: int = 207
        right: int = width - 191

        top: int = 5
        bottom: int = 703

    elif pic_mode == "smaller":
        incr: int = 531

        left: int = 323
        right: int = width - 307

        top: int = 5
        bottom: int = 529

    elif pic_mode == "left":
        incr: int = 706

        left: int = 10
        right: int = width - 387

        top: int = 5
        bottom: int = 703
    elif pic_mode == "other":
        incr: int = 632

        left: int = 257
        right: int = width - 240

        top: int = 5
        bottom: int = 630
    else:
        quit(0)

    futurePDF: list = []

    first_page: Image = None

    for i in range(pg_amount):
        slide: Image = im.crop((left, top, right, bottom))
        if i == 0:
            first_page = slide
        else:
            futurePDF.append(slide)
        top += incr
        bottom += incr

    for slide in futurePDF:
        slide.convert("RGB")

    first_page.convert("RGB")

    first_page.save(r"D:\\KPI\\IoT\\" + pdf_name + ".pdf", save_all=True, append_images=futurePDF)


def test_image_crop():
    src_image: str = input("Name of source image: ")

    im: Image = Image.open(r"D:\\screen\\" + src_image + ".png")

    width, height = im.size

    left, right, top, bottom = 0, 0, 0, 0

    pic_mode: str = input("Enter mode (normal, smaller, left, other): ")
    if pic_mode == "normal":
        incr: int = 706

        left: int = 207
        right: int = width - 191

        top: int = 5
        bottom: int = 703

    elif pic_mode == "smaller":
        incr: int = 531

        left: int = 323
        right: int = width - 307

        top: int = 5
        bottom: int = 529

    elif pic_mode == "left":
        incr: int = 706

        left: int = 10
        right: int = width - 387

        top: int = 5
        bottom: int = 703
    elif pic_mode == "other":
        incr: int = 632

        left: int = 257
        right: int = width - 240

        top: int = 5
        bottom: int = 630
    else:
        quit(0)

    slide: Image = im.crop((left, top, right, bottom))
    slide.show()


mode: int = int(input("1 - test\n2 - creation\nYour choice: "))

if mode == 1:
    test_image_crop()
elif mode == 2:
    crop_image_to_pdf()
