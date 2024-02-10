import codecs
import glob
import json
import lzma
from lzma import open as lzma_open
from os import remove
from os.path import join, basename
from typing import Dict

from tqdm import tqdm

from adaptive_padding.padding.padding_strategy import PaddingStrategy
from adaptive_padding.utils.utils import create_folder


class ExperimentConfiguration:
    @staticmethod
    def load_configuration(filepath):
        return json.load(open(filepath, mode="r"))


class PaddingExperiment:
    def __init__(
            self,
            csv_folder,
            output_folder,
            packet_length_index,
            strategies_mapping):
        self.csv_folder = csv_folder
        self.output_folder = output_folder
        self.packet_length_index = packet_length_index
        self.strategies_mapping: Dict[str, PaddingStrategy] = strategies_mapping

    def execute(self):
        for strategy_name in self.strategies_mapping.keys():
            _ = create_folder(join(self.output_folder, strategy_name))
        self.__process_files()

    @staticmethod
    def write_file(line, output_file):
        with codecs.open(output_file, "a+", "ISO-8859-1") as file_writer:
            file_writer.write(line)

    def __process_files(self):
        files = glob.glob(join(self.csv_folder, "*.xz"))
        current_file_number = 1
        number_files = len(files)
        for filepath in files:
            filename = basename(filepath)
            print(f"Processing the file ({current_file_number}/{number_files}): {filename}")
            self.__apply_padding_strategies(
                filename,
                filepath)
            current_file_number += 1

    def __apply_padding_strategies(
            self,
            filename: str,
            filepath: str):
        for strategy_name in self.strategies_mapping:
            print(f"Executing the padding strategy: {strategy_name}")
            with lzma_open(filename=filepath, mode="rt", encoding="ISO-8859-1") as input_file:
                output_strategy_folder = join(self.output_folder, strategy_name)
                output_filepath = join(output_strategy_folder, filename.replace(".csv.tar.xz", ".csv"))
                for line in tqdm(input_file.readlines()):
                    self.__update_length(line, strategy_name, output_filepath)
                self.__compress(output_filepath)
                PaddingExperiment.remove_temporary_file(output_filepath)

    def __update_length(self, line: str, strategy_name: str, output_filepath: str):
        try:
            length = line.split(",")[self.packet_length_index].replace('"', "")
            modified_length = self.strategies_mapping[strategy_name].pad(int(length))
            line = line.replace(length, str(modified_length))
        except (ValueError, IndexError) as exception:
            ...
        finally:
            PaddingExperiment.write_file(line, output_filepath)

    def __compress(self, filepath: str) -> None:
        print("Generating compressed file.")
        output_file = lzma.LZMAFile(filepath.replace(".csv", ".xz"), mode="wb")
        with open(filepath, mode="rt", encoding="ISO-8859-1") as file_reader:
            output_file.write(file_reader.read().encode())

    @staticmethod
    def remove_temporary_file(filepath: str):
        remove(filepath)
