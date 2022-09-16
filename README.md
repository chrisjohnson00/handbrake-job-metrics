## PyPi Dependencies

```shell
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade kubernetes prometheus-client flask pygogo gunicorn
pip freeze > requirements.txt
sed -i '/pkg_resources/d' requirements.txt
```