from base import BaseControl
shibor_url = "http://www.shibor.org/shibor/web/html/shibor.html"
omo_url = "http://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125431/index.html"

class CenterBank(BaseControl):

    @classmethod
    def Shibor(cls):
        resp = cls.send_requests(shibor_url)
        rows = cls.parse_html(resp.content.decode("gb2312"), '//table[@class="shiborquxian"]/tr')
        sp_treat = {1:".//a//font//text()", 3:".//img/@src"}
        table = [cls.unpack_row(td, sp_treat=sp_treat) for td in rows]
        df = cls.DataFrame(table[:-1]).drop(0, axis=1)
        df[4] = df.apply(lambda x: f"+{x[4].strip()}" if "upicon.gif" in x[3] else f"-{x[4].strip()}", axis=1)
        df = df.drop(3, axis=1)
        df.columns = ["Period","Shibor","Trend(BP)"]
        update_dt = cls.parse_html(resp.content.decode("gb2312"), '//td[@class="infoTitleW"]//text()')
        return "".join(update_dt).strip(), df

    @classmethod
    def OpenMarketOperations(cls):
        resp = cls.getJSPage(omo_url)
        links = cls.parse_html(resp.content.decode("utf-8"), '//td[@class="unline"]//a/@href')
        titles = cls.parse_html(resp.content.decode("utf-8"), '//td[@class="unline"]//a/@title')
        dates = cls.parse_html(resp.content.decode("utf-8"), '//td[@class="unline"]//span/text()')
        today_date = cls.current().strftime("%Y-%m-%d")
        to_link = ""
        for link, title, date in zip(links, titles, dates):
            if "公开市场业务交易公告" in title and date == today_date:
                to_link = link

        operation = ""
        if to_link:
            new_url = cls.parse_new_url(omo_url, to_link)
            info_page = cls.getJSPage(new_url)
            content = cls.parse_html(info_page.content.decode("utf-8"), '//div[@id="zoom"]/p/text()')
            table = cls.parse_html(info_page.content.decode("utf-8"), '//div[@id="zoom"]/table/tbody/tr')
            detail = [cls.unpack_row(row, tag=".//td/p/span/span/span") for row in table]
            if detail:
                operation = f"{content[0]}\n\n{detail[0][0]}:{detail[1][0]}天\n{detail[0][1]}:{detail[1][1]}亿元\n{detail[0][2]}:{detail[1][2]}"
        return operation



print(CenterBank.OpenMarketOperations())