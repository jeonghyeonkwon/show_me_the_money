class NaverResponse:
    def __init__(self, title, originalLink, link, description, pubDate):
        self.title = title
        self.originalLink = originalLink
        self.link = link
        self.description = description
        self.pubDate = pubDate

    def toTemplate(self):
        return """
                    ===========================
                    제목 : {}
                    내용 : {}
                    날짜 : {}
                    ---------------------------
                    내용 : {}
                    ===========================
                """.format(
            self.title, self.description, self.pubDate, self.description
        )
