import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

import pandas as pd


def get_net_segment():
    with os.popen("arp -a") as res:
        for line in res:
            line = line.strip()
            if line.startswith("接口"):
                net_segment = re.findall(
                    "(\d+\.\d+\.\d+)\.\d+", line)[0]
                break
    return net_segment


def ping_net_segment_all(net_segment):
    # for i in range(1, 255):
    #     os.system(f"ping -w 1 -n 1 {net_segment}.{i}")
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(1, 255):
            executor.submit(os.popen, f"ping -w 1 -n 1 {net_segment}.{i}")


def get_arp_ip_mac():
    header = None
    with os.popen("arp -a") as res:
        for line in res:
            line = line.strip()
            if not line or line.startswith("接口"):
                continue
            if header is None:
                header = re.split(" {2,}", line.strip())
                break
        df = pd.read_csv(res, sep=" {2,}",
                         names=header, header=0, engine='python')
    return df


def ping_ip_list(ips, max_workers=4):
    print("正在扫描在线列表")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_tasks = []
        for ip in ips:
            future_tasks.append(executor.submit(os.popen, f"ping -w 1 -n 1 {ip}"))
        wait(future_tasks, return_when=ALL_COMPLETED)


if __name__ == '__main__':
    # 是否进行初始扫描
    init_search = False
    if init_search:
        print("正在扫描当前网段所有ip，预计耗时1分钟....")
        ping_net_segment_all(get_net_segment())

    last = None
    while 1:
        df = get_arp_ip_mac()
        df = df.loc[df.类型 == "动态", ["Internet 地址", "物理地址"]]
        if last is None:
            print("当前在线的设备：")
            print(df)
        else:
            online = df.loc[~df.物理地址.isin(last.物理地址)]
            if online.shape[0] > 0:
                print("新上线设备：")
                print(online)
            offline = last[~last.物理地址.isin(df.物理地址)]
            if offline.shape[0] > 0:
                print("刚下线设备：")
                print(offline)
        time.sleep(5)
        ping_ip_list(df["Internet 地址"].values)
        last = df
