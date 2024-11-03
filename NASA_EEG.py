import pandas as pd
import time
from pylsl import StreamInfo, StreamOutlet, local_clock

# Učitavanje CSV datoteke (zamijeni 'path_to_your_file.csv' s pravom putanjom do tvog dataset-a)
data = pd.read_csv("/Users/patrik/Desktop/5_CA.csv")

# Definiraj kolone koje predstavljaju EEG kanale
eeg_channels = ["EEG_FP1", "EEG_F7", "EEG_F8", "EEG_T4", "EEG_T6", "EEG_T3", "EEG_FP2", "EEG_O1", "EEG_P3",
                "EEG_Pz", "EEG_F3", "EEG_Fz", "EEG_F4", "EEG_C4", "EEG_P4", "EEG_POz", "EEG_C3", "EEG_Cz",
                "EEG_O2"]

# Postavljanje informacija o LSL stream-u
stream_info = StreamInfo(name="NASA_LOFT_Stream", type="EEG", channel_count=len(eeg_channels),
                         nominal_srate=256, channel_format="float32")
outlet = StreamOutlet(stream_info)

print("Početak streaminga podataka...")

# Petlja za slanje svakog reda podataka kao uzorka u realnom vremenu
for index, row in data.iterrows():
    # Ekstrakcija trenutnog uzorka podataka
    sample = row[eeg_channels].values

    # Dohvati trenutni timestamp
    timestamp = local_clock()

    # Slanje uzorka s timestampom putem LSL stream-a
    outlet.push_sample(sample, timestamp)

    # Pauza za simuliranje frekvencije od 256 Hz
    time.sleep(1 / 256)

print("Streaming završen.")