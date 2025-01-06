# Use the Docker-in-Docker (dind) base image
FROM docker:24.0-dind

# Switch to root to install necessary packages
USER root

# Install prerequisites: wget, tar, and supervisor
RUN apk add --no-cache \
    bash \
    curl \
    wget \
    tar \
    openjdk11-jdk \
    supervisor

# Set Java environment variables required by Flink
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Apache Flink
ENV FLINK_VERSION=1.13.0
ENV SCALA_VERSION=2.12
ENV FLINK_HOME=/opt/flink

RUN wget https://archive.apache.org/dist/flink/flink-${FLINK_VERSION}/flink-${FLINK_VERSION}-bin-scala_${SCALA_VERSION}.tgz \
    && tar -xzf flink-${FLINK_VERSION}-bin-scala_${SCALA_VERSION}.tgz -C /opt \
    && rm flink-${FLINK_VERSION}-bin-scala_${SCALA_VERSION}.tgz \
    && ln -s /opt/flink-${FLINK_VERSION} ${FLINK_HOME}

ENV PATH=${FLINK_HOME}/bin:$PATH

# Copy custom entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Flink ports
EXPOSE 6121 6122 6125 8081

# Use custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
