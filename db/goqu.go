package db

import (
	"database/sql"
	"encoding/json"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"github.com/synw/sqlite-speed/types"
	"gopkg.in/doug-martin/goqu.v4"
	_ "gopkg.in/doug-martin/goqu.v4/adapters/sqlite3"
)

func GoqRun(records []types.Record) {
	sdb, err := sql.Open("sqlite3", "speedtest.sqlite")
	if err != nil {
		panic(err.Error())
	}
	db := goqu.New("sqlite3", sdb)
	recs := getGoqRecs(records)
	defer elapsed(len(records))()
	if _, err := db.From("records").Insert(recs).Exec(); err != nil {
		fmt.Println(err.Error())
		return
	}
}

func getGoqRecs(records []types.Record) []goqu.Record {
	var recs []goqu.Record
	for _, rec := range records {
		jrec, err := json.Marshal(rec)
		if err != nil {
			fmt.Println(err)
			return recs
		}
		var qrec goqu.Record
		err = json.Unmarshal(jrec, &qrec)
		if err != nil {
			fmt.Println(err)
			return recs
		}
		recs = append(recs, qrec)
	}
	return recs
}
