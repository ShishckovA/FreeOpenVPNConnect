import os
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
from cutter import cut_image

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class AlexResNet(nn.Module):
    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.conv1 = AlexResNet.block(in_channels, 64)
        self.conv2 = AlexResNet.block_with_pooling(64, 128)
        self.layer1 = AlexResNet.residual_block(128)
        self.conv3 = AlexResNet.block_with_pooling(128, 256)
        self.conv4 = AlexResNet.block_with_pooling(256, 256)
        self.layer2 = AlexResNet.residual_block(256)
        self.conv5 = AlexResNet.block_with_pooling(256, 512)
        self.conv6 = AlexResNet.block_with_pooling(512, 512)
        self.layer3 = AlexResNet.residual_block(512)
        self.clf = AlexResNet.classifier(512, num_classes)

    def forward(self, inp):
        out = self.conv2(self.conv1(inp))
        out = self.layer1(out) + out
        out = self.conv4(self.conv3(out))
        out = self.layer2(out) + out
        out = self.conv6(self.conv5(out))
        out = self.layer3(out) + out
        out = self.clf(out)
        return out

    @staticmethod
    def block(in_channels, out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    @staticmethod
    def block_with_pooling(in_channels, out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2)
        )

    @staticmethod
    def residual_block(channels):
        return nn.Sequential(
            AlexResNet.block(channels, channels),
            AlexResNet.block(channels, channels)
        )

    @staticmethod
    def classifier(in_channels, n_classes):
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(in_channels, n_classes)
        )

    def copy(self, deep=False):
        return AlexResNet(3, 10)


def get_model(path=f"{DIR_PATH}/model/captcha_solver"):
    model = AlexResNet(3, 10)
    model.load_state_dict(torch.load(path, map_location="cpu"))
    return model.eval()


def predict(model, imgs):
    pr_transforms = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize(mean=0.5, std=0.5)
    ])
    result = []
    for dig in map(pr_transforms, imgs):
        dig_pt = dig[None, :, :]
        predicted_label = model(dig_pt).argmax().item()
        result.append(str(predicted_label))
    return result


if __name__ == "__main__":
    image = Image.open("password.png")
    digs = cut_image(image)
    model = get_model()
    print(predict(model, digs))
