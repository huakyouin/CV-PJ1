from ..layers.activation import Softmax
import numpy as np

#交叉熵损失函数
class CrossEntropyLoss(object):
    def __init__(self):
        # 内置一个softmax作为分类器
        self.classifier = Softmax()

    def gradient(self):
        return self.grad

    def __call__(self, a, y, requires_acc=True):
        '''
        a: 批量的样本输出
        y: 批量的样本真值
        requires_acc: 是否输出正确率
        return: 该批样本的平均损失[, 正确率]

        输出与真值的shape是一样的，并且都是批量的，单个输出与真值是一维向量
        a.shape = y.shape = (N, C)      N是该批样本的数量，C是单个样本最终输出向量的长度
        '''
        # 这里封装了softmax，所以网络的输出不应该再经过softmax
        a = self.classifier.forward(a)
        # 提前计算好梯度
        self.grad = a - y
        # 样本的平均损失
        loss = -1 * np.einsum('ij,ij->', y, np.log(a+ 1e-5), optimize=True) / y.shape[0]
        if requires_acc:
            acc = np.argmax(a, axis=-1) == np.argmax(y, axis=-1)
            return acc.mean(), loss
        return loss