    FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    zsh \ 
    wget 

# Default powerline10k theme, no plugins installed
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-syntax-highlighting

RUN chsh -s $(which zsh)

RUN apt-get update && apt-get install -y  \
    python3 \
    python3-pip \
    git-lfs

ENV COSMOS_CONNECTION_STRING "mongodb://inf2003-project:9XygVh5kKnrscIiKfsPXCos1KtjQtFSmMcZfwod9O22zosZE3ZUHrVVbtSQs262Jvv5IwpiFeOUWACDbJsgL2A==@inf2003-project.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&maxIdleTimeMS=120000&appName=@inf2003-project@"