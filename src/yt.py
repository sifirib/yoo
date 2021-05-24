import requests
from bs4 import BeautifulSoup as bs



args = "devletsah dondurma"

base = "https://www.youtube.com/results?search_query="

query = args.split()
search_url = base + '+'.join(query)

print(search_url)
search_result = requests.get(search_url).text
soup = bs(search_result, 'html.parser')
videos = soup.find_all("a", id="yt-simple-endpoint style-scope ytd-video-renderer")
# videos = soup.select(".yt-uix-tile-link")
if not videos:
    raise KeyError("No video found")
url = "https://www.youtube.com" + videos[0]["href"]
print(url)



# page = r.text
# soup = bs(page, "html.parser")
# # vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
# vids = soup.findAll('a',attrs={'class':'yt-simple-endpoint style-scope ytd-video-renderer'})


# videolist=[]
# for v in vids:
#     tmp = 'https://www.youtube.com' + v['href']
#     videolist.append(tmp)

# # url = soup.find('a', attrs={'class':'yt-uix-tile-link'})['href']  # only first video
# print(vids)


# videos_search = VideosSearch(query, limit=1)
# results = videos_search.result()["result"][0]
# url_of_music = results["link"]
# view_count = results["viewCount"]["short"]
# published_time = results["publishedTime"]
# print(url_of_music)

# await ctx.send(f":globe_with_meridians: {view_count} :cyclone: {published_time}\n{url_of_music}")