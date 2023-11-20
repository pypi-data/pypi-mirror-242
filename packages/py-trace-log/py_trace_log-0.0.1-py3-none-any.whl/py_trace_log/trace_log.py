# -*- coding: UTF-8 -*-
import logging
import logging.handlers 
from skywalking.trace.context import get_context
logger = logging.getLogger()
#定义链路追踪过滤器
class TraceFilter(logging.Filter):
  traceId = ""
  def filter(self, record):
    record.traceId = getTraceId()
    return True
## 获取链路追踪id
def getTraceId():
     return str(get_context().segment.related_traces[0])
#链路追踪类
class TraceLog(object):
  """
  日志记录
  """
  def __init__(self, logname='trace_log'):
    self.logname = logname
    self.logger =  logging.getLogger()
    self.logger.setLevel(logging.INFO)
    self.logger.propagate = False
    self.filter_ = TraceFilter()
    self.logger.addFilter(self.filter_)
    self.formatter = logging.Formatter("[%(traceId)s]-%(asctime)s %(name)s %(filename)s [pid:%(process)d] [%(threadName)s] [line:%(lineno)d] %(levelname)s %(message)s")
  def console(self, level, message):
    # 创建一个FileHandler，用于写到本地
    fh = logging.handlers.TimedRotatingFileHandler(self.logname, when='MIDNIGHT', interval=1, encoding='utf-8')
    fh.suffix = '%Y-%m-%d.log'
    fh.setLevel(logging.INFO)
    fh.setFormatter(self.formatter)
    self.logger.addHandler(fh)

    # 创建一个StreamHandler,用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(self.formatter)
    self.logger.addHandler(ch)

    if level == 'info':
      self.logger.info(message)
    elif level == 'debug':
      self.logger.debug(message)
    elif level == 'warning':
      self.logger.warning(message)
    elif level == 'error':
      self.logger.error(message)
    # 这两行代码是为了避免日志输出重复问题
    self.logger.removeHandler(ch)
    self.logger.removeHandler(fh)
    # 关闭打开的文件
    fh.close()

  def debug(self, message):
    self.console('debug', message)

  def info(self, message):
    self.console('info', message)

  def warning(self, message):
    self.console('warning', message)

  def error(self, message):
    self.console('error', message)