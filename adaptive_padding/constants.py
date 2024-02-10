from enum import Enum
from os.path import join


class FolderPath(Enum):
    RAW_DATA = join("Data", "Raw")
    PADDING_DATA = join("Data", "Processed", "padding_data")
    PADDING_FEATURES = join("Data", "Processed", "padding_features")
    GROUND_TRUTH_FEATURES = join("Data", "Processed", "ground_truth_features")
    CONFIGURATION = join("Data", "Configuration")
