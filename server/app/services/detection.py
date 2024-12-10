import torch
import torch.nn as nn

class VGG11(nn.Module):
  """Implements VGG11 architecture"""
  def __init__(self, in_channels, num_classes=2):
    """
    Constructor for VGG11 neural network

    Args:
      in_channels(int) : number of input channels
      num_classes(int, optional) : number of classes to classify into
    """
    super(VGG11, self).__init__()
    self.in_channels = in_channels
    self.num_classes = num_classes

    self.conv_layers = nn.Sequential(
        nn.Conv2d(in_channels, 64, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2),
        nn.Conv2d(64, 128, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2),
        nn.Conv2d(128, 256, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.Conv2d(256, 256, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2),
        nn.Conv2d(256, 512, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.Conv2d(512, 512, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2),
        nn.Conv2d(512, 512, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.Conv2d(512, 512, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2)
    )

    self.flatten = nn.Flatten()

    self.linear_layers = nn.Sequential(
        nn.Linear(in_features=512 * 7 * 7, out_features=4096), # 224 / 2**5 = 7
        nn.ReLU(), nn.Dropout2d(p=0.5),
        nn.Linear(in_features=4096, out_features=4096),
        nn.ReLU(), nn.Dropout2d(p=0.5),
        nn.Linear(in_features=4096, out_features=self.num_classes)
    )

  def forward(self, X):
    """
    Forward feed

    Args:
      X(torch.tensor) : input data

    Returns:
      [torch.tensor] : result of forward feed
    """
    X = self.conv_layers(X)
    X = self.flatten(X)
    X = self.linear_layers(X)

    return X
  
def vggInference(imgTensor):
    """
    Fits extracted faces to the model

    Arg:
        imgTensor(torch.tensor): a tensor containing all faces converted into tensors
    """
    videoModel = VGG11(in_channels=3, num_classes=2)
    videoModel.load_state_dict(torch.load('vgg_params.pth'))
    label = videoModel(imgTensor)

    return label

def lipSyncInference(tracks):
    """
    
    """

