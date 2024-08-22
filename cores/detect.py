import pandas as pd
import pickle
import numpy as np
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
import torch.nn.functional as F
from torch.autograd import Variable
import sys
import os

# Thêm thư mục cha vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import hàm get_file từ file get_latest_file.py
from get_latest_file import get_latest_file


columns = ['Destination Port', 'Flow Duration', 'Total Fwd Packets',
       'Total Backward Packets', 'Total Length of Fwd Packets',
       'Total Length of Bwd Packets', 'Fwd Packet Length Max',
       'Fwd Packet Length Min', 'Fwd Packet Length Mean',
       'Fwd Packet Length Std', 'Bwd Packet Length Max',
       'Bwd Packet Length Min', 'Bwd Packet Length Mean',
       'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s',
       'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
       'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max',
       'Fwd IAT Min', 'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std',
       'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags', 'Bwd PSH Flags',
       'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length',
       'Bwd Header Length', 'Fwd Packets/s', 'Bwd Packets/s',
       'Min Packet Length', 'Max Packet Length', 'Packet Length Mean',
       'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count',
       'SYN Flag Count', 'RST Flag Count', 'PSH Flag Count', 'ACK Flag Count',
       'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
       'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size',
       'Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate',
       'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate',
       'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
       'Subflow Bwd Bytes', 'Init_Win_bytes_forward',
       'Init_Win_bytes_backward', 'act_data_pkt_fwd', 'min_seg_size_forward',
       'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean',
       'Idle Std', 'Idle Max', 'Idle Min']
print(len(columns))
map_columns = {
    'src_ip': 'Source IP', 
    'dst_ip': 'Destination IP',
    'src_port': 'Source Port',
    'dst_port': 'Destination Port',
    'src_mac': 'Source MAC',
    'dst_mac': 'Destination MAC',
    'protocol': 'Protocol',
    'timestamp': 'Timestamp',
    'flow_duration': 'Flow Duration',
    'flow_byts_s': 'Flow Bytes/s',
    'flow_pkts_s': 'Flow Packets/s',
    'fwd_pkts_s': 'Fwd Packets/s',
    'bwd_pkts_s': 'Bwd Packets/s',
    'tot_fwd_pkts':'Total Fwd Packets', 
    'tot_bwd_pkts': 'Total Backward Packets', 
    'totlen_fwd_pkts': 'Total Length of Fwd Packets',
    'totlen_bwd_pkts': 'Total Length of Bwd Packets',
    'fwd_pkt_len_max': 'Fwd Packet Length Max',
    'fwd_pkt_len_min': 'Fwd Packet Length Min',
    'fwd_pkt_len_mean': 'Fwd Packet Length Mean',
    'fwd_pkt_len_std': 'Fwd Packet Length Std',
    'bwd_pkt_len_max':'Bwd Packet Length Max',
    'bwd_pkt_len_min':'Bwd Packet Length Min',
    'bwd_pkt_len_mean':'Bwd Packet Length Mean', 
    'bwd_pkt_len_std':'Bwd Packet Length Std',
    'pkt_len_max': 'Max Packet Length',
    'pkt_len_min': 'Min Packet Length',
    'pkt_len_mean':'Packet Length Mean',
    'pkt_len_std':'Packet Length Std', 
    'pkt_len_var':'Packet Length Variance',
    'fwd_header_len':'Fwd Header Length',
    'bwd_header_len':'Bwd Header Length',
    'fwd_seg_size_min':'min_seg_size_forward',
    'fwd_act_data_pkts':'act_data_pkt_fwd',
    'flow_iat_mean': 'Flow IAT Mean', 
    'flow_iat_max':'Flow IAT Max', 
    'flow_iat_min':'Flow IAT Min',
    'flow_iat_std':'Flow IAT Std',
    'fwd_iat_tot': 'Fwd IAT Total',
    'fwd_iat_max':'Fwd IAT Max',
    'fwd_iat_min':'Fwd IAT Min',
    'fwd_iat_mean': 'Fwd IAT Mean',
    'fwd_iat_std':'Fwd IAT Std', 
    'bwd_iat_tot':'Bwd IAT Total', 
    'bwd_iat_max':'Bwd IAT Max',
    'bwd_iat_min':'Bwd IAT Min',
    'bwd_iat_mean':'Bwd IAT Mean',
    'bwd_iat_std': 'Bwd IAT Std', 
    'fwd_psh_flags':'Fwd PSH Flags',
    'bwd_psh_flags':'Bwd PSH Flags',
    'fwd_urg_flags': 'Fwd URG Flags', 
    'bwd_urg_flags': 'Bwd URG Flags', 
    'fin_flag_cnt': 'FIN Flag Count',
    'syn_flag_cnt': 'SYN Flag Count',
    'rst_flag_cnt':'RST Flag Count', 
    'psh_flag_cnt':'PSH Flag Count',
    'ack_flag_cnt':'ACK Flag Count',
    'urg_flag_cnt': 'URG Flag Count',
    'ece_flag_cnt': 'ECE Flag Count',
    'down_up_ratio': 'Down/Up Ratio', 
    'pkt_size_avg': 'Average Packet Size',
    'init_fwd_win_byts':'Init_Win_bytes_forward',
    'init_bwd_win_byts':'Init_Win_bytes_backward',
    'active_max': 'Active Max', 
    'active_min':'Active Min',
    'active_mean': 'Active Mean',
    'active_std': 'Active Std',
    'idle_max':'Idle Max',
    'idle_min':'Idle Min', 
    'idle_mean': 'Idle Mean',
    'idle_std':'Idle Std', 
    'fwd_byts_b_avg': 'Fwd Avg Bytes/Bulk', 
    'fwd_pkts_b_avg': 'Fwd Avg Packets/Bulk',
    'bwd_byts_b_avg':'Bwd Avg Bytes/Bulk',
    'bwd_pkts_b_avg':'Bwd Avg Packets/Bulk',
    'fwd_blk_rate_avg':'Fwd Avg Bulk Rate',
    'bwd_blk_rate_avg':'Bwd Avg Bulk Rate',
    'fwd_seg_size_avg':'Avg Fwd Segment Size',
    'bwd_seg_size_avg':'Avg Bwd Segment Size', 
    'cwe_flag_count':'CWE Flag Count',
    'subflow_fwd_pkts':'Subflow Fwd Packets',
    'subflow_bwd_pkts':'Subflow Bwd Packets', 
    'subflow_fwd_byts':'Subflow Fwd Bytes',
    'subflow_bwd_byts':'Subflow Bwd Bytes'
}

# Define class Autoencoder 
class Encoder(nn.Module):
    
    def __init__(self, hidden_size):        
        super().__init__()
        
        self.fc1 = nn.Linear(input_size, hidden1_size)
        torch.nn.init.xavier_uniform(self.fc1.weight)
        torch.nn.init.zeros_(self.fc1.bias)
    
        self.fc2 = nn.Linear(hidden1_size, hidden2_size)
        torch.nn.init.xavier_uniform(self.fc2.weight)
        torch.nn.init.zeros_(self.fc2.bias)
    
        self.fc3 = nn.Linear(hidden2_size, hidden_size)
        torch.nn.init.xavier_uniform(self.fc3.weight)
        torch.nn.init.zeros_(self.fc3.bias)
    
    def forward(self,x):
        out = x.view(x.size(0), input_size)
        out = torch.tanh(self.fc1(out))
        out = torch.tanh(self.fc2(out))
        out = self.fc3(out)
        return out
class Decoder (nn.Module):
    
    def __init__(self, hidden_size):        
        super().__init__()
        
        self.fc1 = nn.Linear(hidden_size, hidden2_size)
        self.fc1.weight.data = torch.Tensor(Encoder(hidden_size).fc3.weight).transpose(0,1)
        torch.nn.init.zeros_(self.fc1.bias)
                
        self.fc2 = nn.Linear(hidden2_size, hidden1_size)
        self.fc2.weight.data = torch.Tensor(Encoder(hidden_size).fc2.weight).transpose(0,1)
        torch.nn.init.zeros_(self.fc2.bias)
        
        self.fc3 = nn.Linear(hidden1_size, input_size)
        self.fc3.weight.data = torch.Tensor(Encoder(hidden_size).fc1.weight).transpose(0,1)
        torch.nn.init.zeros_(self.fc3.bias)
        
    def forward(self,x):
        out = torch.tanh(self.fc1(x))
        out = torch.tanh(self.fc2(out))
        out = torch.tanh(self.fc3(out))
        return out

hidden1_size = 39
hidden2_size = 19
hidden_size = 9
input_size = 77

# AE + classifier
d =hidden_size
encoder = Encoder(d)
decoder = Decoder(d)


import torch

with open("/home/ubuntu/Desktop/SIEM/security_system/Detect_AI/Autoencoder.pt", "rb") as f:
    encoder.load_state_dict(torch.load(f))

import joblib
# Tải mô hình từ file
model = joblib.load('/home/ubuntu/Desktop/SIEM/security_system/Detect_AI/Autoencoder.joblib')

# Tải mô hình từ file
scaler = joblib.load('/home/ubuntu/Desktop/SIEM/security_system/Detect_AI/saler_new.joblib')

# Sử dụng hàm
directory_path = "/home/ubuntu/Desktop/SIEM/security_system/csv"
latest_file = get_latest_file(directory_path, "csv")
print(f"File mới nhất: {latest_file}")


def read_csv_(file):
    df = pd.read_csv(file)
    # Xác định header
    header = df.columns.tolist()
    # Xóa các hàng trùng với header
    df_filtered = df[~df.apply(lambda row: row.tolist() == header, axis=1)]
    # Ghi đè DataFrame đã xử lý lên file CSV gốc
    df_filtered.to_csv(file, index=False)
    # Đọc lại file CSV đã xử lý vào DataFrame mới
    df_new = pd.read_csv(file)
    return df_new

def preprocessing(df):
    df_copy = df.drop(columns=['Flow ID', 'Src IP','Dst IP','Src Port','Protocol','Timestamp', 'Label'])
    print('Shape of new_df: ', df_copy)
    new_cols = df_copy.columns
    df_copy.drop_duplicates(subset=new_cols, inplace=True)
    new_df =  df_copy[new_cols]
    print('Columns of df: ', df.columns)
    print('Shape of df: ', df.shape)
    print('Columns of new_df: ', new_df.columns)
    print('Shape of new_df: ', new_df)
    # new_df.drop_duplicates(inplace=True)
    new_df.replace('Infinity', -1, inplace=True)
    new_df = new_df.apply(pd.to_numeric, errors='coerce')
    new_df.replace([np.inf, -np.inf, np.nan], -1, inplace=True)
    print('New_df: ', new_df)
    scaled = scaler.transform(new_df)
    return new_df,scaled


def predic_AE(df,file_name):
    print('Input shape:', df.shape)
    new_df, scaled = preprocessing(df)
    realtime_tensor = torch.Tensor(scaled)
    encoded_realtime = encoder(realtime_tensor)
    print('encoded_realtime: ', encoded_realtime.shape)
    encoded_realtime = encoded_realtime.detach().numpy()
    y_pred =model.predict(encoded_realtime)
    output = df.copy()
    output['Label']=y_pred
    # Lưu DataFrame kết quả vào một file CSV trong thư mục 'csv'
    # output_file_path = os.path.join('/home/ubuntu/Desktop/SIEM/security_system/ouput', 'output_with_predictions.csv')
    # output.to_csv(output_file_path, index=False)
    base_name = os.path.basename(file_name)
    output_file_name = os.path.splitext(base_name)[0] + '_predictions.csv'
    output_file_path = os.path.join('/home/ubuntu/Desktop/SIEM/security_system/ouput', output_file_name)
    output.to_csv(output_file_path, index=False)

    unique_values, value_counts = np.unique(y_pred, return_counts=True)

    # In kết quả
    print("Các giá trị duy nhất:", unique_values)
    print("Số lần xuất hiện tương ứng:", value_counts)
    return y_pred

df=read_csv_(latest_file)
print("test",df)
test=predic_AE(df,latest_file)

