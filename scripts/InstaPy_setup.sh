#!/bin/bash


SEP='==========================================\n'


echo 'Installing Xvfb for headless browser capability'
echo
sudo apt install xvfb

echo -e $SEP
echo 'Updgrading Chrome to latest version'
echo 

sudo apt update
sudo apt install -y google-chrome-stable

echo -e $SEP
echo 'Where would you like to clone the InstaPy repo? (path)'
echo
read path
if [ -z "$path" ] ; then
    path="$HOME"
fi

echo -e $SEP
echo "Cloning InstaPy in $path"
echo
git clone https://github.com/timgrossmann/InstaPy.git ${path}/InstaPy

echo -e $SEP
echo "Downloading latest chromedriver"
echo
latest_version=$(wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O -)
wget https://chromedriver.storage.googleapis.com/${latest_version}/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip
unzip /tmp/chromedriver_linux64.zip
mv chromedriver ${path}/InstaPy/assets/chromedriver
chmod +x ${path}/InstaPy/assets/chromedriver
chmod 755 ${path}/InstaPy/assets/chromedriver

echo -e $SEP
echo "Creating virtual environment"
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv insta
cd ${path}/InstaPy
pip install .
# Weird step nowhere to be found in official documentation
rsync -av assets $HOME/.virtualenvs/insta/local/lib/python2.7/site-packages/

deactivate
cd -

echo -e $SEP
echo "Setup complete"
