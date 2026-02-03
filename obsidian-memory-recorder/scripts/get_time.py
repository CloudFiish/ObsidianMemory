import datetime
import json
import sys

def get_current_time():
    """
    获取当前时间并以 JSON 格式输出
    """
    now = datetime.datetime.now()
    
    time_data = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "datetime": now.strftime("%Y-%m-%d %H:%M"),
        "timestamp": int(now.timestamp())
    }
    
    # 直接打印 JSON 字符串到标准输出，供 Agent 解析
    print(json.dumps(time_data, ensure_ascii=False))

if __name__ == "__main__":
    get_current_time()
