# -*- coding: UTF-8 -*-
import json
import os
import pathlib
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie

file_path = pathlib.Path(__file__).parent
template_path = os.path.join(os.path.dirname(__file__), 'template')
config_tmp_path = os.path.join(template_path, 'template.html')


class TestReport(object):
    def __init__(self, fields, bar_data, pie_data):
        """

        :param fields: 汇总参数, dict
        :param report_dir: 报告地址
        :param filename: 报告名称
        :param bar_data: 柱状图参数, list: [运行总数, 失败数， 平均排名]
        :param pie_data: 环形图参数, list: [通过数, 未通过数]
        """
        self.fields = fields
        self.report_dir = file_path.parent / 'result'
        self.filename = 'test_report.html'
        self.bar_data = bar_data
        self.pie_data = pie_data

    def output_report(self):
        # 生成柱状图
        self.bar_datazoom_slider()
        self.pie_position()

        def render_template(params: dict, template: str):
            for name, value in params.items():
                name = '${' + name + '}'
                template = template.replace(name, value)
            return template

        template_path2 = config_tmp_path
        with open(os.path.join(template_path, 'theme_default' + '.json'), 'r') as theme:
            render_params = {
                **json.load(theme),
                'resultData': json.dumps(self.fields, ensure_ascii=False, indent=4)
            }

        override_path = os.path.abspath(self.report_dir) if \
            os.path.abspath(self.report_dir).endswith('/') else \
            os.path.abspath(self.report_dir) + '/'

        with open(template_path2, 'rb') as file:
            body = file.read().decode('utf-8')
        with open(override_path + self.filename, 'w', encoding='utf-8', newline='\n') as write_file:
            html = render_template(render_params, body)
            write_file.write(html)

    def bar_datazoom_slider(self):
        bar = (
            Bar(init_opts=opts.InitOpts(width="600px", height="300px"))
            .add_xaxis(["运行", "失败", "平均排名"])
            .add_yaxis("", self.bar_data)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="局数统计"),
                brush_opts=opts.BrushOpts(),
            )
        )
        bar.render(f"{self.report_dir}/bar.html")

    def pie_doughnut_chart(self):
        x_data = ["通过", "未通过"]
        y_data = self.pie_data
        c = (
            Pie(init_opts=opts.InitOpts(width="600px", height="300px"))
            .add(
                series_name="截图检测",
                data_pair=[list(z) for z in zip(x_data, y_data)],
                radius=["40%", "55%"],
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c} {per|{d}%}",
                    background_color="#eee",
                    border_color="#aaa",
                    border_width=1,
                    border_radius=4,
                    rich={
                        "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                        "abg": {
                            "backgroundColor": "#e3e3e3",
                            "width": "100%",
                            "align": "right",
                            "height": 22,
                            "borderRadius": [4, 4, 0, 0],
                            },
                        "hr": {
                            "borderColor": "#aaa",
                            "width": "100%",
                            "borderWidth": 0.5,
                            "height": 0,
                        },
                        "b": {"fontSize": 16, "lineHeight": 33},
                        "per": {
                            "color": "#eee",
                            "backgroundColor": "#334455",
                            "padding": [2, 4],
                            "borderRadius": 2,
                        },
                    },
                ),
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="图像识别结果"))
        )
        c.render(f"{self.report_dir}/pie.html")

    def pie_position(self):
        x_data = ["通过", "未通过"]
        y_data = self.pie_data
        data_pair = [list(z) for z in zip(x_data, y_data)]
        data_pair.sort(key=lambda x: x[1])
        c = (
            Pie(init_opts=opts.InitOpts(width="750px", height="350px"))
            .add(
                series_name="检测结果",
                data_pair=data_pair,
                center=["50%", "50%"],
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="图像识别结果",
                    pos_left="left"
                ),
                legend_opts=opts.LegendOpts(pos_left="center"),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        c.render(f"{self.report_dir}/pie.html")


if __name__ == '__main__':
    result_data = {
            "testPass": 100,
            "testName": "局内战斗自动化测试",
            "testAPK": "release_09152352_google_5633.apk",
            "testAll": 200,
            "testFail": 50,
            "beginTime": "2020-09-16 11:02",
            "totalTime": "3589s",
            "errorVideo": ["1.mp4", "2.mp4"]
        }
    result_dir = file_path.parent / 'result'

    TestReport(result_data, [200, 50, 5], [1485, 125]).output_report()
