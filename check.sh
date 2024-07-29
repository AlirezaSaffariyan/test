conda install pyqt
sudo apt install qt5-default libqt5x11extras5

pip install PyQt5

export QT_QPA_PLATFORM_PLUGIN_PATH=/home/amir/miniconda3/envs/zoe/lib/python3.*/site-packages/PyQt5/Qt/plugins/platforms

ls /home/amir/miniconda3/envs/zoe/lib/python3.*/site-packages/PyQt5/Qt/plugins/platforms

# conda env create -f environment.yml
# conda activate zoe
# conda install pyqt


QT_DEBUG_PLUGINS=1 python main-ui.py