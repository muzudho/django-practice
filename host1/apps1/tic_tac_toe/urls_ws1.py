# See also: ð [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url

# ãÃã²ã¼ã ã®ç·´ç¿ï¼
from apps1.tic_tac_toe.websocks.v1o1.consumer import TicTacToeV1Consumer
#    ----- ----------- ------------- --------        -------------------
#    1     2           3             4               5
#    ----------------------------------------
#    6
# 1. éçºèç¨ãã£ã¬ã¯ããªã¼ã®ä¸é¨
# 2. ã¢ããªã±ã¼ã·ã§ã³ ãã©ã«ãã¼å
# 3. ãã£ã¬ã¯ããªã¼å
# 4. Python ãã¡ã¤ã«åãæ¡å¼µå­æã
# 5. ã¯ã©ã¹å
# 6. ã¢ã¸ã¥ã¼ã«å

websocket_urlpatterns = [
    # ãÃã²ã¼ã ã®ç·´ç¿ï¼
    url(r'^tic-tac-toe/v1o1/playing/(?P<room_name>\w+)/$',
        # ----------------------------------------------
        # 1
        TicTacToeV1Consumer.as_asgi()),
    #   -----------------------------
    #   2
    # 1. ä¾ãã° `http://example.com/tic-tac-toe/v1o1/playing/Elephant/` ã®ãããªURLã®ãã¹ã®é¨åã®ãDjango ã§ã®æ­£è¦è¡¨ç¾ã®æ¸ãæ¹ã
    #    room_name ã¯å¤æ°ã¨ãã¦æ¸¡ããã
    # 2. ã¯ã©ã¹åã¨ã¡ã½ããã URL ã ASGIå½¢å¼ã«ãã
]
