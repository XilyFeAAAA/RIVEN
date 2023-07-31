#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
from pathlib import Path
import os


class Settings:
    HOST: str = '127.0.0.1'
    PORT: int = 7070
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: str = "127.0.0.1"
    PROJECT_NAME: str = "RIVEN"

    CONVERSATION_RETRY_TIME: int = 5
    CONVERSATION_RETRY_DELAY_SECOND: int = 3

    WORK_PATH: Path = Path(os.getcwd())

    CONFIG_FILENAME: str = 'config.json'
    CONFIG_PATH: Path = WORK_PATH / CONFIG_FILENAME
    CONFIG_CODING: str = 'utf-8'

    SETTING_FILENAME: str = 'setting.json'
    INPUT_SETTING_FILENAME: str = 'input_setting.json'
    SETTING_PATH: Path = WORK_PATH / SETTING_FILENAME
    INPUT_SETTING_PATH: Path = WORK_PATH / INPUT_SETTING_FILENAME

    GET_PLAYERLIST_INTERVAL: int = 5
    GET_PLAYERLIST_RETRY_TIMES: int = 5

    IMGS_PATH: Path = WORK_PATH / 'assets/imgs'

settings = Settings()
