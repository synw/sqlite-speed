import datetime
import argparse
import dataset
import uuid

db = dataset.connect('sqlite:///speedtest.sqlite')
sdb = None


def get_records(num=1000):
    recs = []
    i = 0
    while i < num:
        rec = {}
        j = 15
        while j > 0:
            field = "Field" + str(j)
            val = "record value"
            if j == 13:
                val = 4578
            elif j == 14:
                val = 1578.258
            elif j == 15:
                val = True
            rec[field] = val
            j -= 1
        recs.append(rec)
        i += 1
        # print(rec)
    return recs


def insert(recs):
    db.begin()
    try:
        i = 0
        for rec in recs:
            # print("Record "+str(i))
            db['records'].insert(rec)
            i += 1
        db.commit()
    except Exception as e:
        db.rollback()
        raise(e)


def initSdb(path):
    global sdb
    sdb = dataset.connect('sqlite:///'+path)


def recStat(rid, exec_time, numi, numruns):
    global sdb
    table = sdb["metrics"]
    data = dict(
            engine="dataset",
            num_inserts=numi,
            total_runs=numruns,
            run_id=rid,
            exec_time=exec_time,
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
    recs = get_records(args.records)
    i = 0
    timer = datetime.datetime.now()
    st = timer
    rid = str(uuid.uuid4())
    while i < args.runs:
        start = datetime.datetime.now()
        insert(recs)
        finish = datetime.datetime.now()
        extime = finish - start
        timer = timer + extime
        print(i + 1, ":", extime)
        if args.stats is True:
            ms = int(extime.total_seconds() * 1000)
            recStat(rid, ms, args.records, args.runs)
        i += 1
    timer = timer - st
    avg = timer / args.runs
    print("Completed the", len(recs), "runs in an average of", avg,
          "all runs took", timer)
