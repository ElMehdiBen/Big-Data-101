hadoop fs -chmod 777 /

sudo sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
sudo sed -i -e '/^#baseurl=http:\/\/mirror.centos.org/p;s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
sudo yum update -y
sudo yum install unzip -y

sudo wget https://archive.apache.org/dist/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz --no-check-certificate
mkdir /opt/spark
mv spark-2.4.8-bin-hadoop2.7 /opt/spark/
tar -zxvf /opt/spark/spark-2.4.8-bin-hadoop2.7 -C /opt/spark

sudo yum install -y python3
sudo unlink /usr/bin/python
sudo ln -s /usr/bin/python3 /usr/bin/python

sudo wget https://dlcdn.apache.org/zeppelin/zeppelin-0.11.0/zeppelin-0.11.0-bin-all.tgz
tar zxvf zeppelin-0.11.0-bin-all.tgz 
mv zeppelin-0.11.0-bin-all /opt/zeppelin
cp /opt/zeppelin/conf/zeppelin-env.sh.template /opt/zeppelin/conf/zeppelin-env.sh

sudo wget https://archive.apache.org/dist/incubator/livy/0.7.1-incubating/apache-livy-0.7.1-incubating-bin.zip

export HADOOP_CONF_DIR=/opt/hadoop/conf
export JAVA_HOME=/usr/lib/jvm/jre/
export ZEPPELIN_ADDR=0.0.0.0
export SPARK_HOME=/opt/spark/spark-3.5.0-bin-hadoop3

sudo /opt/zeppelin/bin/zeppelin-daemon.sh start
sudo /opt/zeppelin/bin/zeppelin-daemon.sh status

sudo ./bin/livy-server start
