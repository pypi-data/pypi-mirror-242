import time
from abc import abstractmethod
from datetime import datetime
import redis
import schedule
import unidecode
from mobio.libs.Singleton import Singleton
from mobio.libs.thread_pool import ThreadPool
import socket


class RedisType:
    REPLICA = 1
    CLUSTER = 2


class BaseScheduler:
    thread_pool = ThreadPool(num_workers=1)
    logger = None

    def __init__(self, name=None, redis_uri=None, beat_time=300, redis_cluster_uri=None, redis_type=RedisType.REPLICA):
        self.name = name
        if not redis_uri and not redis_cluster_uri:
            raise Exception("redis_uri must not be None")

        if redis_type == RedisType.CLUSTER:
            if not redis_cluster_uri:
                self._redis = redis.from_url(redis_uri)
            else:
                from redis.cluster import RedisCluster as Redis
                self._redis = Redis.from_url(redis_cluster_uri)
        else:
            self._redis = redis.from_url(redis_uri)

        if not self.name:
            self.name = self.__class__.__name__
        self.name = unidecode.unidecode(self.name).replace(" ", "")

        self.hostname = socket.gethostname()

        self.schedule_job = None

    @abstractmethod
    def get_schedule(self):
        """
        hàm xác định thời điểm chạy của scheduler, bằng cách xử dụng thư viện schedule
        Các ví dụ hướng dẫn cách xác định thời gian chạy
        1. scheduler chỉ thực hiện công việc một lần duy nhất.
            return None
        2. scheduler sẽ thực hiện mỗi 10 phút một lần.
            return schedule.every(10).minutes
        3. scheduler sẽ thực hiện hàng ngày vào lúc 10h 30 phút.
            return schedule.every().day.at("10:30")
        4. scheduler sẽ thực hiện sau mỗi giờ.
            return schedule.every().hour
        5. scheduler sẽ thực hiện vào mỗi thứ 2 hàng tuần.
            return schedule.every().monday
        6. scheduler sẽ thực hiện vào mỗi thứ 5 hàng tuần và vào lúc 13h 15'.
            return schedule.every().wednesday.at("13:15")
        """
        raise NotImplementedError()

    @abstractmethod
    def owner_do(self):
        """
        đây là hàm sẽ thực hiện công việc của scheduler,
        hàm này sẽ được gọi tự động và tự động bắt lỗi ghi log
        """
        pass

    def set_logger(self, logger):
        self.logger = logger

    @thread_pool.thread
    def do(self):
        try:
            print(datetime.now(), " I'll start my job. ", self.name)
            self.owner_do()
            print(datetime.now(), " I'm finished my job. ", self.name)
        except Exception as e:
            if self.logger:
                self.logger.exception("run job error:%s!" % e)
            else:
                print("run job error:%s!" % e)
            return None

    def check_job_allow_running(self, job_id: str):
        """
        Check job_id allow for running. In some time, two workers can wakeup and get same job in parallel.
        Arguments:
            job_id: string
        Returns:
            True if first worker touch with job_id, else False
        """
        allow = self._redis.incrby(job_id)
        self._redis.expire(job_id, 5)
        return True if allow == 1 else False


@Singleton
class SchedulerFactory:
    def __init__(self):
        self.schedulers = {}
        self.tasks = {}
        self.logger = None

    def set_logger(self, logger):
        self.logger = logger

    def add(self, scheduler: BaseScheduler, scheduler_name=None):
        name = scheduler_name if scheduler_name else scheduler.__class__.__name__
        sq = self.schedulers.get(name, None)
        if sq is None:
            scheduler.set_logger(self.logger)
            the_schedule = scheduler.get_schedule()
            if the_schedule:
                scheduler.schedule_job = the_schedule
                the_schedule.do(scheduler.do)
                self.schedulers[name] = scheduler
            else:
                self.tasks[name] = scheduler
            return scheduler
        return sq

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    class TestScheduler1(BaseScheduler):
        def __init__(self, name):
            super().__init__(name)

        def get_schedule(self):
            return schedule.every(1).seconds

        def owner_do(self):
            print(datetime.now(), " I'm working. ", self.name)
            time.sleep(3)


    class TestScheduler2(BaseScheduler):
        def __init__(self, name):
            super().__init__(name)

        def get_schedule(self):
            return schedule.every(2).seconds

        def owner_do(self):
            print(datetime.now(), " I'm working. ", self.name)
            time.sleep(3)


    fac = SchedulerFactory()
    fac.add(TestScheduler1('Test1'), 'TestScheduler1')
    fac.add(TestScheduler1('Test2'), 'TestScheduler2')
    fac.run()
