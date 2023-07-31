# Fundamental
import json

from aiohttp.web_fileresponse import FileResponse
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from api.deps import get_current_lcu
from core.config import settings
from utils.config import config
from utils.common import save_setting, read_setting
from lcu import lcu

router = APIRouter()


@router.get('/current-summoner')
async def _(instance: lcu = Depends(get_current_lcu)):
    """获取用户简略信息"""
    try:
        return await instance.current_summoner_info()
    except:
        return HTTPException(status_code=401)


@router.get('/summoner/{summonerId}')
async def _(summonerId: str, instance: lcu = Depends(get_current_lcu)):
    """获取用户简略信息"""
    try:
        return await instance.get_info_by_id(summonerId)
    except:
        return HTTPException(status_code=401)


@router.get('/summoner-bypuuid/{puuid}')
async def _(puuid: str, instance: lcu = Depends(get_current_lcu)):
    """获取用户简略信息"""
    return await instance.get_info_by_puuid(puuid)


@router.get('/summoner-byname/{summonerName}')
async def _(summonerName: str, instance: lcu = Depends(get_current_lcu)):
    """获取用户简略信息"""
    return await instance.get_info_by_name(summonerName)


@router.get('/current-summoner-profile')
async def _(instance: lcu = Depends(get_current_lcu)):
    """获取当前用户简略信息"""
    return await instance.current_summoner_profile()


@router.get('/summoner-profile/{puuid}')
async def _(puuid: str, instance: lcu = Depends(get_current_lcu)):
    """获取用户简略信息"""
    return await instance.get_profile_by_puuid(puuid)


@router.get('/rank-status/{puuid}')
async def _(puuid: str, instance: lcu = Depends(get_current_lcu)):
    """获取用户段位信息"""
    return await instance.get_rank_summary(puuid)


@router.get('/environment')
async def _(instance: lcu = Depends(get_current_lcu)):
    """获取所在大区"""
    return await instance.environment


@router.get('/recent-20/{puuid}')
async def _(puuid: str, instance: lcu = Depends(get_current_lcu)):
    """获取近20条数据"""
    return await instance.get_rencent_20_data(puuid)


@router.get('/match-detail/{gameId}')
async def _(gameId: str, instance: lcu = Depends(get_current_lcu)):
    """获取详细对局数据"""
    return await instance.handle_match_detail(gameId)


@router.get('/match/{gameId}')
async def _(gameId: str, instance: lcu = Depends(get_current_lcu)):
    """获取标准对局数据"""
    return await instance.get_match(gameId)


@router.get('/get_rank_list/{puuid}')
async def _(puuid: str, beginIdx: int, endIdx: int, instance: lcu = Depends(get_current_lcu)):
    """获取对局列表"""
    return await instance.get_rank_list_by_puuid(beginIdx, endIdx, puuid)


@router.get('/paneldata-champselect')
async def _(instance: lcu = Depends(get_current_lcu)):
    """获取房间内英雄选择面板信息"""
    return await instance.get_teammate_info()


@router.get('/paneldata-game')
async def _(instance: lcu = Depends(get_current_lcu)):
    """获取游戏中英雄选择面板信息"""
    return await instance.get_players_info()


@router.get('/state')
async def _(instance: lcu = Depends(get_current_lcu)):
    """获取lcuapi连接情况"""
    return instance.state


@router.post('/change-setting')
async def _(new_setting: str = Body()):
    """更改设置"""
    config.update(json.loads(new_setting))


@router.post('/5v5practice')
async def _(instance: lcu = Depends(get_current_lcu)):
    """5v5训练营"""
    return await instance.create_55practice()


@router.post('/forgeRank')
async def _(rtier: str = Body(), rdivision: str = Body(), rqueue: str = Body(),
            instance: lcu = Depends(get_current_lcu)):
    """伪造段位"""
    return await instance.set_rank(rtier, rdivision, rqueue)


@router.post('/change-status/{status}')
async def _(status: str, instance: lcu = Depends(get_current_lcu)):
    """修改个人状态"""
    return await instance.set_status(status)


@router.post('/change-name')
async def _(name: str = Body(), instance: lcu = Depends(get_current_lcu)):
    """修改游戏内名字"""
    return await instance.set_name(name)


@router.post('/change-sign')
async def _(sign: str = Body(), instance: lcu = Depends(get_current_lcu)):
    """修改个人签名"""
    return await instance.set_sign(sign)


@router.post('/change-profileIcon/{profileIconId}')
async def _(profileIconId: int, instance: lcu = Depends(get_current_lcu)):
    """修改游戏头像"""
    await instance.update_icon(profileIconId)


@router.post('/change-bgSkin/{bgSkinId}')
async def _(bgSkinId: int, instance: lcu = Depends(get_current_lcu)):
    """修改生涯背景图"""
    print(await instance.set_background_skin(bgSkinId))


@router.get('/friend-history')
async def _(instance: lcu = Depends(get_current_lcu)):
    """获取好友历史"""
    return await instance.get_friend_record()


@router.get('/get-app-setting')
async def _():
    """获得本地设置"""
    return config.data


@router.post('/change-app-setting')
async def _(new_config: dict = Body()):
    """修改本地设置"""
    # new_config = json.loads(new_config)
    await config.save(new_config)


@router.post('/load-game-setting')
async def _(instance: lcu = Depends(get_current_lcu)):
    """加载游戏设置"""
    setting = await read_setting(settings.SETTING_PATH)
    input_setting = await read_setting(settings.INPUT_SETTING_PATH)
    await instance.set_setting(setting)
    await instance.set_input_setting(input_setting)


@router.post('/loot-dissolve')
async def _(instance: lcu = Depends(get_current_lcu)):
    """分解战利品"""
    return await instance.loot_dissolve()


@router.post('/save-game-setting')
async def _(instance: lcu = Depends(get_current_lcu)):
    """保存游戏设置"""
    setting = await instance.get_setting()
    input_setting = await instance.get_input_setting()
    await save_setting(settings.SETTING_PATH, setting)
    await save_setting(settings.INPUT_SETTING_PATH, input_setting)


@router.get('/skin/{championId}')
async def _(championId: int, instance: lcu = Depends(get_current_lcu)):
    """获取英雄json"""
    return await instance.get_skins(championId)


@router.get('/imgs/{folder}/{file}')
async def _(folder: str, file: str):
    """获取静态资源"""
    try:
        filepath = settings.IMGS_PATH / folder / file
        return FileResponse(filepath)
    except:
        return False


@router.post('/send_msg')
async def _(msg: str = Body(), type: str = Body(), instance: lcu = Depends(get_current_lcu)):
    """发送牛马评分"""
    await instance.send_remarks(msg, type)