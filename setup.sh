python -m venv env

source env/bin/activate

pip install -r requirements.txt

if [ -f "setup.py" ]; then
    python3 setup.py
fi

sudo docker build . -t fabricserver

sudo docker run -it fabricserver
