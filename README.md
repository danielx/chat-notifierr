# danielx/chat-notifierr

Sends notifications to Google Chat based on incoming webhooks from Sonarr & Radarr.

## Supported notification triggers

### Sonarr

- [ ] On Grab
- [x] On Import
- [ ] On Upgrade
- [ ] On Rename
- [ ] On Series Delete
- [ ] On Episode File Delete
- [ ] On Episode File Delete For Upgrade
- [ ] On Health Issue
- [ ] Include Health Warnings
- [ ] On Application Update

### Radarr

- [ ] On Grab
- [x] On Import
- [ ] On Upgrade
- [ ] On Rename
- [ ] On Movie Added
- [ ] On Movie Delete
- [ ] On Movie File Delete
- [ ] On Movie File Delete For Upgrade
- [ ] On Health Issue
- [ ] On Application Update

# Usage

## Configuration

| Environment variable | Required | Description                                        |
| -------------------- | -------- | -------------------------------------------------- |
| BASIC_AUTH_USERNAME  | TRUE     | The HTTP basic auth username required              |
| BASIC_AUTH_PASSWORD  | TRUE     | The HTTP basic auth password required              |
| CHAT_WEBHOOK_URL     | TRUE     | The webhook url for the webhook bot in Google Chat |
| PORT                 | FALSE    | The port the server should listen on               |

The `CHAT_WEBHOOK_URL` is found after the Google Chat webhook is created when following these steps:
https://developers.google.com/chat/how-tos/webhooks#create_a_webhook

## docker-compose example

```yaml
chat-notifierr:
  image: ghcr.io/danielx/chat-notifierr:latest
  ports:
    - "127.0.0.1:8080:8080"
  environment:
    - PORT=8080
    - BASIC_AUTH_USERNAME=<username>
    - BASIC_AUTH_PASSWORD=<password>
    - CHAT_WEBHOOK_URL=<webhook>
```

## docker cli example

```sh
docker run -d \
  --name=chat-notifierr \
  -e BASIC_AUTH_USERNAME=<username> \
  -e BASIC_AUTH_PASSWORD=<password> \
  -e CHAT_WEBHOOK_URL=<webhook> \
  -e PORT=8080 \
  -p 127.0.0.1:8080:8080 \
  --restart unless-stopped \
  ghcr.io/danielx/chat-notifierr:latest
```

## Radarr webhook setup

Point notifications to the container with method POST on the path `/api/v1/radarr`

### Example

In this example the `danielx/chat-notifierr` container runs in the same docker network as
my Radarr server with its hostname configured to `chat-notifierr`.

![radarr example](https://github.com/danielx/chat-notifierr/blob/main/example_radarr.png?raw=true)

## Sonarr webhook setup

Point notifications to the container with method POST on the path `/api/v1/sonarr`

### Example

In this example the `danielx/chat-notifierr` container runs in the same docker network as
my Sonarr server with its hostname configured to `chat-notifierr`.

![sonarr example](https://github.com/danielx/chat-notifierr/blob/main/example_sonarr.png?raw=true)
