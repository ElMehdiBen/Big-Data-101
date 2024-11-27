```
docker run --name nifi-registry -p 18080:18080 -d apache/nifi-registry:latest
```

Try it on

```
http://localhost:18080/nifi-registry
```

Configure it using IP address

```
docker inspect nifi-registry
```

Use its IP address to configure in Nifi Web Server and start trying version control
