# twitch-viewer-bot-py-docker

```
  twitch-viewer-bot:
    image: leandroeffinger/twitch-viewer-bot-py-docker:latest
    container_name: twitch-viewer-bot
    environment:
      PROXY_CHOICE: 2
      TWITCH_USERNAME: xqrv
      PROXY_COUNT: 20
    deploy:
      resources:
        limits:
          memory: 4G #This is the minimum memory required to run the bot
    logging:
      options:
        max-size: "10m"
#        max-file: "3"
    restart: unless-stopped
```