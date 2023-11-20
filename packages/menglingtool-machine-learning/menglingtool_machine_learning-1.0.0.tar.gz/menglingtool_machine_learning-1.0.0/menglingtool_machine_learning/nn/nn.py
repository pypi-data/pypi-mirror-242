import torch
from torch import nn


class NNer:
    def __init__(self, in_dim: int, out_dim: int, mid_dim: int = 32, mid_num=1, if_out_sigmoid=True):
        self.in_dim = in_dim
        self.out_dim = out_dim
        ceils = [nn.Linear(in_dim, mid_dim), nn.Sigmoid()]
        for _ in range(mid_num - 1):
            ceils.append(nn.Linear(mid_dim, mid_dim))
            ceils.append(nn.Sigmoid())
        ceils.append(nn.Linear(mid_dim, out_dim))
        if if_out_sigmoid: ceils.append(nn.Sigmoid())
        self.model = nn.Sequential(*ceils)

    def train(self, X, Y, learn_step=1e-2, train_num=100, loss_print=False):
        X, Y = torch.FloatTensor(X), torch.FloatTensor(Y)
        # 进入训练状态
        self.model.train()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=learn_step)
        loss_fn = nn.MSELoss()
        for i in range(train_num):
            Y0 = self.model(X)
            # 更新参数
            loss = loss_fn(Y0, Y)
            # loss.requires_grad_(True)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if loss_print and i % 10 == 0: print('loss:', loss.item())

    def predict(self, X, return_index=True):
        X = torch.FloatTensor(X)
        # 进入验证状态
        self.model.eval()
        # 仅验证不更新模型
        with torch.no_grad():
            # 转换为Tensor
            Y = self.model(X)
            if return_index:
                return [y.argmax().item() for y in Y]
            else:
                return Y


if __name__ == '__main__':
    nner = NN(4, 2)
    inputer = [[1, 2, 3, 4], [4, 3, 2, 1]]
    print(nner.predict(inputer, return_index=False))
    nner.train(inputer, [[1, 0], [0, 1]], learn_step=0.01, loss_print=True, train_num=20)
    print(nner.predict(inputer, return_index=False))
