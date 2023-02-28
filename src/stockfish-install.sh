# Stockfish installation (to execute with sudo)
# Create for docker
# playechess.com
# Any ARM support

apt-get update
apt-get install -y git make g++ wget
git clone https://github.com/official-stockfish/Stockfish
cd Stockfish/src && CXXFLAGS='-march=native' make -j2 profile-build ARCH=x86-64-bmi2 && cp ./stockfish /bin
