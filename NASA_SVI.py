import pandas as pd
from pylsl import StreamInfo, StreamOutlet, local_clock
import time

# Učitavanje CSV datoteke (zamijeni 'path_to_your_file.csv' s pravom putanjom do tvog dataset-a)
data = pd.read_csv("/Users/patrik/Desktop/5_CA.csv")

# Definiraj kolone za svaki tip podataka
eeg_channels = ["EEG_FP1", "EEG_F7", "EEG_F8", "EEG_T4", "EEG_T6", "EEG_T3", "EEG_FP2", "EEG_O1", "EEG_P3",
                "EEG_Pz", "EEG_F3", "EEG_Fz", "EEG_F4", "EEG_C4", "EEG_P4", "EEG_POz", "EEG_C3", "EEG_Cz",
                "EEG_O2"]
ecg_channels = ["ECG"]  # Ako je ECG u jednoj koloni
resp_rate_channels = ["R"]
gsr_channels = ["GSR"]
event_channels = ["Event"]

# Postavljanje LSL stream-ova za svaki tip podataka
eeg_info = StreamInfo(name="NASA_LOFT_EEG", type="EEG", channel_count=len(eeg_channels), nominal_srate=256, channel_format="float32")
eeg_outlet = StreamOutlet(eeg_info)

ecg_info = StreamInfo(name="NASA_LOFT_ECG", type="ECG", channel_count=len(ecg_channels), nominal_srate=256, channel_format="float32")
ecg_outlet = StreamOutlet(ecg_info)

resp_rate_info = StreamInfo(name="NASA_LOFT_Respiratory", type="Respiratory", channel_count=len(resp_rate_channels), nominal_srate=256, channel_format="float32")
resp_rate_outlet = StreamOutlet(resp_rate_info)

gsr_info = StreamInfo(name="NASA_LOFT_GSR", type="GSR", channel_count=len(gsr_channels), nominal_srate=256, channel_format="float32")
gsr_outlet = StreamOutlet(gsr_info)

event_info = StreamInfo(name="NASA_LOFT_Event", type="Event", channel_count=len(event_channels), nominal_srate=256, channel_format="float32")
event_outlet = StreamOutlet(event_info)

print("Početak streaminga podataka...")

# Petlja za slanje svakog reda podataka kao uzorka u realnom vremenu
for index, row in data.iterrows():
    # Ekstrakcija trenutnih uzoraka podataka
    eeg_sample = row[eeg_channels].values
    ecg_sample = row[ecg_channels].values
    resp_rate_sample = row[resp_rate_channels].values
    gsr_sample = row[gsr_channels].values
    event_sample = row[event_channels].values

    # Dodavanje LSL timestamp-a za sinkronizaciju
    timestamp = local_clock()

    # Slanje uzoraka putem odgovarajućih LSL stream-ova
    eeg_outlet.push_sample(eeg_sample, timestamp)
    ecg_outlet.push_sample(ecg_sample, timestamp)
    resp_rate_outlet.push_sample(resp_rate_sample, timestamp)
    gsr_outlet.push_sample(gsr_sample, timestamp)
    event_outlet.push_sample(event_sample, timestamp)

    # Pauza za simuliranje frekvencije od 256 Hz
    time.sleep(1 / 256)

print("Streaming završen.")