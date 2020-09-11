from base import BaseControl
shibor_url = "http://www.shibor.org/shibor/web/html/shibor.html"

class Shibor(BaseControl):
    @classmethod
    def read_data(cls):
        resp = cls.send_requests(shibor_url)
        rows = cls.parse_html(resp.content.decode("gb2312"), f'//table[@class="shiborquxian"]/tr')
        sp_treat = {1:".//a//font//text()", 3:".//img/@src"}
        table = [cls.unpack_row(td, sp_treat=sp_treat) for td in rows]
        df = cls.DataFrame(table[:-1]).drop(0, axis=1)
        df.columns = ["Period","Shibor","Side","Trend(BP)"]
        df["Trend(BP)"] = df.apply(lambda x: float(x["Trend(BP)"]) if "upicon.gif" in x["Side"] else -float(x["Trend(BP)"]), axis=1)
        df = df.drop("Side", axis=1)
        return df

df = Shibor.read_data()
print(df)