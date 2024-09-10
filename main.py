import time
from olx import olx_main
from otodom import otodom_main

if __name__ == "__main__":
    olx_main()
    time.sleep(1)
    otodom_main()
