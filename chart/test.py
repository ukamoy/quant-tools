import pandas as pd
import numpy as np
from BaseChart import Chart

symbol = "000001.XSHG"
data = pd.read_csv("data.csv")

chart_setting = {"width":"1600px","height":"840px"}
zoom_setting = [
    {"is_show":False, "type_":"inside", "xaxis_index":[0, 0], "range_start":0, "range_end":100},
    {"is_show":True, "pos_top":"97%", "xaxis_index":[0, 1], "range_start":0, "range_end":100},
    {"is_show":False, "xaxis_index":[0, 2], "range_start":0, "range_end":100},
]

chart = Chart(chart_setting)
chart.set_xaxis(data["datetime"].tolist())

candle_data = np.array(data[["open","close","low","high"]]).tolist()
candle = chart.candle(candle_data, symbol, zoom_setting=zoom_setting, mark_point=[{"type_":"max", "name":"最大值"}])

ma5 = [{"label":"MA5", "data":data['close'].rolling(5, min_periods=5).mean()}]
line_ma5 = chart.line(ma5)
candle.overlap(line_ma5)

volume_data = data["volume"].tolist()
volume = chart.bar(volume_data, "Volume", position=1)

macd_data = data["macd"].tolist()
macd = chart.bar(macd_data, "MACD", position=2, show_rgb=True)
dif_dea = [
    {"label":"dif", "data":data["dif"]},
    {"label":"dea", "data":data["dea"]}
]
line_dif_dea = chart.line(dif_dea)
macd.overlap(line_dif_dea)

grid_data = [
    {"chart": candle, "setting": {"pos_left":"5%", "pos_right":"1%", "height":"60%"}},
    {"chart": volume, "setting": {"pos_left":"5%", "pos_right":"1%", "height":"10%", "pos_top":"71%"}},
    {"chart": macd, "setting": {"pos_left":"5%", "pos_right":"1%", "height":"14%", "pos_top":"83%"}},
]
grid_chart = chart.grid(grid_data)
grid_chart.render("candle.html")