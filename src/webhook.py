import requests

class WebHook():
    
    def __init__(self, wh_url, avatar_url, username, discord_id):
        self.wh_url = wh_url
        self.avatar_url = avatar_url
        self.username = username
        self.content = ""
        self.discord_id = discord_id


    def post(self):
        print("self.content: ", self.content)
        data = {
        "username" : f"{self.username}",
        "avatar_url": f"{self.avatar_url}",
        "content" : f"{self.content}"
        }
        # print(data)
        result = requests.post(self.wh_url, json = data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print(f"Payload delivered successfully, code {result.status_code}.")

    def mimic(self, mentioned):
        self.avatar_url = mentioned.avatar_url
        self.username = mentioned.name
        # self.content = last_msg
        # self.post()
        




#leave this out if you dont want an embed
#for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
# data["embeds"] = [
#     {
#         "description" : "text in embed",
#         "title" : "embed title"
#     }
# ]
