import requests as req
async def send_telegram(text: str,id):
    token = "2049895477:AAFFR2KnGkigpt9egqJK09fesZGi2QxAB2I"
    url = "https://api.telegram.org/bot"
    channel_id = id
    url += token
    method = url + "/sendMessage"
    r = req.post(method, data={
         "chat_id": channel_id,
         "text": text
          })
    if r.status_code != 200:
        raise Exception("post_text error")