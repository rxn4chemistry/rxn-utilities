"""Utils for modeling."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Union, cast

import torch


def get_gpu_device_names() -> List[str]:
    """Get GPU device names as a list.

    Returns:
        names of available GPU devices.
    """
    gpu_device_names = []
    if torch.cuda.is_available():
        gpu_device_names = [
            f"cuda:{index}" for index in range(torch.cuda.device_count())
        ]
    return gpu_device_names


def claim_device_name() -> str:
    """Claim a device name.

    Returns:
        device name, if no GPU is available returns CPU.
    """
    device_name = "cpu"
    gpu_device_names = get_gpu_device_names()
    if len(gpu_device_names) > 0:
        device_name = gpu_device_names[0]
    return device_name


def get_device() -> torch.device:
    """Get device dynamically.

    Returns:
        default basic device allocated.
    """
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def device_claim(device: Optional[Union[torch.device, str]] = None) -> torch.device:
    """Satisfy a device claim.

    Args:
        device: device where the inference is running either as a dedicated class or
            a string. If not provided is inferred.

    Returns:
        the claimed device or a default one.
    """
    if isinstance(device, str):
        device = torch.device(device)
    device = (
        get_device()
        if (device is None or not isinstance(device, torch.device))
        else device
    )
    return device


def get_device_from_tensor(tensor: torch.Tensor) -> torch.device:
    """Get the device from a tensor.

    Args:
        tensor: a tensor.

    Returns:
        the device.
    """
    device_id = tensor.get_device()
    device = "cpu" if device_id < 0 else f"cuda:{device_id}"
    return device_claim(device)


def map_dict_sequences_to_tensors(
    sequences_dict: Dict[str, Union[Sequence, torch.Tensor]],
    device: Union[str, torch.device],
) -> Dict[str, torch.Tensor]:
    """Maps a dictionary of sequences to tensors of a specific device.

    Args:
        sequences_dict: a dictionary of sequences.
        device: the device where to allocate the tensors on.

    Returns:
        a dictionary of tensors mapped to the device.
    """
    return {
        key: (
            cast(torch.Tensor, sequence).to(device=device)
            if isinstance(sequence, torch.Tensor)
            else torch.tensor(sequence, device=device)
        )
        for key, sequence in sequences_dict.items()
    }


def get_associated_max_len(checkpoint_dir: Path) -> int:
    """Get the max sequence length by looking in the config file associated with
    a model checkpoint."""
    config_path = checkpoint_dir / "config.json"
    if not config_path.exists():
        raise RuntimeError(f"No config file found where expected: {config_path}")

    try:
        with open(config_path, "rt") as f:
            config = json.load(f)
    except Exception as e:
        raise RuntimeError(f'Error when parsing "{config_path}": {e}')

    try:
        return config["max_position_embeddings"]
    except KeyError:
        raise RuntimeError(
            "Can't determine max sequence length: did not find "
            f'"max_position_embeddings" in "{config_path}"'
        )
