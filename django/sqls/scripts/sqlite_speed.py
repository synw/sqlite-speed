import datetime
import dataset
import uuid
from sqls.models import Rec

runs = 500
records = 1000
sdb_path = "stats_django.sqlite"

db = dataset.connect('sqlite:///speedtest.sqlite')
sdb = None


def get_records():
    global records
    txt = "Lorem ipsum dolor"
    i = 0
    recs = []
    while i < records:
        recs.append(
            Rec(
                field1=txt,
                field2=txt,
                field3=txt,
                field4=txt,
                field5=txt,
                field6=txt,
                field7=txt,
                field8=txt,
                field9=txt,
                field10=txt,
                field11=txt,
                field12=txt,
                field13=1542,
                field14=0.5,
                field15=True,
            ))
        i += 1
    return recs


def initSdb():
    global sdb
    sdb = dataset.connect('sqlite:///' + sdb_path)


def recStat(rid, exec_time, numi, numruns, run):
    global sdb
    table = sdb["metrics"]
    data = dict(
        engine="django",
        num_inserts=numi,
        total_runs=numruns,
        run_id=rid,
        exec_time=exec_time,
        run=run,
        date=datetime.datetime.now())
    table.insert(data)


def run():
    global runs
    initSdb()
    timer = datetime.datetime.now()
    rid = str(uuid.uuid4())
    i = 1
    print("Starting", runs, "runs with", records, "records")
    while i < (runs + 1):
        objs = get_records()
        start = datetime.datetime.now()
        Rec.objects.bulk_create(objs)
        finish = datetime.datetime.now()
        extime = finish - start
        timer = timer + extime
        print(i + 1, ":", extime)
        ms = int(extime.total_seconds() * 1000)
        recStat(rid, ms, records, runs, i)
        i += 1
