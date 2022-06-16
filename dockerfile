FROM nvcr.io/nvidia/l4t-ml:r32.7.1-py3

RUN apt-get update
RUN apt-get install

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
	libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    	libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

RUN cd /usr/src
RUN wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz
RUN tar xzf Python-3.7.9.tgz
RUN cd Python-3.7.9 && ./configure --enable-optimizations && make altinstall


RUN python3 -m pip install --upgrade pip

RUN apt install libavdevice-dev libavfilter-dev libopus-dev libvpx-dev pkg-config python3-dev  libavformat-dev libavcodec-dev  libavutil-dev libswscale-dev -y libswresample-dev -y

RUN pip install aiortc && DEBIAN_FRONTEND=noninteractive apt-get install -y \
pip install aiohttp && pip install aiohttp-jinja2 && DEBIAN_FRONTEND=noninteractive apt-get install -y && pip install v4l2-fix && apt-get install v4l-utils -y && apt-get install python-opencv
 
WORKDIR /NNvision

RUN git clone https://github.com/jouvencia/tkDNN.git

RUN git clone https://github.com/andreikop/python-ws-discovery.git && cd python-ws-discovery && \
    python3 setup.py install

ENV LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

RUN git clone https://github.com/jocover/jetson-ffmpeg.git && \
    cd jetson-ffmpeg && mkdir build

RUN git clone git://source.ffmpeg.org/ffmpeg.git -b release/4.2 --depth=1 && \
    cd ffmpeg && \
    wget https://github.com/jocover/jetson-ffmpeg/raw/master/ffmpeg_nvmpi.patch


RUN git clone https://github.com/AlexeyAB/darknet

RUN cd  darknet  && \
	sed -i '1,10s/GPU=.*/GPU=1/' Makefile && \
	sed -i '1,10s/CUDNN=.*/CUDNN=1/' Makefile && \
	sed -i '1,10s/OPENCV=.*/OPENCV=1/' Makefile && \
	sed -i '1,10s/LIBSO=.*/LIBSO=1/' Makefile

WORKDIR /NNvision
COPY ./compile.sh /NNvision/compile.sh

