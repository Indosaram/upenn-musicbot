# Musicbot for Upenn - 성수

## Secret keys

```
api_token
client_secrets
webhook_url
playlist_id
```

Thoes keys are needed to be kept in secret, hence you should set those as a environmental variables in the repository. The source code accesses the values by `os.environ.get($SECRET_NAME)`.



## Deployment

This source is being hosted at heroku. The only requirement for heroku is `Procfile` and `runtime.txt`.