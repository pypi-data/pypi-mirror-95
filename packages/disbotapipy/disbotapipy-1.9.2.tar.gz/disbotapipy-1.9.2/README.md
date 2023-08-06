# disbotapipy
Disbot.top API Wrapper for Python
[disbot.top](https://disbot.top)

---

## Support

* [Discord](https://disbot.top/d)

* [Website](https://disbot.top)

---

## Installation

`pip install disbotapipy`

---

## Ratelimits
You can POST Server and Shard Count stats once every 5 minutes

---

## Response

**429:**
`[disbot - 429]: You are currently rate limited. You can only make one request per five minutes.`

**200:**
`[disbot - 200]: OK.`

---


**Methods**
`getVotes(clientid)`
`getInfo(clientid)`
`updateStats(client, clientid, token, servercount)`



## Updating Server Count
Working
```py
from disbotapipy import disbotapipy
token = "bot-auth-token"
clientid = "user-id-here"
serverCount = len(client.guilds)
@client.event()
async def on_ready():
    disbotapipy.disbot.updateStats(client, clientid, token, serverCount)

You can loop this as needed, but make sure to not spam the api.

**Where can I find the auth token?**

You can find your auth token via the API page on the disbot.top website

https://disbot.top/api/bottokens
*(Ensure you're logged in.)*

--- 
