import datetime
import argparse
import dataset
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Boolean, Integer, String, create_engine
from sqlalchemy.orm import Session

conn = None
engine = None
sdb = None
Base = declarative_base()


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    
    field1 = Column(String(255))
    field2 = Column(String(255))
    field3 = Column(String(255))
    field4 = Column(String(255))
    field5 = Column(String(255))
    field6 = Column(String(255))
    field7 = Column(String(255))
    field8 = Column(String(255))
    field9 = Column(String(255))
    field10 = Column(String(255))
    field11 = Column(String(255))
    field12 = Column(String(255))
    field13 = Column(Integer())
    field14 = Column(Float())
    field15 = Column(Boolean())


def init_db():
    global engine, conn
    engine = create_engine("sqlite:///speedtest.sqlite")
    conn = engine.connect()


def insert(n=1000):
    global engine
    init_db()
    session = Session(bind=engine)
    session.bulk_save_objects([
        Record(
            field1="Lorem ipsum dolor",
            field2="Lorem ipsum dolor",
            field3="Lorem ipsum dolor",
            field4="Lorem ipsum dolor",
            field5="Lorem ipsum dolor",
            field6="Lorem ipsum dolor",
            field7="Lorem ipsum dolor",
            field8="Lorem ipsum dolor",
            field9="Lorem ipsum dolor",
            field10="Lorem ipsum dolor",
            field11="Lorem ipsum dolor",
            field12="Lorem ipsum dolor",
            field13=4578,
            field14=1578.258,
            field15=True,
        )
        for i in range(n)
    ])
    session.commit()


def initSdb(path):
    global sdb
    sdb = dataset.connect('sqlite:///' + path)


def recStat(rid, exec_time, numi, numruns, run):
    global sdb
    table = sdb["metrics"]
    data = dict(
            engine="sqlalchemy",
            num_inserts=numi,
            total_runs=numruns,
            run_id=rid,
            exec_time=exec_time,
            run=run,
            date=datetime.datetime.now())
    table.insert(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='records', type=int, default=1000,
                        help='Number of records to insert')
    parser.add_argument('-r', dest='runs', type=int, default=10,
                        help='Number of runs to make')
    parser.add_argument('-s', dest='stats', action='store_true',
                        help='Log runs in a database')
    parser.add_argument('-sdb', dest='sdb', type=str,
                        default="stats.sqlite",
                        help='Stats database location')
    args = parser.parse_args()
    print("Starting to save", args.records, "records per run.",
          "Doing", args.runs, "runs")
    if args.stats is True:
        print("Logging results to stats db")
        initSdb(args.sdb)
    i = 0
    timer = datetime.datetime.now()
    st = timer
    rid = str(uuid.uuid4())
    while i < args.runs:
        start = datetime.datetime.now()
        insert()
        finish = datetime.datetime.now()
        extime = finish - start
        timer = timer + extime
        print(i + 1, ":", extime)
        if args.stats is True:
            ms = int(extime.total_seconds() * 1000)
            recStat(rid, ms, args.records, args.runs, i)
        i += 1
    timer = timer - st
    avg = timer / args.runs
    print("Completed the", args.records, "runs in an average of", avg,
          "all runs took", timer)
