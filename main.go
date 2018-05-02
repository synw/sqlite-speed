package main

import (
	"flag"
	"fmt"
	"github.com/jamiealquiza/tachymeter"
	"github.com/synw/sqlite-speed/db"
	"github.com/synw/sqlite-speed/types"
	"log"
	"time"
)

var runs = flag.Int("r", 10, "Number of runs to make")
var records = flag.Int("n", 1000, "Number of records to insert")
var engine = flag.String("e", "gorm", "Database engine")
var stats = flag.Bool("s", false, "Record stats")
var statsDb string = "stats.sqlite"

func main() {
	flag.Parse()
	fmt.Println("Start inserting", *records, "records with the", *engine, "engine")
	// init stuff
	if *stats == true {
		db.InitStats(statsDb)
	}
	db.InitGoqDb()
	// run
	var ds []time.Duration
	t := tachymeter.New(&tachymeter.Config{Size: *runs})
	for i := 1; i <= *runs; i++ {
		d, ok := run(*engine, *records)
		if ok != true {
			log.Println("Error executing inserts during run", i)
			return
		}
		fmt.Println(i, ":", d)
		ds = append(ds, d)
		t.AddTime(d)
		if *stats == true {
			// record metric in stats database
			metric := getMetric(*engine, *records, i, *runs, d)
			db.SaveMetric(metric)
		}
	}
	var total time.Duration
	for _, d := range ds {
		total += d
	}
	dur := t.Calc()
	//stats := fmt.Sprintf("%s", dur.JSON())
	//fmt.Println(stats)
	fmt.Println(dur.String())
	fmt.Println("Completed the", *runs, "runs in an average of",
		dur.Time.Avg,
		",all runs took", total)
}

func run(engine string, records int) (time.Duration, bool) {
	var d time.Duration
	var ok bool
	if engine == "gorm" {
		d, ok = db.GormRun(getRecs(records))
	} else if engine == "goqu" {
		d, ok = db.GoqRun(getRecs(records))
	}
	return d, ok
}

func getMetric(engine string, numInserts int, run int, runs int, execTime time.Duration) types.Metric {
	metric := types.Metric{
		Engine:     engine,
		NumInserts: numInserts,
		TotalRuns:  runs,
		Run:        run,
		ExecTime:   int64(execTime / time.Millisecond),
		Date:       time.Now(),
	}
	return metric
}

func getRecord() types.Record {
	str := "Lorem ipsum dolor"
	in := 1542
	fl := 0.5
	rec := types.Record{
		Field1:  str,
		Field2:  str,
		Field3:  str,
		Field4:  str,
		Field5:  str,
		Field6:  str,
		Field7:  str,
		Field8:  str,
		Field9:  str,
		Field10: str,
		Field11: str,
		Field12: str,
		Field13: in,
		Field14: fl,
		Field15: true,
	}
	return rec
}

func getRecs(records int) []types.Record {
	var recs []types.Record
	i := 0
	for i < records {
		recs = append(recs, getRecord())
		i += 1
	}
	return recs
}
