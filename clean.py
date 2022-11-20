import yaml

from grinmw.wallet_v3 import WalletError

from helpers import initiateWallet, cancelAll

config = None
with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

invoice_owner_api_url = config['invoice_owner_api_url']
invoice_api_user = config['invoice_api_user']
invoice_owner_api_password = config['invoice_owner_api_password']
invoice_wallet_password = config['invoice_wallet_password']

pay_owner_api_url = config['pay_owner_api_url']
pay_api_user = config['pay_api_user']
pay_owner_api_password = config['pay_owner_api_password']
pay_wallet_password = config['pay_wallet_password']

invoice_wallet = initiateWallet(
    invoice_owner_api_url,
    invoice_api_user,
    invoice_owner_api_password,
    invoice_wallet_password)
cancelAll(invoice_wallet)

pay_wallet = initiateWallet(
    pay_owner_api_url,
    pay_api_user,
    pay_owner_api_password,
    pay_wallet_password)
cancelAll(pay_wallet)
