import unittest
import os
import pandas as pd
from commodplot import commodplot
from commodutil import forwards
import plotly.graph_objects as go


class TestCommodplot(unittest.TestCase):

    def test_seas_line_plot(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(os.path.join(dirname, 'test_cl.csv'), index_col=0, parse_dates=True, dayfirst=True)
        cl = cl.dropna(how='all', axis=1)
        fwd = pd.DataFrame([50 for x in range(12)], index=pd.date_range('2021-01-01', periods=12, freq='MS'))

        res = commodplot.seas_line_plot(cl[cl.columns[-1]], fwd=fwd, shaded_range=5)
        self.assertTrue(isinstance(res, go.Figure))

        shaded_range_max = [x for x in res.data if x['name'] == '5yr Max']
        self.assertEqual(len(shaded_range_max), 1)
        shaded_range_min = [x for x in res.data if x['name'] == '5yr Min']
        self.assertEqual(len(shaded_range_min), 1)

        solid_line = [x for x in res.data if x['name'] == '2020']
        self.assertEqual(solid_line[0].hoverinfo, 'y')

        dot_line = [x for x in res.data if x['name'] == '2021']
        self.assertEqual(dot_line[0].line.dash, 'dot')

    def test_seas_line_subplot(self):
        dr = pd.date_range(start='2015', end='2020-12-31', freq='B')
        data = {'A': [10 for x in dr], 'B': [20 for x in dr], 'C': [30 for x in dr], 'D': [10 for x in dr]}
        df = pd.DataFrame(data, index=dr)
        dr = pd.date_range('2021-01-01', periods=12, freq='MS')
        data = {'A': [10 for x in dr], 'B': [20 for x in dr], 'C': [30 for x in dr], 'D': [10 for x in dr]}
        fwd = pd.DataFrame(data, index=dr)

        res = commodplot.seas_line_subplot(2, 2, df, fwd=fwd, subplot_titles=['1', '2', '3', '4'], shaded_range=5)
        self.assertTrue(isinstance(res, go.Figure))
        self.assertEqual(4, [x.name for x in res.data].count('2020'))

    def test_reindex_year_line_plot(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(os.path.join(dirname, 'test_cl.csv'), index_col=0, parse_dates=True, dayfirst=True)
        cl = cl.dropna(how='all', axis=1)
        cl = cl.rename(columns={x: pd.to_datetime(forwards.convert_contract_to_date(x)) for x in cl.columns})

        sp = forwards.time_spreads(cl, 12, 12)

        res = commodplot.reindex_year_line_plot(sp)
        self.assertTrue(isinstance(res, go.Figure))

    def test_reindex_year_line_subplot(self):
        dr = pd.date_range(start='2015', end='2020-12-31', freq='B')
        data = {'Q1 2019': [10 for x in dr], 2020: [20 for x in dr], 2021: [30 for x in dr], 2022: [10 for x in dr]}
        df = pd.DataFrame(data, index=dr)
        dfs = [df for x in range(1,5)]

        res = commodplot.reindex_year_line_subplot(2, 2, dfs, subplot_titles=['1', '2', '3', '4'])
        self.assertTrue(isinstance(res, go.Figure))

    def test_seas_box_plot(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(os.path.join(dirname, 'test_cl.csv'), index_col=0, parse_dates=True, dayfirst=True)
        cl = cl.dropna(how='all', axis=1)
        fwd = cl[cl.columns[-1]].resample('MS').mean()

        res = commodplot.seas_box_plot(cl[cl.columns[-1]], fwd)
        self.assertTrue(isinstance(res, go.Figure))

    def test_table_plot(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(os.path.join(dirname, 'test_cl.csv'), index_col=0, parse_dates=True, dayfirst=True)
        cl = cl.dropna(how='all', axis=1)

        res = commodplot.table_plot(cl, formatted_cols=['CL_2020F'])
        self.assertTrue(isinstance(res, go.Figure))

    def test_seas_table(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(os.path.join(dirname, 'test_cl.csv'), index_col=0, parse_dates=True, dayfirst=True)
        cl = cl.dropna(how='all', axis=1)
        fwd = cl[cl.columns[-1]].resample('MS').mean()

        res = commodplot.seas_table_plot(cl[cl.columns[-1]], fwd)
        self.assertTrue(isinstance(res, go.Figure))

    def test_diff_plot(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        cl = pd.read_csv(os.path.join(dirname, 'test_cl.csv'), index_col=0, parse_dates=True, dayfirst=True)
        cl = cl.dropna(how='all', axis=1)[['CL_2020F', 'CL_2020G']]

        res = commodplot.diff_plot(cl, title='Test')
        self.assertTrue(isinstance(res, go.Figure))


if __name__ == '__main__':
    unittest.main()


