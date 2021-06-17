from celery import Celery

app = Celery("VerWorkr",
             broker='pyamqp://guest@10.0.0.152//',
             backend="rpc://",
             include=[f'{__name__.split(".")[0]}.tasks']
)
