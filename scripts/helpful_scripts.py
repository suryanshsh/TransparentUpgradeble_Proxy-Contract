import eth_utils
from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENV = ["development", "test-ganache-local", "mainnet-fork", "ganache"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


# initalizer=box.store, 1
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    trx = None
    if proxy_admin_contract:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            trx = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encode_function_call,
                {"from": account},
            )
        else:
            trx = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from": account}
            )
    else:
        if initializer:
            encode_function_call = encode_function_data(initializer, *args)
            trx = proxy_admin_contract.upgradeAndCall(
                new_implementation_address,
                encode_function_call,
                {"from": account},
            )
        else:
            trx = proxy.upgradeTo(
                new_implementation_address, {"from": account, "gas_limit": 1000000}
            )
    return trx
