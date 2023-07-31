#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from enum import Enum


class gameMode(str, Enum):
    PRACTICE = 'PRACTICETOOL'
    CLASSIC = 'CLASSIC'
    ARAM = 'ARAM'
    TFT = 'TFT'
    URF = 'URF'

class gameType(str, Enum):
    CUSTOM = 'CUSTOM_GAME'
    MATCHED = 'MATCHED_GAME'
    TUTORIAL = 'TUTORIAL_GAME'


class msgType(str, Enum):
    ALL = 'ALL'
    SELF = 'SELF'

class ROUTE(str, Enum):
    settings = '/lol-game-settings/v1/game-settings'
    settings_schema = '/lol-game-settings/v1/game-settings-schema'
    input_settings = '/lol-game-settings/v1/input-settings'
    input_settings_schema = '/lol-game-settings/v1/input-settings-schema'
    state = '/riot-messaging-service/v1/state'
    GameFlow = '/lol-gameflow/v1/gameflow-phase'
    ChampionBench = '/lol-lobby-team-builder/champ-select/v1/session'
    dialog_message = '/lol-simple-dialog-messages/v1/messages'
    # 选人信息
    BpSession = '/lol-champ-select/v1/session'
    add_friend = '/lol-chat/v1/friend-requests'  # POST
    accept_game = '/lol-matchmaking/v1/ready-check/accept'  # post
    decline_game = '/lol-matchmaking/v1/ready-check/decline'
    reconnect_game = '/lol-gameflow/v1/reconnect'
    play_again = '/lol-lobby/v2/play-again'
    blue_essence = '/lol-inventory/v1/wallet/lol_blue_essence'
    bp_champion = '/lol-champ-select/v1/session/actions/{}'  # patch
    swap_champion = '/lol-champ-select/v1/session/bench/swap/{}'
    cancel_add_friend = '/lol-chat/v1/friend-requests/{}'  # Delete
    # 个人信息
    me = '/lol-chat/v1/me'
    environment = '/riotclient/v1/crash-reporting/environment'
    # 英雄信息
    champions = '/lol-game-data/assets/v1/champions/{id}.json'
    all_champions = '/lol-champions/v1/owned-champions-minimal'
    current_champion = '/lol-champ-select/v1/current-champion'
    # 房间信息
    session = '/lol-gameflow/v1/session'
    friend_list = '/lol-game-client-chat/v1/buddies'
    chat_info = '/lol-chat/v1/conversations/{}/messages'
    jwt = '/lol-summoner/v1/current-summoner/jwt'
    # 当前所有好友对话 id= conversation-id以及最后回复内容
    conversations = '/lol-chat/v1/conversations'
    chat_frient = "/lol-game-client-chat/v1/instant-messages"
    friend_record = '/lol-store/v1/giftablefriends'
    chat_setting = '/lol-chat/v1/settings'
    # 指定聊天的所有内容    post= {body= message type= chat}
    conversation_msg = '/lol-chat/v1/conversations/{}/messages'
    current_environment = '/riotclient/v1/crash-reporting/environment'
    game_flow = '/lol-gameflow/v1/gameflow-phase'
    match_current_summoner = '/lol-match-history/v1/products/lol/current-summoner/matches?begIndex=0&endIndex=100'
    match_ids = '/lol/match/v5/matches/by-puuid/{}/ids'
    match_detail = '/lol-match-history/v1/games/{}'
    match_list_by_id = '/lol-match-history/v3/matchlist/account/{}?begIndex={}&endIndex={}'
    match_list_by_puuid = '/lol-match-history/v1/products/lol/{}/matches?begIndex={}&endIndex={}'
    icon = '/lol-summoner/v1/current-summoner/icon'
    summoner = '/lol-summoner/v1/summoners/{}'
    summoner_by_name = '/lol-summoner/v1/summoners?name={}'
    summoner_by_puuid = '/lol-summoner/v2/summoners/puuid/{}'
    summoner_profile_by_puuid = '/lol-summoner/v1/summoner-profile?puuid={}'
    rank = '/lol-ranked/v1/ranked-stats/{}'
    profile_icon = '/lol-game-data/assets/v1/profile-icons/{}.jpg'
    current_summoner = '/lol-summoner/v1/current-summoner'
    current_summoner_profile = '/lol-summoner/v1/current-summoner/summoner-profile'
    ranked_stats = '/lol-ranked/v1/ranked-stats/{summonerId}'
    # ids = ''.join(summonerIds)
    summoners = '/lol-summoner/v2/summoners?ids={ids}'
    lobby = '/lol-lobby/v2/lobby'
    gamemode = '/lol-lobby/v1/parties/gamemode'
    lobby_bot = '/lol-lobby/v1/lobby/custom/bots'
    promote = '/lol-lobby/v2/lobby/members/{}/promote'
    search = '/lol-lobby/v2/lobby/matchmaking/search'
    invite = '/lol-lobby/v2/lobby/invitations'
    revoke_invite = '/lol-lobby/v2/lobby/members/{}/revoke-invite'
    kick = '/lol-lobby/v2/lobby/members/{}/kick'
    switch = '/lol-lobby/v1/lobby/custom/switch-teams'
    complaint = '/lol-end-of-game/v2/player-complaints'
    # 对局信息
    allgamedata = '/liveclientdata/allgamedata'
    position = '/lol-lobby/v2/lobby/members/localMember/position-preferences'
    notification = '/player-notifications/v1/notifications'
    message = '/lol-game-client-chat'
    # 英雄
    pickable = '/lol-champ-select/v1/pickable-champion-ids'
    bannable = '/lol-champ-select/v1/bannable-champion-ids'
    reroll = '/lol-champ-select/v1/session/my-selection/reroll'
    champion_skin = '/lol-game-data/assets/v1/champions/{}.json'
    # 战利品
    collection = '/lol-collections/v1/inventories/{}/champion-mastery/top?limit={}'
    loot = '/lol-loot/v1/player-loot'
    loot_map = '/lol-loot/v1/player-loot-map'
    refresh_loot = '/lol-loot/v1/refresh?force=true'
    dissolve = '/lol-loot/v1/recipes/{}/craft?repeat={}'
    # 符文
    rune = '/lol-perks/v1/pages'
    current_rune = '/lol-perks/v1/currentpage'
    spectate = '/lol-spectator/v1/spectate/launch'
    eog = "/lol-end-of-game/v1/eog-stats-block"