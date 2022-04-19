from PIL import Image
import os
import string, random


def rnd_str():
    alph = string.hexdigits
    return "".join([random.choice(alph) for i in range(10)]).lower()

def cut_image(img):
    w, h = img.size
    step = (w - 2) // 9
    res = []
    for i in range(1, w - step, step):
        cim = img.crop((i, 0, i + step, h))
        res.append(cim)
    return res

if __name__ == "__main__":
    image_types = [
        "679046356",
        "966187942"
    ]

    images = {k: sorted(os.listdir(f"data/{k}")) for k in image_types}
    os.makedirs("data/prepared", exist_ok=True)
    for i in range(10):
        os.makedirs(f"data/prepared/{i}", exist_ok=True)

    for im_type, files in images.items():
        for file in files:
            print(file)
            digs = cut_image(Image.open(f"data/{im_type}/{file}"))
            for dig, img in zip(im_type, digs):
                img.save(f"data/prepared/{dig}/{rnd_str()}.png")
