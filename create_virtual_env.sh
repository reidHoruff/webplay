deactivate
rm -r virtual_env
virtualenv virtual_env/ --no-site-packages
source virtual_env/bin/activate
pip install -r requirements.txt