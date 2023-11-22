# EventStudy Package

## 简介
EventStudy 是一个用于进行金融事件研究分析的 Python 包。目前仅提供了基于市场模型的事件研究。

## 安装
通过 pip 安装 EventStudy：
```bash
pip install myeventstudy
```
## 快速开始
```bash
import myeventstudy.event_analysis as es

# 示例数据
df_eventstudy = pd.read_...

# 设置事件窗口和估计窗口
event_window_list = [(-20, -11), (-10, -6), (-5, 10), (11, 20), (21, 60)]
est_window = (-120,-20)

# 进行事件研究分析
result = es.event_study(df_eventstudy = df_eventstudy, event_window_list = event_window_list, est_window = est_window)
```

## 功能概述
EventStudy 包包含以下主要功能：

- mark_event_window：标记事件窗口和估计窗口。
- event_study：执行事件研究方法，包括统计检验和结果汇总。