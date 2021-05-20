# Visionia
Factory camera

<h1><h1>
<h2>Installation</h2>
  
<p>  
On installe quelques bibliothèques de manière classique et update pip.
  
```sh
apt-get update -y
python3 -m pip install --upgrade pip
apt install libavdevice-dev libavfilter-dev libopus-dev libvpx-dev pkg-config python3-dev  libavformat-dev libavcodec-dev  libavutil-dev libswscale-dev -y libswresample-dev -y<br 
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
  pip install aiortc
  pip install aiohttp
  pip install aiohttp-jinja2
  pip install v4l2
```
<p>
  
</p> 
