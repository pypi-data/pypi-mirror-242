"""Parse All Model Args"""
import argparse
import os
from pathlib import Path
from pathlib import PurePath
from typing import Dict

import yaml

from .common import tab_printer

type_map = {"int": int, "str": str, "float": float, "bool": bool}

models = {
    "pca_kmeans": "PCA with Kmeans.",
    "sgc_kmeans": "SGC with Kmeans.",
    "dgi_kmeans": "DGI with Kmeans",
    "gmi_kmeans": "GMI with Kmeans",
    "DANMF": "DANMF",
    "MNMF": "MNMF",
    "VGAECD": "VGAECD",
    "CommunityGAN": "CommunityGAN",
    "gae_kmeans": "GAE with Kmeans",
    "vgae_kmeans": "VGAE with Kmeans",
    "DFCN": "DFCN",
    "AGE": "AGE",
    "DAEGC": "DAEGC",
    "SEComm": "SEComm",
    "cc": "Contrastive Clustering",
    "SDCN": "SDCN",
    "SENet_kmeans": "SENEet with kmeans",
    "ComE": "ComE",
    "AGCN": "AGCN",
    "AGC": "AGC",
    "GALA": "GALA",
    "idec": "IDEC",
    "clusternet": "ClusterNet",
    "GDCL": "GDCL",  # BUG exits
    "MVGRL": "MVGRL",
    "SUBLIME": "SUBLIME",
}


def _read_args(model: str = None) -> Dict:
    basename = os.path.abspath(
        f"{os.path.dirname(os.path.realpath(__file__))}/..", )
    config_path: PurePath = Path(f"{basename}/config/{model}.yaml")
    if not config_path.exists():
        return {}
    with open(config_path, encoding="utf-8") as f:
        args = yaml.safe_load(f)
    return args


def _set_subparser(model: str, _parser: argparse.ArgumentParser) -> None:
    args = _read_args(model)
    for key, val in args.items():
        keys = val.keys()
        default_val = val["default"] if "default" in keys else None
        type_val = type_map[val["type"]] if "type" in keys else type(
            val["default"])
        nargs_val = val["nargs"] if "nargs" in keys else None
        _parser.add_argument(
            f"--{key}",
            type=type_val,
            default=default_val,
            help=val["help"],
            nargs=nargs_val,
        )


def parse_all_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="EAGLE Graph Clustering",
        description="Parameters for Graph Clustering",
    )
    parser.add_argument("--dataset",
                        type=str,
                        default="Cora",
                        help="Dataset used in the experiment")
    parser.add_argument("--gpu",
                        type=str,
                        default="0",
                        help="ID(s) of gpu used by cuda")
    parser.add_argument("--dir",
                        type=str,
                        default="./data",
                        help="Path to store the dataset")
    parser.add_argument("--seed",
                        type=int,
                        default=4096,
                        help="Random seed. Defaults to 4096.")
    parser.add_argument(
        "--nodes_rate",
        type=float,
        default=0.5,
        help="Random sample nodes rate in same class. Defaults to 0.5.",
    )
    parser.add_argument(
        "--add_edge_rate",
        type=float,
        default=0.5,
        help="Random add edge rate in same class. Defaults to 0.5.",
    )
    parser.add_argument(
        "--not_set_seed",
        dest="seed",
        action="store_false",
        help="Force Not to Use Random Seed.",
    )
    parser.add_argument(
        "--target_path",
        type=str,
        default=None,
        help=
        "Target file path to save the experiment results. Defaults to None.",
    )

    subparsers = parser.add_subparsers(dest="model", help="sub-command help")

    for _model, _help in models.items():
        _parser = subparsers.add_parser(
            _model, help=f"Run community detection on {_help}")
        _set_subparser(_model, _parser)

    args = parser.parse_args()

    tab_printer(args)

    return args
