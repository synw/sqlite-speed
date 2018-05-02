package db

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"github.com/synw/sqlite-speed/types"
	"log"
)

func GormRun(records []types.Record) {
	db := connect("speedtest.sqlite")
	tx := db.Begin()
	for i, rec := range records {
		tx.Create(&rec)
		if tx.Error != nil {
			tx.Rollback()
			msg := tx.Error.Error()
			log.Println("Error creating record", i, "\n", msg)
			return
		}
	}
	tx.Commit()
}

func connect(addr string) *gorm.DB {
	db, err := gorm.Open("sqlite3", addr)
	if err != nil {
		panic(err)
	}
	return db
}
