# twitch-viewer-bot-py-docker

```
  twitch-viewer-bot:
    image: leandroeffinger/twitch-viewer-bot-py-docker:latest
    container_name: twitch-viewer-bot
    environment:
      PROXY_CHOICE: 2
      TWITCH_USERNAME: default_username
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

**Disclaimer:**

This project is intended for educational purposes only. 
It is designed to demonstrate the use of Docker and Selenium for automating interactions with Twitch. 
Please use it responsibly and in accordance with Twitch's terms of service.
The author assumes no liability for any misuse of this project.
