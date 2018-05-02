# Sqlite write speed tests

Test Sqlite write speed with various sql abstraction tools in Go and Python

## Tested tools

- [Gorm](https://github.com/jinzhu/gorm) : an orm in Go
- [Goqu](https://github.com/doug-martin/goqu): an sql query builder in Go
- [Dataset](https://github.com/pudo/dataset): an easy way to handle database operations
in Python (uses [SqlAlchemy](http://www.sqlalchemy.org/) under the hood).

## Test design

### Disclaimer

This test does not pretend to be a serious benchmark at all. It is a test made
on a small i7 4G ram laptop to figure out the orders of magnitude and the ease of use of the 
tools.

### Data structure

The test inserts records with 13 columns of short text, one of integer, one float and 
one boolean (because this is the kind of data I needed to test for).

All the tests wrap the insert statements into one single transaction.

## Results

Inserting 1000 records (500 runs):

**Gorm**: average of 268 milliseconds

   ```
Cumulative:	2m14.1530073s
HMean:		265.290449ms
Avg.:		268.306014ms
p50: 		265.146922ms
p75:		276.984217ms
p95:		311.541648ms
p99:		418.302206ms
p999:		642.729644ms
Long 5%:	375.964761ms
Short 5%:	232.874774ms
Max:		642.729644ms
Min:		221.76369ms
Range:		420.965954ms
StdDev:		34.302226ms
Rate/sec.:	3.73
   ```

**Goqu**: average of 209 milliseconds

   ```
Cumulative:	1m44.986583994s
HMean:		207.157227ms
Avg.:		209.973167ms
p50: 		205.084806ms
p75:		216.253239ms
p95:		242.910185ms
p99:		354.530163ms
p999:		535.133082ms
Long 5%:	306.202476ms
Short 5%:	180.577667ms
Max:		535.133082ms
Min:		173.921859ms
Range:		361.211223ms
StdDev:		30.698196ms
Rate/sec.:	4.76
   ```
   
**Dataset**: average of 796 milliseconds  [todo: detailed python stats]

Quick conclusion: Dataset is about 3 times slower than the Go solutions. Goqu appears to
be the fastest, and gorm is not far.

## Run the tests

   ```
   pip install dataset
   ```

Get the stuff:

   ```
   go get github.com/synw/sqlite-speed
   ```

Go to `$GOPATH/src/github.com/synw/sqlite-speed`

To create the database run the python script to add a first record:

   ```
   python3 pydb -n 1
   ```

Start testing:

- Python: `python3 pydb`
- Gorm: `go run main.go`
- Goqu: `go run main.go -e goqu`

Optional command line arguments:

`-n`: sets the number of records to insert per run. Default is 1000. 
Ex: `go run main.go -n 10000`

`-r`: sets the number of runs. Default is 10.
Ex: `go run main.go -r 100`

## Todo

- [x] Automate multiple runs and stats
- [ ] Test with Xorm
- [ ] Maybe test with Django orm

