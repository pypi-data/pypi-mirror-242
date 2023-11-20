import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from src.pyneople.functions import get_request
def test_get_request():
    get_request("https://api.neople.co.kr/df/servers?apikey=bNmjPRpeJ5q45xgJ5R46RLT6apqEa70h")

