from .naver import NaverAPI
from .kakao import KakaoAPI
from .tmap import TmapAPI

class Mappy:
    def __init__(self):
        self.naver = NaverAPI()
        self.kakao = KakaoAPI()
        self.tmap = TmapAPI()