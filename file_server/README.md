# Start only image Server

```bash
docker compose -f docker-compose.yml up --build image-server
```

# Upload image

```bash
curl -X POST -F "image=@'my_file_name" -F "project_id=3" -F "issue_id=4" http://localhost:5000/dump
```

# Show image

Open ```localhost:5000/images/<project_id>/<issue_id>/<file_name>``` in your browser of choice and see your wonderfull image
