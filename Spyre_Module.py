# Spyre module

from VHI_Index_Code import get_df, main_folder
from matplotlib import pyplot as plt
from spyre import server


class Visualisaton(server.App):
    title = "VHI Index"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Index',
            "options":
                [
                    {"label": "VCI", "value": "VCI"},
                    {"label": "TCI", "value": "TCI"},
                    {"label": "VHI", "value": "VHI"}
                ],
            "key": 'ticker_index',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'ProvinceID',
            "options":
                [
                    {"label": "1. Cherkasy", "value": 1},
                    {"label": "2. Chernihiv", "value": 2},
                    {"label": "3. Chernivtsi", "value": 3},
                    {"label": "4. Crimea", "value": 4},
                    {"label": "5. Dnipropetrovs'k", "value": 5},
                    {"label": "6. Donets'k", "value": 6},
                    {"label": "7. Ivano-Frankivs'k", "value": 7},
                    {"label": "8. Kharkiv", "value": 8},
                    {"label": "9. Kherson", "value": 9},
                    {"label": "10. Khmel'nyts'kyy", "value": 10},
                    {"label": "11. Kiev", "value": 11},
                    {"label": "12. Kiev City", "value": 12},
                    {"label": "13. Kirovohrad", "value": 13},
                    {"label": "14. Luhans'k", "value": 14},
                    {"label": "15. L'viv", "value": 15},
                    {"label": "16. Mykolayiv", "value": 16},
                    {"label": "17. Odessa", "value": 17},
                    {"label": "18. Poltava", "value": 18},
                    {"label": "19. Rivne", "value": 19},
                    {"label": "20. Sevastopol'", "value": 20},
                    {"label": "21. Sumy", "value": 21},
                    {"label": "22. Ternopil'", "value": 22},
                    {"label": "23. Transcarpathia", "value": 23},
                    {"label": "24. Vinnytsya", "value": 24},
                    {"label": "25. Volyn", "value": 25},
                    {"label": "26. Zaporizhzhya", "value": 26},
                    {"label": "27. Zhytomyr", "value": 27}
                ],
            "key": 'ticker_province_id',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Min year',
            "key": 'min_year',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Max year',
            "key": 'max_year',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Min week',
            "key": 'min_week',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Max week',
            "key": 'max_week',
            "action_id": "update_data"
        }
    ]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Get index data"
    }]

    tabs = ["Plot1", "Plot2", "Table1", "Table2"]

    outputs = [
        {
            "type": "plot",
            "id": "plot1",
            "control_id": "update_data",
            "tab": "Plot1"},
        {
            "type": "plot",
            "id": "plot2",
            "control_id": "update_data",
            "tab": "Plot2"},
        {
            "type": "table",
            "id": "table1",
            "control_id": "update_data",
            "tab": "Table1",
            "on_page_load": True
        },
        {
            "type": "table",
            "id": "table2",
            "control_id": "update_data",
            "tab": "Table2",
            "on_page_load": True
        }
    ]

    def table1(self, params):
        index = params['ticker_index']
        province_id = int(params['ticker_province_id'])
        start_year = int(params['min_year'])
        final_year = int(params['max_year'])
        start_week = int(params['min_week'])
        final_week = int(params['max_week'])
        start_df = get_df(main_folder, province_id)
        final_df = start_df[(start_df['Year'] >= int(start_year)) & (start_df['Year'] <= int(final_year)) & (
                    start_df['Week'] >= int(start_week)) & (start_df['Week'] <= int(final_week))][
            ['Year', 'Week', index]]
        return final_df

    def table2(self, params):
        province_id = int(params['ticker_province_id'])
        start_df = get_df(main_folder, province_id)
        new_df = start_df.groupby(['Week']).mean()
        new_df['Week'] = new_df.index
        return new_df[['Week', 'VHI']]

    def plot1(self, params):

        plt.style.use('ggplot')

        df = self.table1(params)
        df = df[params['ticker_index']]
        plt_obj = df.plot(ylim=[0, 100], kind='line')
        if int(params['min_year']) == int(params['max_year']):
            plt_obj.set_title('{} for {} year'.format(params['ticker_index'], params['min_year']))
        else:
            plt_obj.set_title(
                '{} for {}-{} years'.format(params['ticker_index'], params['min_year'], params['max_year']))
        plt_obj.set_xlabel('Week')
        plt_obj.set_ylabel(params['ticker_index'])

        fig = plt_obj.get_figure()
        return fig

    def plot2(self, params):
        plt.style.use('ggplot')

        df = self.table2(params)
        df = df[['VHI']]
        plt_obj = df.plot(ylim=[0, 100], kind='line')
        plt_obj.set_title('VHI mean')
        plt_obj.set_xlabel('Week')
        plt_obj.set_ylabel('VHI')

        fig = plt_obj.get_figure()
        return fig

app = Visualisaton()
app.launch(port=8080)
