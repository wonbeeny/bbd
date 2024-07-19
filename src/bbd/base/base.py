# coding : utf-8
# author : WONBEEN

import os

from abc import *
from typing import Any, Callable

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ..utils import get_logger

logger = get_logger(__name__)

class Attrs(metaclass=ABCMeta):
    """
    기본 속성값을 필요로 하는 클래스의 부모 클래스
    """
    
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def set(self):
        pass

    def _check_record_text(self, user_text):
        """
        [TODO] if we need more checking, then we will develop more.
        """
        try:
            components = [item.strip() for item in user_text.split('/')]
            if len(components) < 2:
                message = f"Please check `{user_text}`. user_text must have `/` at least one."
                logger.error(message)    # text 입력시 반드시 / 가 2개 이상 (google sheet 등록 및 지출 내역 등록 시 / 는 1개 이상이어야 됨)
                raise ValueError(message)
            else:
                pass    # 정상적인 text 입력 형태
        except Exception as e:
            message = f"Please check `{user_text}`. user_text must not be None."
            logger.error(message)    # text 를 입력하지 않았을 때
            raise e
    
    def _check_exist_text(self, user_text):
        if user_text is None:
            message = f"Please check `{user_text}`. user_text must not be None."
            logger.error(message)    # text 를 입력하지 않았을 때
            raise e
            
        
    @abstractmethod
    def run(self):
        pass
    
    def do(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    __call__ : Callable[..., Any] = do


    
class BasePreProcessor(Attrs):
    """
    각 task에 맞게 정의하는 `PreProcessor` 클래스의 base class.
    """
    def __init__(self, user_text=None, task=None):
        """
        Args:
            user_text (:obj:`str`):
                고객이 요청한 text 에 / 가 2개 이상 있는지 체크
        """
        self.user_text = user_text
        self.set(task)

    def set(self, task):
        if task == "record":
            self._check_record_text(self.user_text)
        if task == "check":
            self._check_exist_text(self.user_text)
        else:
            message = f"Please check `task`. Your task is not exist."
            logger.error(message)    # text 를 입력하지 않았을 때

    def run(self):
        raise NotImplementedError("`run` method must be customized by task.")


class BasePostProcessor(Attrs):
    """
    각 task에 맞게 정의하는 `PostProcessor` 클래스의 base class.
    
    Args:
        json_key_path (:obj: `str`):
            고객의 API Key 경로
        sheet_url (:obj:`str`):
            고객의 스프레드시트 url
    """
    def __init__(self, json_key_path, sheet_url):
        self.sheet = self.set(json_key_path, sheet_url)

    def set(self, json_key_path, sheet_url):
        # 구글 인증
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
            client = gspread.authorize(creds)
        except Exception as e:
            message = "Invalid Google Auth."
            logger.error(message)
            raise e

        # 스프레드시트 오픈
        try:
            sheet = client.open_by_url(sheet_url)
        except Exception as e:
            message = "Invalid open spread sheet."
            logger.error(message)
            raise e
        return sheet

    def run(self):
        raise NotImplementedError("`run` method must be customized by task.")