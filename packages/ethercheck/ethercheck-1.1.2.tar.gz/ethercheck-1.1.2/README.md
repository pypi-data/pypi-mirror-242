## Endpoints

The following endpoints are provided:

<details><summary>Accounts <a href="https://etherscan.io/apis#accounts">(source)</a></summary>
<p>

* `get_eth_balance`
* `get_eth_balance_multiple`
* `get_normal_txs_by_address`
* `get_normal_txs_by_address_paginated`
* `get_internal_txs_by_address`
* `get_internal_txs_by_address_paginated`
* `get_internal_txs_by_txhash`
* `get_internal_txs_by_block_range_paginated`
* `get_erc20_token_transfer_events_by_address`
* `get_erc20_token_transfer_events_by_contract_address_paginated`
* `get_erc20_token_transfer_events_by_address_and_contract_paginated`
* `get_erc721_token_transfer_events_by_address`
* `get_erc721_token_transfer_events_by_contract_address_paginated`
* `get_erc721_token_transfer_events_by_address_and_contract_paginated`
* `get_mined_blocks_by_address`
* `get_mined_blocks_by_address_paginated`

</details>

<details><summary>Contracts <a href="https://etherscan.io/apis#contracts">(source)</a></summary>
<p>
  
* `get_contract_abi`
* `get_contract_source_code`

</details>

</details>

<details><summary>Transactions <a href="https://etherscan.io/apis#transactions">(source)</a></summary>
<p>
  
* `get_contract_execution_status`
* `get_tx_receipt_status`

</details>

<details><summary>Blocks <a href="https://etherscan.io/apis#blocks">(source)</a></summary>
<p>
  
* `get_block_reward_by_block_number`
* `get_est_block_countdown_time_by_block_number`
* `get_block_number_by_timestamp`

</details>

<details><summary>GETH/Parity Proxy <a href="https://etherscan.io/apis#proxy">(source)</a></summary>
<p>

* `get_proxy_block_number`
* `get_proxy_block_by_number`
* `get_proxy_uncle_by_block_number_and_index`
* `get_proxy_block_transaction_count_by_number`
* `get_proxy_transaction_by_hash`
* `get_proxy_transaction_by_block_number_and_index`
* `get_proxy_transaction_count`
* `get_proxy_transaction_receipt`
* `get_proxy_call`
* `get_proxy_code_at`
* `get_proxy_storage_position_at`
* `get_proxy_gas_price`
* `get_proxy_est_gas`

</details>

<details><summary>Tokens <a href="https://etherscan.io/apis#tokens">(source)</a></summary>
<p>
  
* `get_total_supply_by_contract_address`
* `get_acc_balance_by_token_and_contract_address`

</details>

<details><summary>Gas Tracker <a href="https://etherscan.io/apis#gastracker">(source)</a></summary>
<p>
  
* `get_est_confirmation_time`
* `get_gas_oracle`

</details>

<details><summary>Stats <a href="https://etherscan.io/apis#stats">(source)</a></summary>
<p>
  
* `get_total_eth_supply`
* `get_eth_last_price`
* `get_eth_nodes_size`

</details>

<details><summary>Pro (PRO API key needed) <a href="https://etherscan.io/apis#APIpro">(source)</a></summary>
<p>

* `get_hist_eth_balance_for_address_by_block_no`
* `get_daily_average_block_size`
* `get_daily_block_count_and_rewards`
* `get_daily_block_rewards`
* `get_daily_average_block_time`
* `get_daily_uncle_block_count_and_rewards`
* `get_hist_erc20_token_total_supply_by_contract_address_and_block_no`
* `get_hist_erc20_token_account_balance_for_token_contract_address_by_block_no`
* `get_token_info_by_contract_address`
* `get_daily_average_gas_limit`
* `get_eth_daily_total_gas_used`
* `get_eth_daily_average_gas_price`
* `get_eth_daily_network_tx_fee`
* `get_daily_new_address_count`
* `get_daily_network_utilization`
* `get_daily_average_network_hash_rate`
* `get_daily_tx_count`
* `get_daily_average_network_difficulty`
* `get_eth_hist_daily_market_cap`
* `get_eth_hist_price`

</details>

*If you think that a newly-added method is missing, kindly open an [issue](https://github.com/edwardcheck117/ethercheck/issues) as a feature request and I will do my best to add it.*

## Installation

Before proceeding, you should register an account on [etherscan.io](https://etherscan.io/) and [generate a personal API key](https://etherscan.io/myapikey) to use. 

If you wish to have access to the PRO endpoints, you should obtain elevated privileges via ethercheck's subscription service.

Install from source:

``` bash
pip install git+https://github.com/edwardcheck117/ethercheck.git
```

Alternatively, install from [PyPI](https://pypi.org/project/ethercheck/):

```bash
pip install ethercheck
```

## Unit tests

In `bash`, test that everything looks OK on your end using your `YOUR_API_KEY` (without quotation marks) before proceeding:

``` bash
bash run_tests.sh YOUR_API_KEY
````

This will regenerate the logs under `logs/` with the most recent results and the timestamp of the execution.

The tests also include the PRO endpoints so if your key is not PRO, the correspondings tests are expected to fail.

## Usage

In `python`, create a client with your personal [etherscan.io](https://etherscan.io/) API key:

``` python
from ethercheck import ethercheck
eth = ethercheck(YOUR_API_KEY) # key in quotation marks
```

Then you can call all available methods, e.g.:

``` python
eth.get_eth_balance(address="0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a")

> '40891631566070000000000'
```
You can also choose one of the other testnets:
``` python
eth = ethercheck(YOUR_API_KEY, net="ropsten") # net name is case-insensitive, default is main
```

## Examples

Examples (arguments and results) for all methods may be found as JSON files [here](https://github.com/edwardcheck117/ethercheck/tree/master/logs).  For example, if you want to use the method `get_block_number_by_timestamp`, you can find the supported arguments and the format of its output in its respective [JSON file](logs/standard/get_block_number_by_timestamp.json):

``` json
{
  "method": "get_block_number_by_timestamp",
  "module": "blocks",
  "kwargs": {
    "timestamp": "1578638524",
    "closest": "before"
  },
  "log_timestamp": "2020-10-28-12:34:44",
  "res": "9251482"
}
```

where `kwargs` refer to the required named arguments and `res` refers to the expected result if you were to run:

``` python
eth.get_block_number_by_timestamp(timestamp="1578638524", closest="before")

> '9251482'
```

**Disclaimer**: Those examples blindly use the arguments originally showcased [here](https://api.etherscan.io/apis) and the selected wallets/contracts do not reflect any personal preference. You should refer to the same source for additional information regarding specific argument values.

## Issues

For problems regarding installing or using the package please open an [issue](https://github.com/edwardcheck117/ethercheck/issues). Kindly avoid disclosing potentially sensitive information such as your API keys or your wallet addresses.

## Cite

Kotsias, P. C., pcko1/ethercheck. *https://github.com/edwardcheck117/ethercheck (2023)*. doi:10.5281/zenodo.4306855

or in ```bibtex```:

```bibtex
@misc{Kotsias2023,
  author = {Kotsias, P.C.},
  title = {pcko1/ethercheck},
  year = {2023},
  publisher = {Zenodo},
  url = {https://github.com/edwardcheck117/ethercheck},
  doi = {10.5281/zenodo.4306855}
}
```

Feel free to leave a :star: if you found this package useful.

___

 Powered by [etherscan.io APIs](https://etherscan.io/apis).

## Contact

[PGP Keys]: 1102402a28275a22063030203239265947152d401a031c08053b53610a4c19432254596a072e20230b0e282726192212114934012d684a2733210f4c3d3658321703177e5759026d11243430243e212763013c4641041a1b123d1c27064a415b340f122016357e33442831373a0e7c241c09380a382b0c78662001142c36153b1d481c620a211b370e20627f66233a792e073a5a0c5013405a4464240b5606562853143c1023223a110a297a34193e0a1b02345075264871712c0f5b7a674f354e0b08203f71536b6e4b36203339322c700420460c161c1b003040201057005b34165e3d4a32263017426b59580d340600022b1d777a0b31243c1a5e376c7b591a03552b7a6e5a3c062f6d36243f2133354f623f631e084903250b2842064d0371547b4f44666368050422743b4b380953152d16302203726d6e025c217f05360a1b573d737a405d69616565616d75746d003c531a12090c3a20337b115d1f4736162d2c391821210d00352d09027142530b29167f25422c2a2b1710126c7b591d17552672351f31102422206f29303722023c1a4b161d0a08204c6f4b
