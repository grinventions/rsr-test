import yaml

from helpers import initiateWallet, address, invoice, process_invoice, finalize

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

amount = 1000000

invoice_wallet = initiateWallet(
    invoice_owner_api_url,
    invoice_api_user,
    invoice_owner_api_password,
    invoice_wallet_password)
invoice_wallet_address = address(invoice_wallet)

print('invoice wallet is')
print(invoice_wallet_address)
print()

pay_wallet = initiateWallet(
    pay_owner_api_url,
    pay_api_user,
    pay_owner_api_password,
    pay_wallet_password)
pay_wallet_address = address(pay_wallet)

print('pay wallet is')
print(pay_wallet_address)
print()

print('I1')
I1 = invoice(invoice_wallet, pay_wallet_address, amount)
print()

print('I2')
I2 = process_invoice(pay_wallet, I1, amount, invoice_wallet_address)
print()

print('I3')
I3 = finalize(invoice_wallet, I2)
print()
print('done')
