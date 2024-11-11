pkg upgrade -y
pkg install git -y
pkg install python -y
yes | pip install cython
pkg install libxml2 libxslt -y
pkg install -y python ndk-sysroot clang make libjpeg-turbo -y
pkg install clang -y
yes |pip install lxml
yes |pip install --pre uiautomator2 
yes |pip install pure-python-adb 
pkg install android-tools -y
yes |pip install flask
yes |pip install xmltodict 
pkg update -y

cd ngrok
bash install_ngrok.sh -y
