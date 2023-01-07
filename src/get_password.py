from model import get_model, predict
from src.cutter import cut_image
import requests
import io
from PIL import Image
from collections import Counter

URL = "https://www.freeopenvpn.org/premium.php?cntid={}"            
IMG_URL = "https://www.freeopenvpn.org/img/password.php"

def get_password_for_region(region, n=5):
    url = URL.format(region)
    images = []
    model = get_model()
    for i in range(n):
        page = requests.get(IMG_URL, headers={"referer": url})
        image_data = page.content
        image = Image.open(io.BytesIO(image_data))
        images.append(image)
    predicts = [predict(model, cut_image(img)) for img in images]
    best_predict = []
    for i in range(len(predicts[0])):
        c = Counter(predict[i] for predict in predicts)
        best_ans = max(c.items(), key=lambda x: x[1])
        best_predict.append(best_ans[0])
    return "".join(best_predict)

if __name__ == "__main__":
    # USA, UK, Russia-2, Russia-3, Germany, Netherlands
    region = "UK"

    password = get_password_for_region(region, n=5)
    print(password)
