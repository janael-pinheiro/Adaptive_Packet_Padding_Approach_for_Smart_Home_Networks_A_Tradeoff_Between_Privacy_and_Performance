<h2>Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance</h2>
Guide for conducting the experiments described in the paper "Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance":

- The experiment configuration is defined in the file "Data/Configuration/experiment_configuration.json". In this file, specify the padding type (Proposal or Existing) and the strategy (100, 500, 700, 900, mtu, random, random255, exponential, linear, and mouse_elephant);
- Produce the features for the original IoT traffic with the script "prepare_features.py". Please, in file "Data/Configuration/experiment_configuration.json", set 'None' for padding and paddingStrategy. Use these features to evaluate padding strategies;
- Update the configuration file with the padding type and strategy to be evaluated;
- The following instructions always assume you are in the project root folder;
- Run the script for padding with the desired strategy (scripts run_existing_padding.py and run_proposal_padding.py);
- The generated files are saved in the appropriate folder under Data/Processed/padding_data. The data generated by the strategies are separated into separate folders;
- Generate the packet length features with the script "prepare_features.py" for each of the strategies;
- Run the script "padding_strategies_evaluation.py" to evaluate padding strategies with the original and modified data;
- Analyze the results.

Note: we use multiple datasets, one per day, to analyze the results with statistical methods such as hypothesis testing. Files with IoT traffic are located in the "Data/Raw" folder. It is unnecessary to decompress the files before running the experiments.  

The files were converted from PCAP files made available by the authors of "A. Sivanathan et al., 'Classifying IoT Devices in Smart Environments Using Network Traffic Characteristics,' in IEEE Transactions on Mobile Computing, vol. 18, no. 8, pp. 1745-1759, 1 Aug. 2019, doi: 10.1109/TMC.2018.2866249." We use Wireshark software to perform this conversion. Configure Wireshark to display the time from the beginning of the capture in seconds.

If you use this code in a publication please cite the following paper:

A. J. Pinheiro, P. Freitas de Araujo-Filho, J. de M. Bezerra and D. R. Campelo, "Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance," in IEEE Internet of Things Journal, 2021.

@ARTICLE{9203848,  
author={Pinheiro, Antônio J. and Freitas de Araujo-Filho, Paulo and de M. Bezerra, Jeandro and Campelo, Divanilson R.},  journal={IEEE Internet of Things Journal},  title={Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance},  year={2021},  volume={8},  number={5},  pages={3930-3938},  doi={10.1109/JIOT.2020.3025988}}

## Run the experiment using Poetry
Inside project root folder:

On Windows:
```sh
set PYTHONPATH=%PYTHONPATH%;.
```

On Linux:
```sh
export PYTHONPATH=$PYTHONPATH:.
```

```sh
pip3 install poetry
```

```sh
poetry install
```

```sh
poetry run python3 adaptive_padding/run_existing_padding.py
poetry run python3 adaptive_padding/run_proposal_padding.py
```

```sh
poetry run python3 adaptive_padding/prepare_features.py
```

```sh
poetry run python3 adaptive_padding/padding_strategies_evaluation.py
```