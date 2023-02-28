# Stockfish API Dockerfile (ARM)
# playechess.com
# If using x86_64 change last line ARCH make param

FROM ubuntu:latest

RUN apt-get update

RUN apt install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash -
RUN apt install -y nodejs

RUN apt-get install -y git make g++ wget
RUN git clone https://github.com/official-stockfish/Stockfish
RUN cd Stockfish/src && CXXFLAGS='-march=native' make -j2 profile-build ARCH=armv8 && cp ./stockfish /bin
