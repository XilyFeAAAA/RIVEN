#! /usr/bin/env python
# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         __init__.py.py
# Author:       Xilyfe
# Date:         2023/6/11
# Description:  
# -------------------------------------------------------------------------------
from fastapi import APIRouter

from api.api_v1.endpoints import ws_api, common_api

api_router = APIRouter()
api_router.include_router(common_api.router)
api_router.include_router(ws_api.router)
