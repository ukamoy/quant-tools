from pyecharts.charts import Kline, Line, Grid, Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
init_chart = {}
class Chart:
    def __init__(self, chart_opt):
        self.chart_opt = chart_opt
        self.xaxis = []

    def set_xaxis(self, series):
        self.xaxis = series
    
    def candle(self, data, label="", xaxis=None, zoom_setting=[], position=0, show_rgb=False, mark_point=[], mark_line=[]):
        zoomopt = []
        for setting in zoom_setting:
            zoomopt.append(
                opts.DataZoomOpts(**setting)
            )

        if not xaxis: xaxis = self.xaxis
        rgb_color = {
            "itemstyle_opts": opts.ItemStyleOpts(
                color="#ef232a",
                color0="#14b143",
                border_color="#ef232a",
                border_color0="#14b143",
            ),
        }
        if not show_rgb: rgb_color = {}
        mark_point_item = []
        for point in mark_point:
            mark_point_item.append(
                opts.MarkPointItem(**point),
            )
        return (Kline(init_opts=opts.InitOpts(**self.chart_opt))
            .add_xaxis(xaxis_data=xaxis)
            .add_yaxis(
                series_name=label,
                y_axis=data,
                markpoint_opts=opts.MarkPointOpts(data=mark_point_item),
                markline_opts=opts.MarkLineOpts(
                    label_opts=opts.LabelOpts(
                        position="middle", color="blue", font_size=15
                    ),
                    data=mark_line,
                    symbol=["circle", "none"],
                ),
                **rgb_color
            )
            .set_series_opts(
                markarea_opts=opts.MarkAreaOpts(is_silent=True, data=[])
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Candle Chart", pos_left="0"),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    grid_index=position,
                    is_scale=True,
                    boundary_gap=False,
                    axislabel_opts=opts.LabelOpts(is_show=True),
                ),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                datazoom_opts=zoomopt,
            )
        )

    def line(self, data, xaxis=None, position=0):
        if not xaxis: xaxis = self.xaxis
        line = Line(init_opts=opts.InitOpts(**self.chart_opt)).add_xaxis(xaxis_data=xaxis)
        for d in data:
            line.add_yaxis(
                    series_name=d["label"],
                    y_axis=d["data"],
                    is_smooth=True,
                    is_selected=True,
                    is_symbol_show=False,
                    linestyle_opts=opts.LineStyleOpts(opacity=1),
                    label_opts=opts.LabelOpts(is_show=False),
                )
        line.set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=position,
                is_scale=True,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
        )
        return line

    def bar(self, data, label="", xaxis=None, position=0, show_rgb=False):
        if not xaxis: xaxis = self.xaxis
        rgb_color = {
            "itemstyle_opts": opts.ItemStyleOpts(color=JsCode(
                """
                function(params) {
                    var colorList;
                    if (params.data >= 0) { colorList = '#ef232a'; } else { colorList = '#14b143'; }
                    return colorList;
                }
                """
                )
            )
        }
        if not show_rgb: rgb_color = {}
        return (Bar()
                .add_xaxis(xaxis_data=xaxis)
                .add_yaxis(
                    series_name=label,
                    y_axis=data,
                    label_opts=opts.LabelOpts(is_show=False),
                    **rgb_color
                )
                .set_global_opts(
                    xaxis_opts=opts.AxisOpts(
                        type_="category",
                        grid_index=position,
                        axislabel_opts=opts.LabelOpts(is_show=False),
                    ),
                    legend_opts=opts.LegendOpts(is_show=False),
                )
            )

    def grid(self, data=[]):
        grid = Grid(init_opts=opts.InitOpts(**self.chart_opt))
        for d in data:
            grid.add(
                d["chart"],
                grid_opts=opts.GridOpts(**d["setting"]),
            )
        return grid
