# <h2 id="title"> Thư viện Schedule trên ngôn ngữ Python để chạy service background.</h2>

# Copyright: MobioVN

# CHANGE LOG:
## v1.0.1
- Support Redis cluster

## v1.0.0
- Breaking change:
    + Core concept của phiên bản này là các schedule có thể chạy song song nhằm giải quyết các bài toán như xử lý import excel, csv đồng thời.
    + Để tránh N schedule cùng xử lý 1 file, call self.check_job_allow_running(str_job_id) để check xem job đấy trong 5seconds vừa qua đã có được worker nào xử lý hay không?
    + Giải thuật ở đây là tận dụng Atomic của redis, sử dụng incrby function để check redis-key đã tồn tại chưa? chỉ có worker thao tác incrby đầu tiên(return value = 1) mới có quyền xử lý file
  
## v0.6.7
- Sửa lỗi key "last_run"


#### Cài đặt:
`$ pip3 install m-schedule`

#### Sử dụng:

1. Tạo class thực thi scheduler kế thừa từ class BaseScheduler
    ```python
    class TestScheduler(BaseScheduler):
        def owner_do(self):
            lst_job = db.excel_file.find({"status":0}).limit(1)
            for job in lst_job:
                if self.check_job_allow_running(str(job.id)):
                    print("execute {}".format(job.id))
                else:
                    print("job {} is running".format(job.id))
            pass
    
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
        return schedule.every(10).minutes
    ```

2. Đăng ký scheduler với factory
    ```python
    factory = SchedulerFactory()
    factory.add(TestScheduler(name="MyScheduler", redis_uri="redis://redis-server:6379/0"))
    # sample using redis cluster
    factory.add(TestScheduler(name="MyScheduler1", redis_cluster_uri="redis://redis-cluster.redis.svc.cluster.local:6379/0", redis_type=RedisType.REPLICA))
    factory.run()
    ```