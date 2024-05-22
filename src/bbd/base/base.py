# coding : utf-8
# author : WONBEEN

import os

from abc import *
from typing import Any, Callable


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
    
    def _check_id(self, user_id):
        """
        [TODO] if we need more checking, then we will develop more.
        """
        if user_id is None:
            error = f"Please check `{user_id}`. user_id must not be None."
            return error
        else:
            return None

    def _check_text(self, user_text):
        """
        [TODO] if we need more checking, then we will develop more.
        """
        try:
            components = [item.strip() for item in user_text.split('/')]
            if len(components) < 2:
                error = f"Please check `{user_text}`. user_text must have `/` at least one."
                return error    # text 입력시 반드시 / 가 2개 이상 (google sheet 등록 및 지출 내역 등록 시 / 는 1개 이상이어야 됨)
            else:
                return None    # 정상적인 text 입력 형태
        except:
            error = f"Please check `{user_text}`. user_text must not be None."
            return error    # text 를 입력하지 않았을 때
        
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
    def __init__(self, user_id=None, user_text=None):
        """
        Args:
            user_id (:obj:`str`):
                고객의 고유 번호
            user_text (:obj:`str`):
                고객이 요청한 text 에 / 가 2개 이상 있는지 체크
        """
        self.user_id = user_id
        self.user_text = user_text
        self.set()

    def set(self):
        errors = list()
        check_id = self._check_id(self.user_id)
        check_text = self._check_text(self.user_text)
        if check_id is not None:
            errors.append(check_id)
        if check_text is not None:
            errors.append(check_text)
            
        self.errors = [error for error in errors if error is not None]    # input 에 대한 검증 결과 error 가 있는지 없는지를 output 으로 내보내기 위함

    def run(self):
        raise NotImplementedError("`run` method must be customized by task.")


class BasePostProcessor(Attrs):
    """
    각 task에 맞게 정의하는 `PostProcessor` 클래스의 base class.
    
    Args:
        trial (:obj:`bool`):
            에러 없이 정상적으로 동작하고 있는지 체크
        errors (:obj:`List[str]`):
            에러 발생 시 에러 메세지 확인을 위함
    """
    def __init__(self, trial=None, errors=None):
        self.trial = trial
        self.errors = errors
        self.set()

    def set(self):
        if self.trial and self.errors != list():    # error message 가 있는데 trial 이 True 임
            self.trial = False
            self.errors.append(f"self.trial is True but self.errors exists.")
        

    def run(self):
        raise NotImplementedError("`run` method must be customized by task.")