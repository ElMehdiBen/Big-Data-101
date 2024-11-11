**YUM**

```
sudo sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
sudo sed -i -e '/^#baseurl=http:\/\/mirror.centos.org/p;s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
sudo yum update -y
sudo yum install nano -y
```

**Script**

```
sudo wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz --no-check-certificate
mkdir /opt/spark
mv spark-3.5.0-bin-hadoop3.tgz /opt/spark/
tar -zxvf /opt/spark/spark-3.5.0-bin-hadoop3.tgz -C /opt/spark

sudo yum install -y python3
sudo unlink /usr/bin/python
sudo ln -s /usr/bin/python3 /usr/bin/python

sudo wget https://dlcdn.apache.org/zeppelin/zeppelin-0.11.0/zeppelin-0.11.0-bin-all.tgz
tar zxvf zeppelin-0.11.0-bin-all.tgz 
mv zeppelin-0.11.0-bin-all /opt/zeppelin
cp /opt/zeppelin/conf/zeppelin-env.sh.template /opt/zeppelin/conf/zeppelin-env.sh

export JAVA_HOME=/usr/lib/jvm/jre/
export ZEPPELIN_ADDR=0.0.0.0
export SPARK_HOME=/opt/spark/spark-3.5.0-bin-hadoop3

/opt/zeppelin/bin/zeppelin-daemon.sh start
/opt/zeppelin/bin/zeppelin-daemon.sh status
```

**DFS**


```
hdfs dfs -mkdir /user/training
hdfs dfs -chown hdfs /user/training
hdfs dfs -chmod 777 /user/training
hdfs dfs -put count.txt /user/training/wordcount
hdfs dfs -put -f count.txt /user/training/wordcount
hdfs dfs -rm -r /user/training/wordcount/output

hdfs dfs -setrep -w 2 /user/training/wordcount/count.txt
```

**Web HDFS**

```
curl -i "http://localhost:9870/webhdfs/v1/user?op=LISTSTATUS"
```

**MapReduce**

```
echo 'hello mapreduce hello' >> input.txt

yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 10 15
yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/training/wordcount/count.txt /user/training/wordcount/output
yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordmean /user/training/wordcount/count.txt /user/training/wordcount/outputmean
yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar sudoku sudoku.txt
```
