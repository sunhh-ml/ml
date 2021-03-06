# !/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Time         : 2020/4/11 11:37
# @Author       : Huanhuan sun
# @Email        : sun58454006@163.com
# @File         : classfire_training_test.py
# @Software     : PyCharm
# @Project      : ml

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
from def_store import Net

EPOCH = 10
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
data_adress = 'E:\\ML_data\\CIFAR10\\'
#   Normalize第一个（）内表示图片RGB三通道的均值，第二个表示RGB三通道的标准差，若为自己的图片数据要自行计算，
#   或是采用pytorch的推荐值mean=[0.485， 0.456， 0.406]，std=[0.229, 0.224, 0.225]
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5),
                                                                            (0.5, 0.5, 0.5))])
#   通过torchvision工具下载CIFAR10数据到root指定文件夹里面(不用解压，程序会自动解压），若已有，则不会重复下载
#   若train为True则创建训练数据集，transform功能为变换
trainset = torchvision.datasets.CIFAR10(root=data_adress, train=True,
                                        download=True, transform=transform)
#   batch_size每批次进入多少数据，shuffle为True就打乱数据顺序，num_workers用多少个子进程加载数据，0表示默认在主进程中加载
#   这里num_workers需要设置为0，不然后面的dataiter = iter(trainloader)会报错
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=0)
testset = torchvision.datasets.CIFAR10(root=data_adress, train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=0)
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


# functions to show an image
def imshow(img):
    img = img / 2 + 0.5  # 因为之前标准化的时候除以0.5就是乘以2，还减了0.5，所以回复原来的亮度值（img*0.5（均值）-0.5（标准差））
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))  # 转置，改变索引顺序，即bgr转rgb，因为img.numpy读取后的三通道为BGR，要转成RGB
    plt.show()


# get some random training images
dataiter = iter(trainloader)
images, labels = dataiter.next()
# show images
# imshow(torchvision.utils.make_grid(images))  # 以格子形式显示多张图片
# # print labels
# print(' '.join('%5s' % classes[labels[j]] for j in range(4)))


# class Net(nn.Module):  # nn.Module是所有神经网络的基类，我们自己定义任何神经网络，都要继承nn.Module! 即class Net(nn.Module):
#     def __init__(self):
#         super(Net, self).__init__()  # 第二、三行都是python类继承的基本操作,此写法应该是python2.7的继承格式,但python3里写这个好像也可以
#         #  输入  3*32*32
#         self.conv1 = nn.Conv2d(3, 3, 3, stride=1, padding=0, dilation=1, groups=1)
#         self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1)
#         # self.conv2 = nn.Conv2d(64, 32, 3, padding=0)  # 32*13*13
#         # self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)  # 32*6*6
#         # self.conv3 = nn.Conv2d(32, 16, 3)   # 16*4*14
#         # self.pool3 = nn.MaxPool2d(2, 2)     # 16*2*2
#         self.fc1 = nn.Linear(16 * 2 * 2, 512)  # conv2输出16个通道，size为5*5,120自行设置
#         self.fc2 = nn.Linear(512, 128)  # 之所以使用84个神经元，是因为有人曾将 ASCII 码绘制于[12*7]的 bit-map 上，LeNet-5作者希望此层的输出有类似的效果
#         self.fc3 = nn.Linear(128, 10)  # 10是最后分类共10类，若为CIFAR100则为100
#
#     def forward(self, x):
#         x = x.to(device)
#         x = self.pool1(F.relu(self.conv1(x)))  # F是torch.nn.functional的别名，这里调用了relu函数 F.relu()
#         # x = self.pool2(F.relu(self.conv2(x)))
#         # x = self.pool3(F.relu(self.conv3(x)))
#         print(x.shape)
#         x = x.view(-1, 16 * 2 * 2)  # .view( )是一个tensor的方法，使得tensor改变size但是元素的总数是不变的。
#         #  那么为什么这里只关心列数不关心行数呢，因为马上就要进入全连接层了，而全连接层说白了就是矩阵乘法，
#         #  你会发现第一个全连接层的首参数是16*5*5，所以要保证能够相乘，在矩阵乘法之前就要把x调到正确的size
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x


net = Net()
criteria = nn.CrossEntropyLoss()

optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9, nesterov=False)
# optimizer = optim.Adam(net.parameters(), lr=0.001, betas=(0.9, 0.999))
for epoch in range(EPOCH):  # 所有数据遍历次数，相当于训练次数
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data[0].to(device), data[1].to(device)

        # zero the parameter gradients
        optimizer.zero_grad()
        # forward + backward + optimize
        outputs = net(inputs)
        loss = criteria(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:  # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('finish training')

#   保存训练模型
PATH = 'E:\\ML_data\\CIFAR10\\model\\cifar_net.pth'
torch.save(net.state_dict(), PATH)

#   测试部分
dataiter = iter(testloader)
images, labels = dataiter.next()
imshow(torchvision.utils.make_grid(images))
print('GroundTruth: ', ' '.join('%5s' % classes[labels[j]] for j in range(4)))

# #   重新保存
# net = Net()
# net.load_state_dict((torch.load(PATH)))

outputs = net(images)

_, predicted = torch.max(outputs, 1)
print('Predicted: ', ' '.join('%5s' % classes[predicted[j]] for j in range(4)))

#   查看网络对整个数据集的性能
correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))

#   查看哪些类表现好，哪些不好
class_correct = list(0. for i in range(10))  # 一共10类
class_totle = list(0. for i in range(10))
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs, 1)  # 返回每一行(0为列)中最大值的那个元素，且返回其索引
        c = (predicted == labels).squeeze()
        for i in range(4):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_totle[label] += 1

for i in range(10):
    print('Accuracy of %5s : %2d %%' % (classes[i], 100 * class_correct[i] / class_totle[i]))

#   重新保存
net = Net()
net.load_state_dict((torch.load(PATH)))