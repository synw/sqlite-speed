import datetime
import argparse
import dataset

db = dataset.connect('sqlite:///speedtest.sqlite')


def get_records(num=100):
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
    parser.add_argument('-r', dest='records', type=int, default=1000,
                        help='Number of records to insert')
    args = parser.parse_args()
    print("Starting to save records ...")
    start = datetime.datetime.now()
    recs = get_records(args.records)
    insert(recs)
    finish = datetime.datetime.now()
    extime = finish - start
    print("Saved", len(recs), "records in", extime)
