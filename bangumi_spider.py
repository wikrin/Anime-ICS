import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import *

headers = {'User-Agent': 'wikrin/Anime-ICS (https://github.com/wikrin/Anime-ICS)'}


def geturlist(uid: str):
    url_list = []
    name_idDict = {}
    listHomePage = requests.get(
        f"https://bangumi.tv/anime/list/{uid}/do", headers=headers
    )
    listHomePageSoup = BeautifulSoup(listHomePage.content, "html.parser")
    fanh = listHomePageSoup.find_all("h3")
    for fana in fanh:
        fan = fana.find('a')
        url_list.append(re.sub(r'\D', "", fan.get("href")))
        name_idDict[re.sub(r'\D', "", fan.get("href"))] = fan.string
    return url_list, name_idDict


def bgmdata(id: str):
    bgmApiData = requests.get(
        f"https://api.bgm.tv/v0/episodes?subject_id={id}&type=0", headers=headers
    )
    bgmapiJS = bgmApiData.json()
    bgmDict = {
        id: [
            {
                'ep': str(apidata['ep']),
                'id': apidata['subject_id'],
                'epid': apidata['id'],
                'airdate': apidata['airdate'],
                'duration_seconds': apidata['duration_seconds'],
            }
            for apidata in bgmapiJS['data']
        ]
    }
    return bgmDict


def bangumidata(idlist: list):
    bangumiData = requests.get("https://unpkg.com/bangumi-data@0.3/dist/data.json")
    bgmdataJS = bangumiData.json()
    time_idDict = {
        sites['id']: items['begin'][11:19]
        for items in bgmdataJS['items']
        for sites in items['sites']
        if sites['site'] == "bangumi" and sites['id'] in idlist
    }
    bangumiData.status_code
    return time_idDict


def enddata(bgmDict: dict, name_idDict: dict, time_idDict: dict, id: str):
    icslist = []
    ep_name = name_idDict.get(id, "获取失败!")
    temptime = time_idDict.get(id, "15:00:00")
    for eplist in bgmDict[id]:
        if eplist['airdate'] == '':
            continue
        op_time = eplist['airdate'] + " " + temptime
        if eplist['duration_seconds'] == 0:
            play_time = 1440
        else:
            play_time = eplist['duration_seconds']
        dtstart = datetime.strptime(op_time, "%Y-%m-%d %H:%M:%S")
        dtstamp = dtstart + timedelta(seconds=play_time)
        icslist.append(
            {
                'summary': "[ep." + eplist['ep'] + "] " + ep_name,
                'id': eplist['id'],
                'epid': eplist['epid'],
                'dtstart': dtstart.strftime("%Y%m%dT%H%M%SZ"),
                'dtstamp': dtstamp.strftime("%Y%m%dT%H%M%SZ"),
            }
        )
    return icslist


def ics_header():
    return (
        "BEGIN:VCALENDAR\n"
        + "PRODID:-//Anime broadcast time Calendar//CN\n"
        + "VERSION:2.0\n"
        + "CALSCALE:GREGORIAN\n"
        + "METHOD:PUBLISH\n"
        + "X-WR-CALNAME:番剧放送\n"
        + "X-WR-TIMEZONE:Asia/Shanghai\n"
        + "BEGIN:VTIMEZONE\n"
        + "TZID:Asia/Shanghai\n"
        + "X-LIC-LOCATION:Asia/Shanghai\n"
        + "BEGIN:STANDARD\n"
        + "TZOFFSETFROM:+0800\n"
        + "TZOFFSETTO:+0800\n"
        + "TZNAME:CST\n"
        + "DTSTART:19700101T000000\n"
        + "END:STANDARD\n"
        + "END:VTIMEZONE\n"
    )


def body_ics(icsDict: dict):
    return (
        "BEGIN:VEVENT\n"
        + f"DTSTART;VALUE=DATE-TIME:{icsDict['dtstart']}\n"
        + f"DTEND;VALUE=DATE-TIME:{icsDict['dtstamp']}\n"
        + f"DTSTAMP:{icsDict['dtstart']}\n"
        + f"UID:{icsDict['id']}-{icsDict['epid']}\n"
        + f"CREATED:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\n"
        + f"SUMMARY:{icsDict['summary']}\n"
        + f"DESCRIPTION:https://bgm.tv/ep/{icsDict['epid']}\n"
        + "TRANSP:OPAQUE\n"
        + "SEQUENCE:0\n"
        + "STATUS:CONFIRMED\n"
        + f"LAST-MODIFIED:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\n"
        + "END:VEVENT\n"
    )


def save_ics(file, str, mode='w'):
    with open(f'./ics/{file}.ics', mode, encoding='utf-8') as ics:
        ics.write(str)
