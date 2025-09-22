from abc import ABC, abstractmethod
import numpy as np
from matplotlib import pyplot as plt


class WaterRetentionModel(ABC):
    @abstractmethod
    def retention(self, psi):
        pass

    @abstractmethod
    def conductivity(self, psi):
        pass


class BrooksCorey(WaterRetentionModel):
    def __init__(self, psi_b, power_lambda):
        self.psi_b = psi_b
        self.power_lambda = power_lambda

    def retention(self, psi):
        return np.where(psi < self.psi_b, (self.psi_b / psi) ** self.power_lambda, 1)

    def conductivity(self, psi):
        return (self.psi_b / psi) ** (2 + 3 * self.power_lambda)


class vanGenuchten(WaterRetentionModel):
    def __init__(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def retention(self, psi):
        return 1 / (1 + (self.alpha * abs(psi)) ** self.beta) ** self.gamma

    def conductivity(self, psi):
        return (1 - (1 - (self.alpha * abs(psi)) ** self.beta) ** (self.gamma + 1)) ** 2 / (1 + (self.alpha * abs(psi)) ** self.beta) ** (self.gamma / 2)


if __name__ == "__main__":
    brooks_corey = BrooksCorey(psi_b=1e3, power_lambda=-1.13)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    psi = np.linspace(1, 5e3, 10000)
    ax.plot(psi, brooks_corey.retention(psi), label="Effective saturation")
    ax.set_xscale("log")
    ax.set_xlabel(r"Pressure head [kPa]")
    ax.set_ylabel(r"Water Saturation $S_e$ []")
    ax.grid(True)
    ax.set_title("Brooks-Corey (1966)")
    ax.legend()
    fig.savefig("image/brooks_corey.png", dpi=300, bbox_inches="tight")