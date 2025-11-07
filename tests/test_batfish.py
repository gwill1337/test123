#!/usr/bin/env python3
from pybatfish.client.session import Session
import os

# Настройки
bf_address = "127.0.0.1"
snapshot_path = "./snapshots/ci_net/s1"
output_dir = "./output"
network_name = "ci_net"

# Подключение к Batfish
bf = Session(host=bf_address)
bf.set_network(network_name)
bf.init_snapshot(snapshot_path, name="s1", overwrite=True)

# Пример запроса nodeProperties
res = bf.q.nodeProperties().answer().frame()
print(res)

# Сохраняем результат
os.makedirs(output_dir, exist_ok=True)
res.to_csv(f"{output_dir}/results.csv")



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
