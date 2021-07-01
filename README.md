<h2>Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance</h2>
Guide for conducting the experiments described in the paper "Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance":

- Run the script "src/createsFolderStructure.py";
- Run the script for padding with the desired strategy (implemented through functions in src/proposal.py and src/existingStrategies.py);
- The generated CSV files are saved in the appropriate folder under Data/Processed/PaddingData. The data generated by the strategies are separated into separate folders;
- Generate the packet length features with the script "prepare_features.py" for each of the strategies;
- Produce the features for the original IoT traffic with the same script as the previous step. Use these features to evaluate padding strategies;
- Run the script "src/padding_strategys_evaluation.py" to evaluate padding strategies with the original and modified data;
- Analyze the results.

Note: we use multiple datasets, one per day, to analyze the results with statistical methods such as hypothesis testing. CSV files with IoT traffic are located in the "Data/Raw" folder. It is necessary to decompress the files before running the experiments.  

CSV files were converted from PCAP files made available by the authors of "A. Sivanathan, H. H. Gharakheili, F. Loi, A. Radford, C. Wijenayake, A. Vishwanath, and V. Sivaraman, 'Classifying IoT devices in smart environments using network traffic characteristics,' IEEE". We use Wireshark software to perform this conversion. Configure Wireshark to display the time from the beginning of the capture in seconds.

If you use this code in a publication please cite the following paper:

A. J. Pinheiro, P. Freitas de Araujo-Filho, J. de M. Bezerra and D. R. Campelo, "Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance," in IEEE Internet of Things Journal, 2021.

@ARTICLE{9203848,  
author={Pinheiro, Antônio J. and Freitas de Araujo-Filho, Paulo and de M. Bezerra, Jeandro and Campelo, Divanilson R.},  journal={IEEE Internet of Things Journal},  title={Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance},  year={2021},  volume={8},  number={5},  pages={3930-3938},  doi={10.1109/JIOT.2020.3025988}}