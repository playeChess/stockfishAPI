# Stockfish Dockerfile
# playechess.com
# ARM support

FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y git make g++ wget
RUN git clone https://github.com/official-stockfish/Stockfish
RUN cd Stockfish/src && CXXFLAGS='-march=native' make -j2 profile-build ARCH=armv8 && cp ./stockfish /bin
