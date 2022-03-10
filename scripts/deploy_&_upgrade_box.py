from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    Contract,
    network,
    Box,
    Boxv2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
)


def main():
    account = get_account()
    print(f"[+] Deploying to {network.show_active()}")

    box = Box.deploy({"from": account}, publish_source=True)
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # initializer = box.store, 1
    box_encode_init_fun = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encode_init_fun,
        {"from": account, "gas_limit": 1000000},
    )

    print(f"[+] Proxy deployed to {proxy}, you can now upgrade to v2!")

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})

    print("[+] Upgrading Contract to BoxV2")
    box_v2 = Boxv2.deploy({"from": account}, publish_source=True)

    upgrade_trx = upgrade(account, proxy, box_v2.address, proxy_admin)
    upgrade_trx.wait(1)
    print("[+] Proxy has been upgraded !")
    proxy_box = Contract.from_abi("Boxv2", proxy.address, Boxv2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
