FROM python:3.12.4-bookworm

ARG DEBIAN_FRONTEND=noninteractive
# borrowed from https://github.com/dimmg/dockselpy/blob/master/Dockerfile
RUN BUILD_DEPS="curl unzip" && \
    apt-get update && apt-get install --no-install-recommends -y \
    wget \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 libgbm1 \
    $BUILD_DEPS \
    xvfb && \
    GECKODRIVER_VERSION='v0.34.0' && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

WORKDIR /app
COPY requirements.txt .
COPY app app
RUN pip install -r requirements.txt
RUN pip install gunicorn

VOLUME /tmp/
VOLUME /app/
VOLUME /root/

CMD python3 -m flask run -h 0.0.0.0
