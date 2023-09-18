class NewCoinResponse:
    def __init__(self, market, korean_name, english_name, coin_type):
        self.market = market
        self.korean_name = korean_name
        self.english_name = english_name
        self.coin_type = coin_type

    def toTemplate(self):
        return """
            신규 코인 발행
            market : {}
            코인 타입 : {}
            한국명 : {}
            영어명 : {}
            """.format(
            self.market, self.coin_type, self.korean_name, self.english_name
        )
