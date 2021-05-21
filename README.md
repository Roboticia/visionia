# Visionia
Factory camera

<h1><h1>
<h2>Installation</h2>
  Les drivers sont à monter hors du docker
https://www.arducam.com/docs/camera-for-jetson-nano/mipi-camera-modules-for-jetson-nano/driver-installation/
  
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
  docker run -it --name visionia --runtime nvidia --rm --net host -v /home/nnvision:/home/ju -v /dev/video0 -v /usr/src/jetson_multimedia_api:/usr/src/jetson_multimedia_api visionia:0 bash
  ```
  
<p>
  Poursuivons l'installation :
</p>
  
  
```sh  
  pip install aiortc
  pip install aiohttp
  pip install aiohttp-jinja2
  pip install v4l2
```
<p>
  V4L2 fourni certains fichiers quelques peu datés, qussi nous faut il passer de Python 2.x à Python 3.x deux lignes du fichier : 
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
