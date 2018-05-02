import datetime
import argparse
import dataset

db = dataset.connect('sqlite:///speedtest.sqlite')


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='records', type=int, default=1000,
                        help='Number of records to insert')
    parser.add_argument('-r', dest='runs', type=int, default=10,
                        help='Number of runs to make')
    args = parser.parse_args()
    print("Starting to save", args.records, "records ...")
    recs = get_records(args.records)
    i = 0
    timer = datetime.datetime.now()
    st = timer
    while i < args.runs:
        start = datetime.datetime.now()
        insert(recs)
        finish = datetime.datetime.now()
        extime = finish - start
        timer = timer + extime
        print(i + 1, ":", extime)
        i += 1
    timer = timer - st
    avg = timer / args.runs
    print("Completed the", len(recs), "runs in an average of", avg,
          ",all runs took", timer)
