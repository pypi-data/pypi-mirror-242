# 导入包
import pandas as pd
import statsmodels.api as sm
from functools import reduce
from scipy import stats

# 定义 生成估计窗口和事件窗口虚拟变量 的函数
def mark_event_window(group, est_window, event_window):
    # Find the index where 'date1' changes from negative to positive
    # If there's no such change, find the closest to zero
    # transition_index是date1是0或者最小正数所在行的索引
    transition_index = group[group['date1'] >= pd.Timedelta(days=0)].index.min()
    
    # Mark 5 days before and 10 days after the transition as the event window
    event_window_indices = range(max(transition_index + event_window[0], group.index.min()), 
                                 min(transition_index + event_window[1] + 1, group.index.max() + 1))
    est_window_indices = range(max(transition_index + est_window[0], group.index.min()), 
                               min(transition_index + est_window[1], group.index.max() + 1))
    group['event_window'] = group.index.isin(event_window_indices).astype(int)
    group['est_window'] = group.index.isin(est_window_indices).astype(int)
    group.drop('stockid', axis=1, inplace= True)
    return group

def event_study(df_eventstudy = None, event_window_list = None, est_window = None):
    # 基本处理
    df_eventstudy['stockid']  = df_eventstudy['stockid'].astype(str).str.zfill(6)
    df_eventstudy['date1'] = df_eventstudy['date'] - df_eventstudy['eventdate']

    # Sort the data by 'stockid' and 'date'
    df_eventstudy1 = df_eventstudy.sort_values(by=['stockid', 'date'], ascending=True).reset_index().drop(['index'],axis=1)

    # Filter the dataframe to keep only the rows where date1 is between -365 and 0 (inclusive)
    filtered_df = df_eventstudy1[(df_eventstudy1['date1'] >= pd.Timedelta(days=-365)) & (df_eventstudy1['date1'] <= pd.Timedelta(days=0))]

    # Group by stockid and count the number of rows for each stockid
    stock_counts = filtered_df.groupby('stockid').size()

    # Identify the stocks with less than 240 data points
    stocks_to_remove = stock_counts[stock_counts < 240].index

    # Remove these stocks from the original dataframe
    df_eventstudy2 = df_eventstudy1[~df_eventstudy1['stockid'].isin(stocks_to_remove)]

    df_eventstudy3 = df_eventstudy2[(df_eventstudy2['date1'] >= pd.Timedelta(days=-365)) & (df_eventstudy2['date1'] <= pd.Timedelta(days=365))]

    # Displaying a summary of the operation
    remove_summary = {
        "Total Stocks in Original Data": df_eventstudy1['stockid'].nunique(),
        "Stocks with Insufficient Data": len(stocks_to_remove),
        "Total Stocks in Cleaned Data": df_eventstudy3['stockid'].nunique()
    }

    print(remove_summary)

    # Sort the data by 'stockid' and 'date'
    df_eventstudy4 = df_eventstudy3.sort_values(by=['stockid', 'date'], ascending=True).reset_index().drop(['index'],axis=1)

    merge_car_list = []
    for event_window in event_window_list:
        # Apply the function to each group of 'stockid'
        df_eventstudy5 = df_eventstudy4.groupby('stockid').apply(lambda group: mark_event_window(group, est_window, event_window))
        df_eventstudy6 = df_eventstudy5.reset_index().drop(['level_1'],axis=1)
        # Display the first few rows of the updated dataframe to verify the changes
        # df_eventstudy6

        # 去除事件窗口天数不够的股票数据
        stock_list = list(df_eventstudy6['stockid'].unique())
        remove_list = []
        len_event_window = event_window[1] - event_window[0]
        for id in stock_list:
            if len(df_eventstudy6[(df_eventstudy6['event_window'] == 1) & (df_eventstudy6['stockid'] == id)]) < len_event_window:
                remove_list.append(id)
                stock_list.remove(id)
        # 删除stockid为这些特定值的行
        df_eventstudy7 = df_eventstudy6[~df_eventstudy6['stockid'].isin(remove_list)]
        df_eventstudy8 = df_eventstudy7.sort_values(by=['stockid', 'date'], ascending=True).reset_index().drop(['index'],axis=1)

        for id in stock_list:
            # 利用估计窗口数据拟合模型
            condition3 = (
            (df_eventstudy8['est_window'] == 1) &
            (df_eventstudy8['stockid'] == id)
            )

            X = sm.add_constant(df_eventstudy8.loc[condition3, 'mreturn'], has_constant='add')  # 假设mreturn是自变量
            y = df_eventstudy8.loc[condition3, 'sreturn']  # 假设sreturn是因变量
            model = sm.OLS(y, X).fit()

            condition4 = (
            (df_eventstudy8['event_window'] == 1) &
            (df_eventstudy8['stockid'] == id)
            )

            # 在事件窗口生成预测值
            X_predict = sm.add_constant(df_eventstudy8.loc[condition4, 'mreturn'], has_constant='add')
            df_eventstudy8.loc[condition4, 'predicted'] = model.predict(X_predict)
                                                 
        df_eventstudy8['AR'] = df_eventstudy8['sreturn'] - df_eventstudy8['predicted']
        df_eventstudy9 = df_eventstudy8.sort_values(['stockid', 'date'], ascending = True)
        # 按股票ID分组，并计算每个股票每天的累积异常收益
        df_eventstudy9['CAR'] = df_eventstudy9.groupby('stockid')['AR'].cumsum()
        df_eventstudy10 = df_eventstudy9.dropna(subset=['CAR'])
        df_eventstudy11 = df_eventstudy10.sort_values(['stockid', 'date'], ascending = True)
        df_eventstudy12 = df_eventstudy11.drop_duplicates(subset=['stockid'], keep='last')
        df_eventstudy13 = df_eventstudy12.reindex(columns=['stockid','CAR'])
        df_eventstudy14 = df_eventstudy13.rename(columns={'CAR':f'CAR[{event_window[0]},{event_window[1]}]'})

        merge_car_list.append(df_eventstudy14)

    # 使用reduce()合并这些DataFrame
    merged_CARs = reduce(lambda x, y: pd.merge(x, y, on = ['stockid'], how = 'inner'), merge_car_list)
    # merged_CARs

    # 对每个CAR列进行T检验
    t_test_results = {}
    # 使用列表推导来获取所有以'CAR'开头的列名
    car_columns = [col for col in merged_CARs.columns if 'CAR' in col]

    for col in car_columns:
        Mean_CAR = merged_CARs[col].mean()
        t_stat, p_value = stats.ttest_1samp(merged_CARs[col].dropna(), 0)  # 删除NaN值
        t_test_results[col] = {'Mean CAR': Mean_CAR, 't_stat': t_stat, 'p_value': p_value}

    # 将T检验结果转换为DataFrame
    t_test_df = pd.DataFrame(t_test_results).T  # 转置以使每个时间窗口成为一行
    t_test_df.reset_index(inplace=True)
    t_test_df.rename(columns={'index': 'Time Window'}, inplace=True)
    # t_test_df

    t_test_df.to_excel('t_test.xlsx',index=False)
    merged_CARs.to_excel('tem.xlsx',index=False)
    return t_test_df