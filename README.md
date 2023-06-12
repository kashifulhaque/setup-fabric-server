## Fabric server script

A simple python script to setup the latest fabric server on Linux

## Steps to run
1. Clone the repo `git clone https://github.com/kashifulhaque/setup-fabric-server`
2. `cd` into the repo `cd setup-fabric-server`
3. [OPTIONAL] Create a virtual environment `python3 -m venv .venv`
4. [OPTIONAL] Activate the virtual environment `source .venv/bin/activate`
5. Install the dependencies `pip install -r requirements.txt`
6. Run the setup `python setup.py`
7. `cd` into the fabric server directory `cd fabric_server`
8. Start the server by running `sh start.sh` (Requires `screen` to be installed)
9. `screen` can be installed on Debian, Ubuntu and other Debian and Ubuntu based OS by running `sudo apt install -y screen`
