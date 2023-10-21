import os
import concurrent.futures
import bangumi_spider

try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass
if __name__ == "__main__":
    UID = os.getenv('BGM_UID')
    url_list, name_idDict = bangumi_spider.geturlist(UID)
    # time_idDict = bangumi_spider.bangumidata(url_list)

    with concurrent.futures.ThreadPoolExecutor() as bgmapi:
        futuresDict = {}
        futures = bgmapi.submit(bangumi_spider.bangumidata, url_list)
        futuresDict[futures] = 'bangumidata'
        for url in url_list:
            futures = bgmapi.submit(bangumi_spider.bgmdata, url)
            futuresDict[futures] = url

        bgmDict = {}
        for future in concurrent.futures.as_completed(futuresDict):
            if futuresDict[future] == 'bangumidata':
                time_idDict = future.result()
            else:
                bgmDict.update(future.result())

    # 以+=扩展方式合并enddata()返回的列表数据结构[{},{},  ... , {}]每一个{}为以ep为单位的键值对
    icslist = []
    for i in url_list:
        icslist += bangumi_spider.enddata(bgmDict, name_idDict, time_idDict, i)

    # 生成日程所需的数据都在icslist列表里了，for遍历icslist获得dict对象
    ics = bangumi_spider.ics_header()
    for icsdata in icslist:
        ics += bangumi_spider.body_ics(icsdata)
    ics += "END:VCALENDAR"
    # 最后写出数据至文件
    bangumi_spider.save_ics('bangumi', ics)

    # with concurrent.futures.ThreadPoolExecutor() as body_ics:
    #     bangumi_spider.save_ics(bangumi_spider.ics_header())
    #     icsstr = body_ics.map(bangumi_spider.body_ics, icslist)
    #     for ics in icsstr:
    #         bangumi_spider.save_ics(ics, 'a+')
