# See also: ð [Channels - Consumers](https://channels.readthedocs.io/en/latest/topics/consumers.html)
from django.conf.urls import url

# Websockç·´ç¿ï¼
from webapp1.websocks.websock_practice1.v1.consumer import WebsockPractice1V1Consumer
#    ------- ----------------------------- --------        --------------------------
#    1       2                             3               4
# 1. ã¢ããªã±ã¼ã·ã§ã³ ãã©ã«ãã¼å
# 2. ãã£ã¬ã¯ããªã¼å
# 3. Python ãã¡ã¤ã«åãæ¡å¼µå­æã
# 4. ã¯ã©ã¹å

# Websockç·´ç¿ï¼
from webapp1.websocks.websock_practice2.v1.consumer import WebsockPractice2V1Consumer
#                                     ^                                   ^
#    ------- ----------------------------- --------        --------------------------
#    1       2                             3               4
# 1. ã¢ããªã±ã¼ã·ã§ã³ ãã©ã«ãã¼å
# 2. ãã£ã¬ã¯ããªã¼å
# 3. Python ãã¡ã¤ã«åãæ¡å¼µå­æã
# 4. ã¯ã©ã¹å

# ãÃã²ã¼ã ã®ç·´ç¿ï¼
from webapp1.websocks.tic_tac_toe.v2.consumer_custom import TicTacToeV2ConsumerCustom
#                                  ^ two                              ^ two
#    ------- ----------------------- ---------------        -------------------------
#    1       2                       3                      4
# 1. ã¢ããªã±ã¼ã·ã§ã³ ãã©ã«ãã¼å
# 2. ãã£ã¬ã¯ããªã¼å
# 3. Python ãã¡ã¤ã«åãæ¡å¼µå­æã
# 4. ã¯ã©ã¹å

# ãÃã²ã¼ã ã®ç·´ç¿ï¼ï¼ï¼
from webapp1.websocks.tic_tac_toe.v3o1.consumer_custom import TicTacToeV3o1ConsumerCustom
#                                  ^^^ three o one                      ^^^ three o one
#    ------- ------------------------- ---------------        ---------------------------
#    1       2                         3                      4
# 1. ã¢ããªã±ã¼ã·ã§ã³ ãã©ã«ãã¼å
# 2. ãã£ã¬ã¯ããªã¼å
# 3. Python ãã¡ã¤ã«åãæ¡å¼µå­æã
# 4. ã¯ã©ã¹å


websocket_urlpatterns = [

    # +----
    # | Websockç·´ç¿ï¼

    # Websockç·´ç¿ï¼
    url(r'^websock-practice1/v1/$', WebsockPractice1V1Consumer.as_asgi()),
    #     -----------------------   ------------------------------------
    #     1                                      2
    # 1. URLã®ãã¹ã®é¨åã®ãDjango ã§ã®æ­£è¦è¡¨ç¾ã®æ¸ãæ¹
    # 2. ã¯ã©ã¹åã¨ã¡ã½ããã URL ã ASGIå½¢å¼ã«ãã

    # | Websockç·´ç¿ï¼
    # +----




    # +----
    # | Websockç·´ç¿ï¼

    # Websockç·´ç¿ï¼
    url(r'^websock-practice2/v1/$', WebsockPractice2V1Consumer.as_asgi()),
    #                      ^                       ^
    #     -----------------------   ------------------------------------
    #     1                                      2
    # 1. URLã®ãã¹ã®é¨åã®ãDjango ã§ã®æ­£è¦è¡¨ç¾ã®æ¸ãæ¹
    # 2. ã¯ã©ã¹åã¨ã¡ã½ããã URL ã ASGIå½¢å¼ã«ãã

    # | Websockç·´ç¿ï¼
    # +----




    # ãÃã²ã¼ã ã®ç·´ç¿ï¼
    url(r'^tic-tac-toe/v2/playing/(?P<kw_room_name>\w+)/$',
        #               ^
        # -----------------------------------------------
        # 1
        TicTacToeV2ConsumerCustom.as_asgi()),
    #             ^
    #   -----------------------------------
    #   2
    # 1. ä¾ãã° `http://example.com/tic-tac-toe/v2/playing/Elephant/` ã®ãããªURLã®ãã¹ã®é¨åã®ãDjango ã§ã®æ­£è¦è¡¨ç¾ã®æ¸ãæ¹ã
    #    kw_room_name ã¯å¤æ°ã¨ãã¦æ¸¡ããã
    # 2. ã¯ã©ã¹åã¨ã¡ã½ããã URL ã ASGIå½¢å¼ã«ãã

    # ãÃã²ã¼ã ã®ç·´ç¿ï¼ï¼ï¼
    url(r'^tic-tac-toe/v3o1/playing/(?P<kw_room_name>\w+)/$',
        #               ^^^ three o one
        # -------------------------------------------------
        # 1
        TicTacToeV3o1ConsumerCustom.as_asgi()),
    #             ^^^ three o one
    #   -------------------------------------
    #   2
    # 1. ä¾ãã° `http://example.com/tic-tac-toe/v3o1/playing/Elephant/` ã®ãããªURLã®ãã¹ã®é¨åã®ãDjango ã§ã®æ­£è¦è¡¨ç¾ã®æ¸ãæ¹ã
    #                              -----------------------------------
    #    kw_room_name ã¯å¤æ°ã¨ãã¦æ¸¡ããã
    # 2. ã¯ã©ã¹åã¨ã¡ã½ããã URL ã ASGIå½¢å¼ã«ãã
]
