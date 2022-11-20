# Testing RSR Flow

Given the issue [#635](https://github.com/mimblewimble/grin-wallet/issues/635#issuecomment-1310189686) the RSR flow is not operational.

I prepared this tool to be able to quickly test different wallet releases to find when did RSR flow break. The Python script is opening collection with two wallets and performs RSR slatepack exchange allowing us to quickly test without spending a lot of time doing copy-paste.

## Preparing

1. Clone the [grin-wallet](https://github.com/mimblewimble/grin-wallet) repo.
2. Create two local wallets, make sure one of them has some funds. One is invoice wallet that issues an invoice and another one is payer wallet that pays the invoice.
3. Make sure the payer wallet has some funds.
4. Set the payer wallet owner API to run on port `3421` and invoice wallet owner API to run on standard `3421`.
5. Fill out the `config.yml` from this repo and put the owner API passwords. They are available in the `.owner_api_secret` of each of the wallets.
6. Run `pip install -r requirements` in the root of this repo to install the dependencies.

You are ready for testing.

## Perform the test

1. Checkout your local grin-wallet repo to the commit height you wish to test.
2. Compile it.
3. Run both of the owner APIs with it. One for invoice wallet and one for payer wallet.
4. Run `test.py` to perform the RSR exchange. See if you get the error.
5. Run `clean.py` to cancel all the transactions and ensure no outputs are locked.

If you reproduced the error you should see something like

```
grinmw.wallet_v3.WalletError: Callng finalize_tx with params {'token': 'adbcb1d1db7d1a14a37e1e80f36aa42ad944cb4838149eaa1c298fc8b1c0eedc', 'slate': {'amt': '1000000', 'id': 'cc251c7a-18d2-4f02-85f0-aac6f7f03d96', 'sigs': [{'nonce': '030e51f20a6511e1e30ab9aa1d6172acea6abd58fa1a2be897808f3176b666922a', 'xs': '02dec7bb26349f87cf5afccedf9b9cbad5a412085b7ce2d90e5e656690beda59fe'}], 'sta': 'I1', 'ver': '4:3'}} failed with error code -32099 because: Fee: Missing fee fields
```

(don't worry, this wallet is just for tests, it is ok to expose signatures and other data).

If everything works then you managed to find wallet commit that works. Try to find as recent as possible and report it in [#635](https://github.com/mimblewimble/grin-wallet/issues/635#issuecomment-1310189686). Myself, the oldest commit I managed to test was [1dd85690a1c08b3508385f0c11abf29a05b664d9](https://github.com/mimblewimble/grin-wallet/commit/1dd85690a1c08b3508385f0c11abf29a05b664d9) and one before it [ba9a4982df8c0a5c34583769e2c35a7669762f58](https://github.com/mimblewimble/grin-wallet/commit/ba9a4982df8c0a5c34583769e2c35a7669762f58) does not compile for me.
