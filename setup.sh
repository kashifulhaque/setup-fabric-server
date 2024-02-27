python -m venv env

source env/bin/activate

pip install -r requirements.txt

python3 setup.py

sudo docker build . -t fabricserver

sudo docker run -it fabricserver
