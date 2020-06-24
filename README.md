### Application start

```shell script
python -m venv env && source env/bin/activate
pip install -r requirements.txt

docker run --rm -d -p 127.0.0.1:27017:27017 --name shop-service mongo

python -m app
```

### Tests (httpie/curl)

**create product**

```shell script
http post localhost:13031/product \
product_id="000000000001" name="AMD Ryzen 9 3900X" \
params:='[{"core": 12}, {"L3": 64}]'
```

```shell script
curl localhost:13031/product --request POST \
--data '{"product_id": "000000000001", "name": "AMD Ryzen 9 3900X",
"params": [{"core": 12}, {"L3": 64}]}'
```

**find product by parameter**

```shell script
http get localhost:13031/products params:='{"core": 12}'
```

```shell script
curl localhost:13031/products --request GET --data '{"params": {"core": 12}}'
```

**find product by barcode value**

```shell script
http get localhost:13031/products product_id="000000000001"
```

```shell script
curl localhost:13031/product --request GET --data '{"product_id": "000000000001"}'
```

**multifilter**

```shell script
http get localhost:13031/products \
name="ryzen" params:='{"core": 6, "thread": 12}'
```

```shell script
curl localhost:13031/products --request GET \
--data '{"name": "ryzen", "params": {"core": 6, "thread": 12}}'
```

```json
[
    {
        "description": "Empty",
        "id": "5ee6883326d3f39b1c16e50d",
        "name": "AMD Ryzen 5 3600",
        "params": [
            {
                "core": 6
            },
            {
                "thread": 12
            },
            {
                "speed": 3.6
            },
            {
                "L3": 32
            }
        ],
        "product_id": "1234567891233"
    },
    {
        "description": "Сокет SocketAM4, ядро Pinnacle Ridge, ядер — 6, потоков — 12...",
        "id": "5ee6883326d3f39b1c16e50c",
        "name": "AMD Ryzen 5 2600",
        "params": [
            {
                "core": 6
            },
            {
                "thread": 12
            },
            {
                "speed": 3.4
            }
        ],
        "product_id": "123456789123"
    }
]
```
