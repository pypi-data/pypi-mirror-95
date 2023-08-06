# PayUnit
<p align="center">
    <a href="https://github.com/noderedis/node-redis/">
        <img width="190px" src="https://static.invertase.io/assets/node_redis_logo.png" />
    </a>
    <h2 align="center">PayUnit</h2>
    <h4 align="center">An python payment sdk for MTN Mobile Money,Orange Money,Express Union and Yup transactions.</h4>
</p>



## Installation

```bash
pip install payunit
```

## Usage

#### Example

```js
from payUnit import payUnit

# Enter your config details as parameters
payment = payunit({
    "apiUsername": "",
    "apiPassword": "",
    "api_key": "",
    "return_url": "",
    "notify_url": "",
    "total_amount": "",
    "return_url":"",
    "purchaseRef": "",
    "description":"",
    "name": "",
    "currency":"",
})


# Spawns a new transaction process of 4000
payment.makePayment(4000)
```
