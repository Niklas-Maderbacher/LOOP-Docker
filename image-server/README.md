# Start only image Server

```bash
docker compose -f docker-compose.yml up --build image-server
```

# Upload image

```bash
curl -X POST -F "image=@'my_file_name" http://localhost:5000/image
```

# Show image

Open ```localhost:5000/images/<my_file_name>``` in your browser of choice and see your wonderfull image
