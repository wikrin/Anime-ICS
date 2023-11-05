'''
sel内填写播放源,以下标为优先级

值:                 代表为:
acfun               AcFun
bilibili            哔哩哔哩
bilibili_hk_mo_tw   哔哩哔哩（港澳台）
bilibili_hk_mo      哔哩哔哩（港澳）
bilibili_tw         哔哩哔哩（台灣）
sohu                搜狐视频
youku               优酷
qq                  腾讯视频
iqiyi               爱奇艺
letv                乐视
pptv                PPTV
mgtv                芒果tv
nicovideo           Niconico
netflix             Netflix
gamer               動畫瘋
muse_hk             木棉花 HK
ani_one             Ani-One中文官方動畫頻道
ani_one_asia        Ani-One Asia 
viu                 Viu 
mytv                myTV SUPER 
disneyplus          Disney+ 
nowPlayer           Now Player 
dmhy                动漫花园
'''

sel = ['ani_one', 'gamer', 'dmhy', 'netflix', 'muse_hk']


# def timeit(func):
#     def wrapper(*arges, **kwargs):
#         t1 = time.time()
#         result = func(*arges, **kwargs)
#         t2 = time.time()
#         print(t2 - t1)
#         return result

#     return wrapper


def sel_begin(bgm_data: dict[str, tuple[str, dict]]) -> dict:
    id_begin: dict = {id: jptv[0] for (id, jptv) in bgm_data.items()}
    # for id, begin in bgm_data.items():
    #     for meta in sel:
    #         if meta in begin[-1]:
    #             id_begin[id] = begin[-1][meta]
    #         else:
    #             continue
    id_begin.update(
        {
            id: begin[-1][meta]
            for id, begin in bgm_data.items()
            for meta in sel
            if meta in begin[-1]
        }
    )
    return id_begin
