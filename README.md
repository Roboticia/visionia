# Visionia
Factory camera

<h1><h1>
<h2>Installation</h2>
  Les drivers sont à monter hors du docker
https://www.arducam.com/docs/camera-for-jetson-nano/mipi-camera-modules-for-jetson-nano/driver-installation/
  
```sh
wget https://github.com/ArduCAM/MIPI_Camera/releases/download/v0.0.3/install_full.sh
chmod +x install_full.sh
./install_full.sh -m arducam
```  
  
  
  
  
<p>  
On installe quelques bibliothèques de manière classique et update pip.
  
```sh
apt-get update -y
python3 -m pip install --upgrade pip
apt install libavdevice-dev libavfilter-dev libopus-dev libvpx-dev pkg-config python3-dev  libavformat-dev libavcodec-dev  libavutil-dev libswscale-dev -y libswresample-dev -y
```

Il nous faut maintenant installer ffmpeg avec une routine consacrée au Jetson nano : https://github.com/jocover/jetson-ffmpeg
Cependant il n'est pas possible de faire cela dans un dockerfile à cause d'un accès à un fichier important du hardware :
```sh
  /usr/src/jetson_multimedia_api/samples/common/classes/NvBuffer.cpp
```
</p>
<p> 
  Nota : docker image visionia:0
  
</p>
  
  ```sh
docker run -it --device /dev/video0:/dev/video0  --name visionia --runtime nvidia --rm --net host \
           -v /home/nnvision:/home/ju  -v /usr/src/jetson_multimedia_api:/usr/src/jetson_multimedia_api \
           visionia:0.2 bash
  ```
  
<p>
  Poursuivons l'installation :
</p>
  
  
```sh  
  pip install aiortc
  pip install aiohttp
  pip install aiohttp-jinja2
  pip install v4l2
  apt-get install v4l-utils -y
```
<p>
  V4L2 fourni certains fichiers quelques peu datés, aussi nous faut il passer de Python 2.x à Python 3.x deux lignes du fichier en transtypant : 
</p> 
  
```sh
  /usr/local/lib/python3.6/dist-packages/v4l2.py
```
  
  <p>
 Ligne 197 : 
  </p>
    
  ```py
  range (1, 9) + [0x80]        -------->           list (range (1, 9)) + [0x80]
  ```
  
  <p>
Ligne 248 :
  </p>
  
  ```py
  range (0, 4) + [2]        -------->           list (range (0, 4)) + [2]
  ```
  
<p> 
  Nota : docker image visionia:0.2
  
</p>

<p>
  Installation de Darknet, version de Alexey AB
</p>
  
```sh
git clone https://github.com/AlexeyAB/darknet.git
cd darknet
```
  
<p>
On modifie le Makefile de manière à rajouter l'utilisation du GPU (permise par CUDA) et d'OpenCV
</p>

  
```py
GPU=0
CUDNN=0
CUDNN_HALF=0
OPENCV=0
AVX=0
OPENMP=0
LIBSO=0
ZED_CAMERA=0
ZED_CAMERA_v2_8=0  
```
  
<p>
  devient
</p>
  
```py
GPU=1
CUDNN=0
CUDNN_HALF=0
OPENCV=1
AVX=0
OPENMP=0
LIBSO=0
ZED_CAMERA=0
ZED_CAMERA_v2_8=0  
```
  
```sh
  make
```
