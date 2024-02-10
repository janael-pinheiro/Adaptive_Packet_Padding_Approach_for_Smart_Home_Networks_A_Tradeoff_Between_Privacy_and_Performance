"""
Implements the packet padding proposal presented in the paper "Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance".
"""
from os.path import join

from adaptive_padding.constants import FolderPath
from adaptive_padding.experiment.evaluation import PaddingExperiment
from adaptive_padding.padding.strategies_mapping_factory import create_existing_strategies_mapping


def main():
    strategies = create_existing_strategies_mapping()
    experiment = PaddingExperiment(
        FolderPath.RAW_DATA.value,
        join(FolderPath.PADDING_DATA.value, "Existing"),
        5,
        strategies)
    experiment.execute()


if __name__ == "__main__":
    main()
