"""
Implements the packet padding proposal presented in the paper "Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance".
"""

from os.path import join
from typing import Dict

from adaptive_padding.constants import FolderPath
from adaptive_padding.experiment.evaluation import PaddingExperiment
from adaptive_padding.padding.padding_strategy import PaddingStrategy
from adaptive_padding.padding.strategies_mapping_factory import create_proposal_strategies_mapping


def main():
    strategies: Dict[str, PaddingStrategy] = create_proposal_strategies_mapping()
    experiment = PaddingExperiment(
        FolderPath.RAW_DATA.value,
        join(FolderPath.PADDING_DATA.value, "Proposal"),
        5,
        strategies)
    experiment.execute()


if __name__ == "__main__":
    main()
