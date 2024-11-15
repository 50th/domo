import logging
import logging.handlers
import os
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

import portalocker


def get_lock_filename(log_file: Path) -> Path:
    """
    定义日志文件锁名称，类似于 `.__file.lock`，其中file与日志文件baseFilename一致

    :param log_file: 日志文件路径
    :return: 锁文件名称
    """
    # hide the file on Unix and generally from file completion
    lock_file = log_file.parent / f'.__{log_file.name.removesuffix(".log")}.lock'
    return lock_file


class ConcurrentTimedRotatingFileHandler(TimedRotatingFileHandler):
    # 上一次翻转时间
    before_rollover_at = -1

    def __init__(self, filename: Path, *args, **kwargs):
        super().__init__(filename, *args, **kwargs)

        file_path = os.path.split(filename)[0]
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        self.concurrent_lock = portalocker.Lock(get_lock_filename(filename), flags=portalocker.LOCK_EX)

    def emit(self, record) -> None:
        """
        本方法继承Python标准库,修改的部分已在下方使用注释标记出
        本次改动主要是对日志文件进行加锁，并且保证在多进程环境下日志内容切割正确
        """
        # 此行为新增代码，尝试获取非重入进程锁，阻塞，直到成功获取
        with self.concurrent_lock:
            try:
                if self.shouldRollover(record):
                    self.doRollover()

                """
                如果日志内容创建时间小于上一次翻转时间，不能记录在baseFilename文件中，否则正常记录

                处理日志写入哪个日志文件，修改开始
                """
                if record.created <= ConcurrentTimedRotatingFileHandler.before_rollover_at:
                    current_time = int(record.created)
                    # v 引用Python3.7标准库logging.TimedRotatingFileHandler.doRollover(110:124)中翻转目标文件名生成代码 v
                    dst_now = time.localtime(current_time)[-1]
                    t = self.computeRollover(current_time) - self.interval
                    if self.utc:
                        time_tuple = time.gmtime(t)
                    else:
                        time_tuple = time.localtime(t)
                        dst_then = time_tuple[-1]
                        if dst_now != dst_then:
                            if dst_now:
                                addend = 3600
                            else:
                                addend = -3600
                            time_tuple = time.localtime(t + addend)
                    dfn = self.rotation_filename(self.baseFilename + "." +
                                                 time.strftime(self.suffix, time_tuple))
                    # ^ 引用标准库TimedRotatingFileHandler中翻转目标文件名生成规则代码                                  ^

                    # 如果back_count值设置的过低，会出现日志文件实际数量大于设置值
                    # 因为当日志写入负载过高时，之前的某个时刻产生的日志会延迟到现在才进行写入，在写入时又找不到与时间对应的日志文件，
                    # 则会再创建一个与日志创建时刻对应的日志文件进行写入。
                    # 对应的日志文件是指达到翻转条件后创建的翻转文件，文件命名规则与标准库一致。
                    self._do_write_record(dfn, record)
                else:
                    logging.FileHandler.emit(self, record)
                """
                处理日志写入哪个日志文件，修改结束
                """
            except Exception:
                self.handleError(record)

    def doRollover(self):
        """
        本方法继承Python标准库,修改的部分已在下方使用注释标记出
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(t)
        else:
            time_tuple = time.localtime(t)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, time_tuple))
        """
        如果翻转文件已经生成，则说明其他进程已经处理过翻转
        处理日志文件已经翻转当前进程中未写入文件的日志副本，修改开始
        """
        # 直接修改静态变量，因为代码执行到此处已经获取到非重入进程锁，保证同一时间只有一个线程对变量进行修改
        # 由于Python GIL，同一时间同一进程内只有一个线程运行，线程切换后缓存自动失效，即其他线程可以看见修改后的最新值
        # 记录每一次触发翻转动作的时间，不管反转是否真的执行
        ConcurrentTimedRotatingFileHandler.before_rollover_at = self.rolloverAt
        if os.path.exists(dfn):
            # 因为进程变量不会在内存同步，所以存在其他进程已经翻转过日志文件当时当前进程中还标识为未翻转
            # 日志内容创建时间如果小于等于下一个处理翻转时刻，则将日志写入反转后的日志文件，而不是当前的baseFilename
            # 当前磁盘上的baseFilename对于当前进程中的标识副本来说已经是翻转后要写入的文件
            # 所以当文件存在时，本次不再进行翻转动作
            pass
        else:
            self.rotate(self.baseFilename, dfn)
        """
        处理日志文件已经翻转当前进程中未写入文件的日志副本，修改结束
        """
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                new_rollover_at += addend
        # 此刻，当前进程中的标识副本已经同步为最新
        self.rolloverAt = new_rollover_at

    def _do_write_record(self, dfn, record):
        """
        将日志内容写入指定文件

        :param dfn: 指定日志文件
        :param record: 日志内容
        """
        with open(dfn, mode="a", encoding=self.encoding) as file:
            file.write(self.format(record) + self.terminator)


class ConcurrentRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename: Path, *args, **kwargs):
        super().__init__(filename, *args, **kwargs)

        file_dir = os.path.split(filename)[0]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        self.lock_filename = get_lock_filename(filename)
        # self.concurrent_lock = portalocker.Lock(lock_filename, flags=portalocker.LOCK_EX)

    def _do_rollover(self, record):
        # 检查日志文件是否需要翻转
        base_stream = self._open()
        base_stream.seek(0, 2)
        msg = "%s\n" % self.format(record)
        base_stream_length = base_stream.tell() + len(msg)
        base_stream.close()
        if base_stream_length >= self.maxBytes:
            # print('current pid: %d, doRollover' % os.getpid())
            try:
                super().doRollover()
            except PermissionError as e:
                if self.stream:
                    self.stream.close()
                    self.stream = None
        else:
            if self.stream:
                self.stream.close()
                self.stream = None
            if not self.delay:
                self.stream = self._open()

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        with portalocker.Lock(self.lock_filename, flags=portalocker.LOCK_EX):
            try:
                if self.shouldRollover(record):
                    # print('current pid: %d, shouldRollover: %d' % (os.getpid(), self.shouldRollover(record)))
                    self._do_rollover(record)
                logging.FileHandler.emit(self, record)
            except Exception:
                self.handleError(record)


# 添加当前类到 "logging.handlers" 模块中，使logging.config.fileConfig()进行配置时可以使用
# logging.handlers.ConcurrentTimedRotatingFileHandler = ConcurrentTimedRotatingFileHandler
# logging.handlers.ConcurrentRotatingFileHandler = ConcurrentRotatingFileHandler
