## PyPi Dependencies

```shell
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade pygogo kubernetes prometheus-client
pip freeze > requirements.txt
sed -i '/pkg_resources/d' requirements.txt
```