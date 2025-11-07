#!/usr/bin/env python3
from pybatfish.client.session import Session
import os
import pandas as pd

# Настройки
bf_address = "127.0.0.1"
snapshot_path = "./snapshots/ci_net/s1"
output_dir = "./output"
network_name = "ci_net"

# Подключение к Batfish
bf = Session(host=bf_address)
bf.set_network(network_name)
bf.init_snapshot(snapshot_path, name="s1", overwrite=True)

# Создаём директорию для результатов
os.makedirs(output_dir, exist_ok=True)

# 1. Node Properties (узлы + базовые свойства)
nodes_df = bf.q.nodeProperties().answer().frame()
nodes_df.to_csv(f"{output_dir}/nodes.csv")
print("=== Nodes ===")
print(nodes_df)

# 2. Интерфейсы каждого узла
interfaces_df = bf.q.interfaceProperties().answer().frame()
interfaces_df.to_csv(f"{output_dir}/interfaces.csv")
print("\n=== Interfaces ===")
print(interfaces_df)

# 3. BGP-соседи
bgp_neighbors_df = bf.q.bgpNeighbors().answer().frame()
bgp_neighbors_df.to_csv(f"{output_dir}/bgp_neighbors.csv")
print("\n=== BGP Neighbors ===")
print(bgp_neighbors_df)

# 4. ACLs (если есть)
acls_df = bf.q.accessLists().answer().frame()
acls_df.to_csv(f"{output_dir}/acls.csv")
print("\n=== ACLs ===")
print(acls_df)


# #!/usr/bin/env python3
# from pybatfish.client.session import Session
# import os

# # Настройки
# bf_address = "127.0.0.1"
# snapshot_path = "./snapshots/ci_net/s1"
# output_dir = "./output"
# network_name = "ci_net"

# # Подключение к Batfish
# bf = Session(host=bf_address)
# bf.set_network(network_name)
# bf.init_snapshot(snapshot_path, name="s1", overwrite=True)

# # Пример запроса nodeProperties
# res = bf.q.nodeProperties().answer().frame()
# print(res)

# # Сохраняем результат
# os.makedirs(output_dir, exist_ok=True)
# res.to_csv(f"{output_dir}/results.csv")



# #!/usr/bin/env python

# # Modules
# from pybatfish.client.commands import bf_init_snapshot, bf_session
# from pybatfish.question.question import load_questions
# from pybatfish.question import bfq
# import os

# # Variables
# bf_address = "127.0.0.1"
# snapshot_path = "./snapshot"
# output_dir = "./output"

# # Body
# if __name__ == "__main__":
#     # Setting host to connect
#     bf_session.host = bf_address

#     # Loading confgs and questions
#     bf_init_snapshot(snapshot_path, overwrite=True)
#     load_questions()

#     # Running questions
#     r = bfq.nodeProperties().answer().frame()
#     print(r)

#     # Saving output
#     if not os.path.exists(output_dir):
#         os.mkdir(output_dir)

#     r.to_csv(f"{output_dir}/results.csv")

# import time
# from pybatfish.client.session import Session

# def test_snapshot_parses():
#     bf = Session(host="localhost")
#     NETWORK = "ci_net"
#     bf.set_network(NETWORK)

#     # Retry init snapshot несколько раз
#     for _ in range(10):
#         try:
#             name = bf.init_snapshot("snapshots/ci_net/s1", name="s1", overwrite=True)
#             break
#         except FileNotFoundError:
#             time.sleep(1)
#     else:
#         raise RuntimeError("Snapshot folder not found after retries")

#     res = bf.q.fileParseStatus().answer().frame()
#     assert not res.empty
#     statuses = [str(s).lower() for s in res["Status"].astype(str).tolist()]
#     assert "pass" in statuses
