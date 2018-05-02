package main

import (
	"flag"
	"fmt"
	"github.com/synw/sqlite-speed/db"
	"github.com/synw/sqlite-speed/types"
)

var runs = flag.Int("r", 10, "Number of runs to make")
var records = flag.Int("n", 1000, "Number of records to insert")
var engine = flag.String("e", "gorm", "Database engine")

func main() {
	flag.Parse()
	fmt.Println("Start inserting", *records, "records with the", *engine, "engine")
	run(*engine, *records)
	fmt.Println("Finished inserting", *records, "records")
}

func run(engine string, records int) {
	if engine == "gorm" {
		db.GormRun(getRecs(records))
	} else if engine == "goqu" {
		db.GoqRun(getRecs(records))
	}
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
