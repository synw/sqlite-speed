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

Inserting 1000 records (average of 10 runs):

**Dataset**: 789 milliseconds

**Gorm**: 263 milliseconds

**Goqu**: 253 milliseconds

Quick conclusion: Gorm and Goqu are nearly equivalent and Dataset is 3x times slower.

## Run the tests

Get the stuff:

   ```
   go get github.com/synw/sqlite-speed
   ```

Go to `$GOPATH/src/github.com/synw/sqlite-speed`

To create the database run the python script to add a first record:

   ```
   python3 pydb -r 1
   ```

Start testing:

- Python: `python3 pydb`
- Gorm: `go run main.go`
- Goqu: `go run main.go -e goqu`

Option: use the `-r` flag to specify the number of records to insert (default is 1000). Ex:
`go run main.go -r 10000`

## Todo

- [ ] Automate multiple runs and stats
- [ ] Test with Xorm
- [ ] Maybe test with Django orm

