#!/usr/bin/env python3
from pybatfish.client.session import Session
import os

import pandas as pd

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', 0)
# pd.set_option('display.max_colwidth', None)

# Настройки
bf_address = "127.0.0.1"
snapshot_path = "./snapshots/ci_net/s1"
output_dir = "./output"
network_name = "ci_net"

# Подключение к Batfish
bf = Session(host=bf_address)
bf.set_network(network_name)
bf.init_snapshot(snapshot_path, name="s1", overwrite=True)

os.makedirs(output_dir, exist_ok=True)

# --- Вспомогательная функция для разбиения Interface на Node и Intf ---
def split_node_interface(df):
    df = df.copy()
    df['Node'] = df['Interface'].str.split('[').str[0]
    df['Intf'] = df['Interface'].str.split('[').str[1].str.rstrip(']')
    return df

# --- Node Properties ---
nodes_df = bf.q.nodeProperties().answer().frame()
nodes_df.to_csv(f"{output_dir}/nodes.csv")
print("=== Nodes ===")
print(nodes_df)

# --- Interfaces ---
interfaces_df = bf.q.interfaceProperties().answer().frame()
interfaces_df = split_node_interface(interfaces_df)
interfaces_df.to_csv(f"{output_dir}/interfaces.csv")
print("\n=== Interfaces ===")
print(interfaces_df)

# --- Validation ---
errors = []

# Неактивные интерфейсы
inactive = interfaces_df[interfaces_df['Active'] == False]
if not inactive.empty:
    errors.append(f"Inactive interfaces:\n{inactive[['Intf','Node']]}")

# --- BGP Sessions ---
try:
    bgp_df = bf.q.bgpSessionCompatibility().answer().frame()
    bgp_df.to_csv(f"{output_dir}/bgp_sessions.csv")
    print("\n=== BGP Sessions ===")
    print(bgp_df)
    
    # Проверка на несовместимые или неизвестные BGP сессии
    bad_bgp = bgp_df[bgp_df['Configured_Status'].isin(['NOT_COMPATIBLE','UNKNOWN_REMOTE'])]
    if not bad_bgp.empty:
        errors.append(f"Incompatible BGP sessions:\n{bad_bgp[['Node','Remote_Node','Configured_Status']]}")
except Exception as e:
    print("BGP Sessions not available:", e)

# --- OSPF Sessions ---
try:
    ospf_df = bf.q.ospfSessionCompatibility().answer().frame()
    ospf_df.to_csv(f"{output_dir}/ospf_sessions.csv")
    print("\n=== OSPF Sessions ===")
    print(ospf_df)
    
    # Проверка на несовместимые OSPF сессии
    bad_ospf = ospf_df[ospf_df['Session_Status'] != 'ESTABLISHED']
    if not bad_ospf.empty:
        errors.append(f"Incompatible OSPF sessions:\n{bad_ospf[['Interface','Remote_Interface','Session_Status']]}")
except Exception as e:
    print("OSPF Sessions not available:", e)

# --- Вывод ошибок ---
if errors:
    print("\nVALIDATION FAILED:")
    for e in errors:
        print("-", e)
    exit(1)
else:
    print("\nVALIDATION PASSED: no errors found")


# =========================================

# #!/usr/bin/env python3
from pybatfish.client.session import Session
import os

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 0)
pd.set_option('display.max_colwidth', None)

# Настройки
bf_address = "127.0.0.1"
snapshot_path = "./snapshots/ci_net/s1"
output_dir = "./output"
network_name = "ci_net"

# Подключение к Batfish
bf = Session(host=bf_address)
bf.set_network(network_name)
bf.init_snapshot(snapshot_path, name="s1", overwrite=True)

os.makedirs(output_dir, exist_ok=True)

# 1. Nodes
nodes_df = bf.q.nodeProperties().answer().frame()
nodes_df.to_csv(f"{output_dir}/nodes.csv")
print("=== Nodes ===")
print(nodes_df)

# 2. Interfaces
interfaces_df = bf.q.interfaceProperties().answer().frame()
interfaces_df.to_csv(f"{output_dir}/interfaces.csv")
print("\n=== Interfaces ===")
print(interfaces_df)

# 3. Filter Line Reachability
try:
    filter_df = bf.q.filterLineReachability().answer().frame()
    filter_df.to_csv(f"{output_dir}/filter_line_reachability.csv")
    print("\n=== Filter Line Reachability ===")
    print(filter_df.head(5))
except Exception as e:
    print("Filter Line Reachability not available:", e)

# 4. BGP Session Compatibility
try:
    bgp_compat_df = bf.q.bgpSessionCompatibility().answer().frame()
    bgp_compat_df.to_csv(f"{output_dir}/bgp_session_compatibility.csv")
    print("\n=== BGP Session Compatibility ===")
    print(bgp_compat_df.head(5))
except Exception as e:
    print("BGP Session Compatibility not available:", e)

# 5. BGP Session Status
try:
    bgp_status_df = bf.q.bgpSessionStatus().answer().frame()
    bgp_status_df.to_csv(f"{output_dir}/bgp_session_status.csv")
    print("\n=== BGP Session Status ===")
    print(bgp_status_df.head(5))
except Exception as e:
    print("BGP Session Status not available:", e)

# 6. BGP Edges
try:
    bgp_edges_df = bf.q.bgpEdges().answer().frame()
    bgp_edges_df.to_csv(f"{output_dir}/bgp_edges.csv")
    print("\n=== BGP Edges ===")
    print(bgp_edges_df.head(5))
except Exception as e:
    print("BGP Edges not available:", e)

# 7. OSPF Session Compatibility
try:
    ospf_df = bf.q.ospfSessionCompatibility().answer().frame()
    ospf_df.to_csv(f"{output_dir}/ospf_session_compatibility.csv")
    print("\n=== OSPF Session Compatibility ===")
    print(ospf_df.head(5))
except Exception as e:
    print("OSPF Session Compatibility not available:", e)

# 8. OSPF Edges
try:
    ospf_edges_df = bf.q.ospfEdges().answer().frame()
    ospf_edges_df.to_csv(f"{output_dir}/ospf_edges.csv")
    print("\n=== OSPF Edges ===")
    print(ospf_edges_df.head(5))
except Exception as e:
    print("OSPF Edges not available:", e)
    
