import numpy as np
import torch
import wandb
import yaml
from torch import nn
from torchvision import transforms

from data.make_dataset import PolonyDataset
from data.utils import mean_std
from models.models import UNet
from models.utils import Config, Looper

# folder to load config file
CONFIG_PATH = "src/config/config.yaml"

with open(CONFIG_PATH, "r") as file:
    config_yaml = yaml.load(file, Loader=yaml.FullLoader)
train_params = config_yaml["train"]


def train(
    dataset_name: str,
    network_architecture: str,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    horizontal_flip: float,
    vertical_flip: float,
    unet_filters: int,
    convolutions: int,
    lr_patience: int,
    input_channels: int,
    loss: nn.MSELoss = nn.MSELoss(),
    wandb_bool: bool = False,
    factor: float = 0.5,
    res: bool = False,
):
    """Train chosen model on selected dataset."""
    # use GPU if avilable
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    if wandb_bool:
        # start a new wandb run to track this script
        run = wandb.init(
            # set the wandb project where this run will be logged
            project="polony",
            save_code=True,
            # track hyperparameters and run metadata
            config={
                "learning_rate": learning_rate,
                "architecture": network_architecture,
                "dataset": dataset_name,
                "epochs": epochs,
                "lr_patience": lr_patience,
                "factor": factor,
            },
        )

        # Copy config to WandB
        config = wandb.config
    #         artifact = wandb.Artifact(name='neural_network', type='model')
    else:
        config = Config(
            {
                "learning_rate": learning_rate,
                "architecture": network_architecture,
                "dataset": dataset_name,
                "epochs": epochs,
                "lr_patience": lr_patience,
                "factor": factor,
            }
        )

    dataset = {}  # training and validation HDF5-based datasets
    dataloader = {}  # training and validation dataloaders
    shuffle = {"train": True, "valid": False}

    for mode in ["train", "valid"]:
        # expected HDF5 files in dataset_name/(train | valid).h5
        # turn on flips only for training dataset
        polony_dataset_params = (
            config_yaml["PolonyDataset_train"]
            if mode == "train"
            else config_yaml["PolonyDataset_val"]
        )
        dataset[mode] = PolonyDataset(**polony_dataset_params)
        dataloader[mode] = torch.utils.data.DataLoader(
            dataset[mode], batch_size=batch_size, shuffle=shuffle[mode]
        )

    # initialize a model based on chosen network_architecture
    if network_architecture == "UNet":
        network = UNet(
            input_filters=input_channels,
            filters=unet_filters,
            N=convolutions,
            res=res,
        ).to(device)
        network = torch.nn.DataParallel(network)
    else:
        network = network_architecture

    optimizer = torch.optim.AdamW(
        network.parameters(),
        lr=config.learning_rate,
    )

    lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        patience=config.lr_patience,
        verbose=True,
        factor=config.factor,
    )

    MEAN, STD = mean_std(dataset["train"])
    normalize = transforms.Normalize(MEAN, STD)
    # create training and validation Loopers to handle a single epoch
    train_looper = Looper(
        network,
        device,
        loss,
        optimizer,
        dataloader["train"],
        len(dataset["train"]),
        wandb_bool=wandb_bool,
        transforms=normalize,
    )
    valid_looper = Looper(
        network,
        device,
        loss,
        optimizer,
        dataloader["valid"],
        len(dataset["valid"]),
        validation=True,
        wandb_bool=wandb_bool,
        transforms=normalize,
    )

    # current best results (lowest mean absolute error on validation set)
    current_best = 100
    second_best = np.infty
    for epoch in range(config.epochs):
        print(f"Epoch {epoch + 1}\n")

        # run training epoch and update learning rate
        train_looper.run()

        # run validation epoch
        with torch.no_grad():
            result = valid_looper.run()

        # update learning rate
        lr_scheduler.step(result)

        # update checkpoint if new best is reached
        if result < current_best:
            # second_best = current_best
            current_best = result
            if result < 3:
                torch.save(
                    network.state_dict(),
                    f"{dataset_name}_{epoch}_{result:.4f}.pth",
                )
            #                 # Save model as an Artifact

            #                 artifact.add_file('neural_network.h5')
            #                 run.log_artifact(artifact)

            print(f"\nNew best result: {result}")
        elif result <= second_best:
            second_best = result
            if result < 3:
                torch.save(
                    network.state_dict(),
                    f"{dataset_name}_{epoch}_{result:.4f}.pth",
                )

            print(f"\nNew best second result: {result}")
        print("\n", "-" * 80, "\n", sep="")

    print(f"[Training done] Best result: {current_best}")
    torch.save(network.state_dict(), f"{dataset_name}_last.pth")
    if wandb_bool:
        run.finish()


if __name__ == "__main__":
    print("Training parameters were taken from the config file")
    train(**train_params)
