package db

import (
	"fmt"
	"time"
)

func elapsed(records int) func() {
	start := time.Now()
	return func() {
		fmt.Println("Saved", records, "records in", time.Since(start))
	}
}
