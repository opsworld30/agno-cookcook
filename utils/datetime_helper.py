from datetime import datetime
import locale


def get_current_datetime_str() -> str:
    try:
        locale.setlocale(locale.LC_TIME, 'zh_CN.UTF-8')
    except:
        pass
    
    now = datetime.now()
    
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday = weekdays[now.weekday()]
    
    datetime_str = (
        f"当前时间: {now.year}年{now.month}月{now.day}日 "
        f"{now.hour:02d}:{now.minute:02d}:{now.second:02d} {weekday}"
    )
    
    return datetime_str


def get_datetime_context() -> str:
    return f"【系统时间】{get_current_datetime_str()}"
