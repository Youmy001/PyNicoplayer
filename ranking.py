import re
import feedparser


def parse_entry(entry):
    """Extract data from the xml entry"""
    item = dict()
    p = re.compile('([a-z]{2})?([0-9]+)')
    smile = p.search(entry['link'])

    re_title = re.compile('alt=\"(.*?)\"')
    re_position = re.compile('第([0-9]+)位')
    re_points = re.compile('\<strong class\=\".*?\"\\>([0-9,]+)?\<\/strong\>pts\.')
    re_views = re.compile('再生：\<strong class\=\".*?\"\\>([0-9,]+)?\<\/strong\>')
    re_mylists = re.compile('マイリスト：\<strong class\=\".*?\"\\>([0-9,]+)?\<\/strong\>')
    re_comments = re.compile('コメント：\<strong class\=\".*?\"\\>([0-9,]+)?\<\/strong\>')

    item['position'] = re_position.search(entry['title']).group(1)
    item['title'] = re_title.search(entry['description']).group(1)
    item['link'] = entry['link']
    item['thumbnail'] = "http://tn.smilevideo.jp/smile?i=" + smile.group(2) + ".L"
    item['points'] = re_points.search(entry['description']).group(1)
    item['views'] = re_views.search(entry['description']).group(1)
    item['mylists'] = re_mylists.search(entry['description']).group(1)
    item['comments'] = re_comments.search(entry['description']).group(1)

    return item


def ranking_top_ten(category, period='daily', segment='fav'):
    """Fetch the top 10 of a ranking"""
    videos = list()
    url = "http://www.nicovideo.jp/ranking/" + segment + "/" + period + "/" + category + "?rss=2.0"

    feed = feedparser.parse(url)
    position = 1

    for item in feed['items']:
        if position > 10:
            break

        videos.append(parse_entry(item))
        position += 1

    return videos


def ranking(category, period='daily', segment='fav'):
    """Fetch all the entries of a ranking"""
    videos = list()
    url = "http://www.nicovideo.jp/ranking/" + segment + "/" + period + "/" + category + "?rss=2.0"

    feed = feedparser.parse(url)

    for item in feed['items']:
        videos.append(parse_entry(item))

    return videos


