# EventStudy Package

## 简介
EventStudy 是一个用于进行金融事件研究分析的 Python 包。目前提供了基于市场模型、市场调整模型、Fama三因子模型的事件研究法。
- 市场模型 (Market Model)

    $ R_{i,t}=\alpha_i+\beta_iR_{m,t}+\epsilon_{i,t} $

- 市场调整模型 (Market-adjused Model)

    $ R_{i,t}=R_{m,t}+\epsilon_{i,t} $

- Fama三因素模型 (Fama-French Three Factor Model)

    $ R_{i,t}-R_{f,t}=\alpha_i+\beta_1[R_{m,t}-R_{f,t}]+\beta_2SMB_t+\beta_3(HML_t)+\epsilon_{i,t} $

## 安装
通过 pip 安装 EventStudy：
```bash
pip install myeventstudy
```

## 参数
| 参数名 | 描述 | 例子 |
|:------|:----|:----|
| `df_eventstudy` | 待分析数据，必须包含 `stockid`, `sreturn`, `date`, `mreturn`, `eventdate` 变量，如果使用FAMA三因子模型，还必须包含 `smb`, `hml`, `rf` 变量 | `df_eventstudy = df_eventstudy` |
| `event_window_list` | 事件窗口列表，可添加多个事件窗口 | `event_window_list = [(-20, -11), (-10, -6), (-5, 10), (11, 20), (21, 60)]` |
| `est_window` | 估计窗口，默认值为 `(-120, -20)` | `est_window = (-120, -20)` |
| `predict_model` | 估计正常收益率时所用模型，支持 `'market'`, `'fama3'`, `'market_adj'` | `predict_model = 'market'` |

## 示例数据
| stockid | sreturn   | date      | mreturn   | eventdate |
|---------|-----------|-----------|-----------|-----------|
| 2       | -.099668  | 04mar2013 | -.046133  | 15jul2022 |
| 2       | -.006454  | 24aug2017 | -.005709  | 15jul2022 |
| 2       | -.009456  | 07dec2016 | .004797   | 15jul2022 |
| 2       | .013333   | 12mar2014 | .002595   | 15jul2022 |
| 2       | -.005549  | 13may2021 | -.010224  | 15jul2022 |
| 2       | -.003764  | 29apr2014 | .011008   | 15jul2022 |
| 2       | .000911   | 09apr2013 | .006929   | 15jul2022 |

- note1：证券代码前有没有0都可以，函数内部会自动补齐
- note2：date和eventdate只要是日期格式即可


## 快速开始
```bash
import myeventstudy.event_analysis as es

# 示例数据
df_eventstudy = pd.read_...

# 设置事件窗口
event_window_list = [(-20, -11), (-10, -6), (-5, 10), (11, 20), (21, 60)]

# 进行事件研究分析
result = es.event_study(df_eventstudy = df_eventstudy, event_window_list = event_window_list, est_window = (-120,-20), predict_model = 'market')
```

## 功能概述
EventStudy 包包含以下主要功能：

- mark_event_window：标记事件窗口和估计窗口。
- event_study：执行事件研究方法，包括统计检验和结果汇总。
