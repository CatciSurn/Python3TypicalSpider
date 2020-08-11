import requests

res = requests.get("https://antispider5.scrape.center/detail/1")
with open("case_5/response.html",'w',encoding="utf-8") as f:
    f.write(res.text)
print(res.text)