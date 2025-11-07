import time
from pybatfish.client.session import Session

def test_snapshot_parses():
    bf = Session(host="localhost")
    NETWORK = "ci_net"
    bf.set_network(NETWORK)

    # Retry init snapshot несколько раз
    for _ in range(10):
        try:
            name = bf.init_snapshot("snapshots/ci_net/s1", name="s1", overwrite=True)
            break
        except FileNotFoundError:
            time.sleep(1)
    else:
        raise RuntimeError("Snapshot folder not found after retries")

    res = bf.q.fileParseStatus().answer().frame()
    assert not res.empty
    statuses = [str(s).lower() for s in res["Status"].astype(str).tolist()]
    assert "pass" in statuses
