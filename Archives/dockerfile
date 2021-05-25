FROM nvcr.io/nvidia/l4t-ml:r32.4.4-py3

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install  Pillow psutil

RUN apt-get update

RUN apt-get install cmake git libgtk2.0-dev pkg-config \
                     libavcodec-dev libavformat-dev libswscale-dev
RUN mkdir ~/src
RUN cd ~/src
RUN git clone https://github.com/opencv/opencv.git
RUN cd opencv
RUN mkdir build && cd build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D INSTALL_C_EXAMPLES=ON ..
RUN make -j$(nproc)

RUN make install

RUN cd ~/src/opencv/samples
RUN cmake .
RUN make




#RUN pip3 install opencv-python

####WORK UNTIL THERE

# Compile OpenCV
# start from opencv image ready : https://forums.developer.nvidia.com/t/process-to-install-opencv-4-1-on-nano/75801
# https://github.com/mdegans/nano_build_opencv/tree/docker  mdegans/tegra-opencv:latest
#RUN cd opencv-4.4.0 && mkdir build && cd build && wget https://github.com/opencv/opencv/archive/3.0.0.zip &&  \
#    cmake -D CMAKE_BUILD_TYPE=RELEASE \
#-D CMAKE_INSTALL_PREFIX=/usr/local \
#-D INSTALL_PYTHON_EXAMPLES=OFF \
#-D INSTALL_C_EXAMPLES=OFF \
#-D OPENCV_ENABLE_NONFREE=ON \
#-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.4.0/modules \
#-D BUILD_EXAMPLES=OFF ... && \
#    make && make install && ln -s /usr/local/python/cv2/python-3.6/cv2.cpython-36m-aarch64-linux-gnu.so /usr/local/lib/python3.6/dist-packages/cv2.so && ldconfig \
#    && cd ../.. && rm -rf opencv-4.4.0/ opencv_contrib-4.4.0/



#RUN apt-get update && apt-get install -y \ 
#    wget \
#    build-essential \ 
#    cmake \ 
#    git \
#    unzip \ 
#    pkg-config \
#    python-dev \ 
#    python-opencv \ 
#    libopencv-dev \ 
#    libav-tools  \ 
#    libjpeg-dev \ 
#    libpng-dev \ 
#    libtiff-dev \ 
#    libjasper-dev \ 
#    libgtk2.0-dev \ 
#    python-numpy \ 
#    python-pycurl \ 
#    libatlas-base-dev \
#    gfortran \
#    webp \ 
#    python-opencv \ 
#    qt5-default \
#    libvtk6-dev \ 
#    zlib1g-dev 

# Install Open CV - Warning, this takes absolutely forever
RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/opencv/opencv/archive/4.4.0.zip && \
    unzip 4.4.0.zip && \
    rm 4.4.0.zip && \
    mv opencv-4.4.0 OpenCV && \
    cd OpenCV && \
    mkdir build && \ 
    cd build && \
    cmake \    
    -DWITH_QT=ON \ 
    -DWITHOPENGL=ON \ 
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON .. && \
    make -j4 && \
    make install && \ 
    ldconfig

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app 




#RUN apt-get update && apt-get install -y apt-utils && rm -rf /var/lib/apt/lists/*

# Set the locale
#RUN  apt-get update && apt-get install locales && locale-gen en_US.UTF-8 && rm -rf /var/lib/apt/lists/*
#ENV LANG en_US.UTF-8
#ENV LANGUAGE en_US:en
#ENV LC_ALL en_US.UTF-8


#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
 #              tzdata libxml2-dev libxslt-dev \
  #             wget mlocate build-essential python3 python3-dev  openssh-client sshpass\
   #            python3-pip nano cron yasm pkg-config cmake libjpeg-dev \
    #           libpng-dev libtiff-dev libavcodec-dev libavformat-dev \
     #          libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran libpq-dev \
      #         && rm -rf /var/lib/apt/lists/*


#RUN pip3 install cython psutil Pillow numpy requests 


# Compile OpenCV essai 2
# start from opencv image ready : https://forums.developer.nvidia.com/t/process-to-install-opencv-4-1-on-nano/75801 
# https://github.com/mdegans/nano_build_opencv/tree/docker  mdegans/tegra-opencv:latest
#RUN cd opencv-3.4.4 && mkdir build && cd build && \
#    cmake -D CMAKE_BUILD_TYPE=RELEASE \
#	-D CMAKE_INSTALL_PREFIX=/usr/local \
#	-D INSTALL_PYTHON_EXAMPLES=OFF \
#	-D INSTALL_C_EXAMPLES=OFF \
#	-D OPENCV_ENABLE_NONFREE=ON \
#	-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.4/modules \
#	-D BUILD_EXAMPLES=OFF .. && \
#   make && make install && ln -s /usr/local/python/cv2/python-3.6/cv2.cpython-36m-aarch64-linux-gnu.so /usr/local/lib/python3.6/dist-packages/cv2.so && ldconfig \
#    && cd ../.. && rm -rf opencv-3.4.4/ opencv_contrib-3.4.4/



# Compile OpenCV
#RUN cd opencv-4.3.0 && mkdir build && cd build && \
#    cmake -D CMAKE_BUILD_TYPE=RELEASE \
#-D CMAKE_INSTALL_PREFIX=/usr/local \
#-D INSTALL_PYTHON_EXAMPLES=OFF \
#-D INSTALL_C_EXAMPLES=OFF \
#        -D OPENCV_GENERATE_PKGCONFIG=ON \
#-D OPENCV_ENABLE_NONFREE=ON \
#-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.3.0/modules \
#-D BUILD_EXAMPLES=OFF .. && \
#    make && make install && ln -s /usr/local/python/cv2/python-3.6/cv2.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/dist-packages/cv2.so && ldconfig \
#    && cd ../.. && rm -rf opencv-4..3.0/ opencv_contrib-4.3.0/


RUN git clone https://github.com/AlexeyAB/darknet.git

RUN cd darknet &&  sed -i '1,10s/GPU=.*/GPU=1/' Makefile && sed -i '1,10s/CUDNN=.*/CUDNN=1/' Makefile && \
                   sed -i '1,10s/OPENCV=.*/OPENCV=1/' Makefile && sed -i '1,10s/LIBSO=.*/LIBSO=1/' Makefile &&  \
                   sed -i '1,10s/CUDNN_HALF=.*/CUDNN_HALF=1/' Makefile && \
                   make -s  --no-print-directory && \
                   rm -rf backup include scripts src results examples && rm L* M* R*

RUN gh repo clone Roboticia/visionia
