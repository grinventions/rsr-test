import time

from grinmw.wallet_v3 import WalletV3, WalletError


# until the following PR gets merged...
# https://github.com/grinfans/grinmw.py/pull/7
def receive(api_url, api_user, api_password, slate, dest_acct_name, r_addr):
    method = ''
    payload = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'receive_tx',
        'params': [slate, dest_acct_name, r_addr]
    }
    response = requests.post(
                api_url, json=payload,
                auth=(api_user, api_password))
    return resp['result']['Ok']


def initiateWallet(owner_api_url, api_user, owner_api_password, wallet_password):
    wallet = WalletV3(
        owner_api_url,
        api_user,
        owner_api_password)
    wallet.init_secure_api()
    wallet.open_wallet(None, wallet_password)
    return wallet


def address(wallet, derivation_index=0):
    slatepack_address = wallet.get_slatepack_address(derivation_index=derivation_index)
    return slatepack_address


def invoice(wallet, slatepack_address, amount):
    params = {
		'amount': amount,
        'dest_acct_name': None,
        'target_slate_version': None
	}
    slate = wallet.issue_invoice_tx(params)
    txid = slate.get('id', None)
    recipients = []
    if slatepack_address is not None:
        recipients = [slatepack_address]
    slatepack = wallet.create_slatepack_message(slate, recipients)
    return slatepack


def process_invoice(wallet, slatepack, amount, slatepack_address):
    secret_indices = [0]
    slate = wallet.slate_from_slatepack_message(slatepack, secret_indices)
    print(slate)
    args = {
		'src_acct_name': None,
		'amount': amount,
		'minimum_confirmations': 2,
		'max_outputs': 500,
		'num_change_outputs': 1,
		'selection_strategy_is_use_all': True,
		'target_slate_version': None,
		'payment_proof_recipient_address': None,
		'ttl_blocks': None,
		'send_args': None
	}
    wallet.process_invoice_tx(slate, args)
    recipients = []
    if slatepack_address is not None:
        recipients = [slatepack_address]
    slatepack = wallet.create_slatepack_message(slate, recipients)
    return slatepack


def getStoredTx(wallet, tx_id):
    tx = wallet.retrieve_txs(tx_id=tx_id, refresh=False)
    return tx


def cancel(wallet, tx_id):
    wallet.cancel_tx(tx_id=tx_id)


def cancelAll(wallet, start_tx_id=0, delay=0.1):
    tx_id = start_tx_id
    stop = False
    while not stop:
        try:
            txs = getStoredTx(wallet, tx_id)
            if len(txs) == 0:
                stop = True
                break
            tx = txs[0]
            if tx['tx_type'] == 'TxReceivedCancelled':
                tx_id += 1
                continue
            cancel(wallet, tx_id)
            time.sleep(1)
        except WalletError as e:
            if 'TransactionNotCancellable' in e.reason:
                tx_id += 1
                continue
            if 'TransactionDoesntExist' in e.reason:
                stop = True
                break
            print(e)


def finalize(wallet, slatepack, lock=False, post=True, fluff=False):
        if isinstance(slatepack, dict):
            slate = slatepack
        elif isinstance(slatepack, str):
            secret_indices = [0]
            slate = wallet.slate_from_slatepack_message(
                slatepack, secret_indices)
        if lock:
            wallet.tx_lock_outputs(slate)
        slate_finalized = wallet.finalize_tx(slate)
        txid = slate_finalized.get('id', None)
        if post:
            wallet.post_tx(slate_finalized, fluff=fluff)
