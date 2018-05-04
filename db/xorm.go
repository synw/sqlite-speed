package db

import (
	"github.com/go-xorm/xorm"
	_ "github.com/mattn/go-sqlite3"
	"github.com/synw/sqlite-speed/types"
	"time"
)

var engine *xorm.Engine = connectX("speedtest.sqlite")

func XormRun(records []types.Record) (time.Duration, bool) {
	start := time.Now()
	session := engine.NewSession()
	defer session.Close()
	if err := session.Begin(); err != nil {
		panic(err)
	}
	for _, rec := range records {
		_, _ = session.Insert(&rec)
	}
	session.Commit()
	return time.Since(start), true
}

func connectX(addr string) *xorm.Engine {
	eng, err := xorm.NewEngine("sqlite3", addr)
	if err != nil {
		panic(err)
	}
	return eng
}
