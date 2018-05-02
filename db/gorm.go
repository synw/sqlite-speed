package db

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"github.com/synw/sqlite-speed/types"
	"log"
	"time"
)

func GormRun(records []types.Record) (time.Duration, bool) {
	db := connect("speedtest.sqlite")
	//defer elapsed(len(records))()
	start := time.Now()
	tx := db.Begin()
	for i, rec := range records {
		tx.Create(&rec)
		if tx.Error != nil {
			tx.Rollback()
			msg := tx.Error.Error()
			log.Println("Error creating record", i, "\n", msg)
			var d time.Duration
			return d, false
		}
	}
	tx.Commit()
	return time.Since(start), true
}

func connect(addr string) *gorm.DB {
	db, err := gorm.Open("sqlite3", addr)
	if err != nil {
		panic(err)
	}
	return db
}
