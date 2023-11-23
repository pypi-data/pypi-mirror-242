# 导入包
import pandas as pd
import statsmodels.api as sm
from functools import reduce
from scipy import stats
import os

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

def event_study(df_eventstudy = None, event_window_list = None, est_window = (-210,-10), predict_model = 'market', save_path = None):
    # 检查参数有效性
    # 检查 df_eventstudy
    if df_eventstudy is None:
        raise ValueError("df_eventstudy cannot be None")

    # 去除缺失值
    df_eventstudy = df_eventstudy.dropna()
    
    # 尝试将 'date' 和 'eventdate' 列转换为日期格式
    try:
        df_eventstudy['date'] = pd.to_datetime(df_eventstudy['date'])
        df_eventstudy['eventdate'] = pd.to_datetime(df_eventstudy['eventdate'])
    except ValueError as e:
        raise ValueError("Conversion to datetime failed. Please ensure 'date' and 'eventdate' columns are in a proper date format.") from e

    if predict_model == 'fama3':
        required_columns = ['smb', 'hml', 'rf']
        if not all(column in df_eventstudy.columns for column in required_columns):
            raise ValueError("For 'fama3' model, df_eventstudy must contain columns: " + ', '.join(required_columns))

    # 检查 event_window_list
    if not isinstance(event_window_list, (list, tuple)) or not all(isinstance(window, (list, tuple)) for window in event_window_list):
        raise ValueError("event_window_list must be a list of lists or tuples")

    # 检查 est_window
    if not isinstance(est_window, (list, tuple)) or len(est_window) != 2:
        raise ValueError("est_window must be a tuple or list of two elements")
    
    # 检查 predict_model
    if predict_model not in ['market', 'market_adj', 'fama3']:
        raise ValueError("Invalid predict_model. Please choose 'market', 'market_adj', or 'fama3'.")
    
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

        if predict_model == 'market':
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
        
        if predict_model == 'fama3':
            for id in stock_list:
                # 利用估计窗口数据拟合模型
                condition_est = (
                    (df_eventstudy8['est_window'] == 1) &
                    (df_eventstudy8['stockid'] == id)
                )

                # 计算超额收益
                df_eventstudy8['excess_return'] = df_eventstudy8['sreturn'] - df_eventstudy8['rf']
                df_eventstudy8['market_excess'] = df_eventstudy8['mreturn'] - df_eventstudy8['rf']

                X = sm.add_constant(df_eventstudy8.loc[condition_est, ['market_excess', 'smb', 'hml']], has_constant='add')
                y = df_eventstudy8.loc[condition_est, 'excess_return']
                model = sm.OLS(y, X).fit()

                # 在事件窗口生成预测值
                condition_event = (
                    (df_eventstudy8['event_window'] == 1) &
                    (df_eventstudy8['stockid'] == id)
                )

                X_predict = sm.add_constant(df_eventstudy8.loc[condition_event, ['market_excess', 'smb', 'hml']], has_constant='add')  # 添加常数项
                df_eventstudy8.loc[condition_event, 'predicted'] = model.predict(X_predict)
        if (predict_model == 'market') or (predict_model == 'fama3'):
            df_eventstudy8['AR'] = df_eventstudy8['sreturn'] - df_eventstudy8['predicted']
        if predict_model == 'market_adj':
            df_eventstudy8['AR'] = df_eventstudy8['sreturn'] - df_eventstudy8['mreturn']
        
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

    # 如果用户没有提供save_path，使用当前工作目录作为默认保存路径
    if save_path is None:
        save_path = os.getcwd()

    # 初始文件名
    file_name = f'{predict_model}_ttest.xlsx'
    file_path = os.path.join(save_path, file_name)

    # 如果文件已经存在，找到一个新的文件名
    counter = 0
    while os.path.isfile(file_path):
        counter += 1
        # 添加一个数字标识（1, 2, 3, ...）到文件名中
        file_name = f'{predict_model}_ttest_{counter}.xlsx'
        file_path = os.path.join(save_path, file_name)

    # 将DataFrame保存到指定的Excel文件
    t_test_df.to_excel(file_path, index=False)

    # 创建消息以确认文件已经保存
    message = f"The file has been saved to: {file_path}"
    print(message)

    return t_test_df