# eth-balancer

eth-balancer is a python wrapper built ontop the [web3py](https://web3py.readthedocs.io/en/stable/) library to interact with [Balancer](https://balancer.finance/) solidity contracts on a public or private ethereum blockchain. 

The library defines a python function for each function defined by the solidity contracts in python, adding type hints for the arguments and return values. This makes it easier to call the contracts' function by enabling IDE features such as auto-completion. 

## Installation

You can install the `eth-balancer` package using pip:

```
python -m pip install eth-balancer
```

## Getting started

Here is how to deploy and use the [Balancer v1 BFactory solidity contract](https://github.com/balancer-labs/balancer-core/blob/master/contracts/BFactory.sol) using this library:


```python
# First, you need a connection to an ethereum node.
# Here, we are using a local node created with ganache-cli for instance.

from web3 import Web3, HTTPProvider
url = "http://127.0.0.1:8545"
w3 = Web3(HTTPProvider(url))

# We can deploy the factory as follows:

from eth_balancer.v1.core import BFactory, BPool

receipt = BFactory.deploy(w3).waitForReceipt()
factory = receipt.contract

# Alternatively, we can connect to a deployed instance:

factory_address = '0x9424B1412450D0f8Fc2255FAf6046b98213B76Bd'
factory = BFactory(w3, address=factory_address)

# All the functions defined by the solidity contract are available.
# Here is how to send a transaction to the newBPool function

receipt = factory.functions.newBPool().waitForReceipt()

# You can parse the event emitted by the function as follows:

events = receipt.events.LOG_NEW_POOL()
pool_address = events[0]["args"]["pool"]

# Here is how to make an eth-call 

return_value = factory.functions.isBPool(pool_address).call()
print(f"isBPool({pool_address}) returned {return_value}")

# And here is how to create a BPool object using the newly created address

pool = BPool(w3, pool_address)

```

## Documentation

For each solidity contract defined by Balancer, this package contains a python class with the same name and its methods also have the same name as the solidity one. This makes it easy to find the class and method you are looking for. Refer to Balancer documentation to learn how to interact with the contracts.

- [Balancer documentation](https://docs.balancer.finance/)
- [Solidity contracts for Balancer v1](https://github.com/balancer-labs/balancer-core/tree/master/contracts)