**YUM**

sudo sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
sudo sed -i -e '/^#baseurl=http:\/\/mirror.centos.org/p;s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

**DFS**

hdfs dfs -mkdir /user/training
hdfs dfs -chown hdfs /user/training
hdfs dfs -chmod 777 /user/training
hdfs dfs -put count.txt /user/training/wordcount
hdfs dfs -put -f count.txt /user/training/wordcount
hdfs dfs -rm -r /user/training/wordcount/output

hdfs dfs -setrep -w 2 /user/training/wordcount/count.txt

**Web HDFS**
curl -i "http://localhost:9870/webhdfs/v1/user?op=LISTSTATUS"

**MapReduce**
echo 'hello mapreduce hello' >> input.txt

yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 10 15
yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordcount /user/training/wordcount/count.txt /user/training/wordcount/output
yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar wordmean /user/training/wordcount/count.txt /user/training/wordcount/outputmean
yarn jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar sudoku sudoku.txt
