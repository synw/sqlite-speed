package db

import (
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
	"github.com/synw/sqlite-speed/types"
)

var statsDb *gorm.DB

func SaveMetric(metric types.Metric) {
	statsDb.Create(&metric)
}

func InitStats(addr string) error {
	err := connectStats(addr)
	if err != nil {
		return err
	}
	statsDb.AutoMigrate(&types.Metric{})
	return nil
}

func connectStats(addr string) error {
	var err error
	statsDb, err = gorm.Open("sqlite3", addr)
	if err != nil {
		return err
	}
	return nil
}
