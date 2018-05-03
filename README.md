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

**Gorm**: average of 239 milliseconds

**Goqu**: average of 195 milliseconds
   
**Dataset**: average of 741 milliseconds

![All](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/bar.png)

![Timeline](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/timeline_all.png)

Legend: orange: Dataset, blue: Gorm, green: Goqu

### Execution time

#### Gorm

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/gorm_timeline.png)

#### Goqu

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/goqu_timeline.png)

#### Dataset

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/dataset_timeline.png)

### Regularity

This uses normalized data with the extreme values removed to compare the most common cases.

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/goqu_gorm_norm.png)

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/dataset_norm.png)

Dataset seems to have a lot of spikes. Considering the histograms above Gorm seems to be the most irregular regarding
to the distributions of the values.

### Summary

Engine | Speed | Ease of use
--- | --- | ---
**Gorm** | ++++ | ++++
**Goqu** | +++++ | +++
**Dataset** | + | +++++

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
   python3 pydb -n 1 -r 1
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

## Stats

Use the `-s` flag to log the execution times per run 

The datapoints are collected in a database to be able to 
process analytics on it. The default database is `stats.sqlite`.
To change the database location use the `-sdb` flag: ex:
`python3 pydb -s -sbd /home/me/somewhere/stats.sqlite`

## Todo

- [x] Automate multiple runs and stats
- [ ] Test with Xorm
- [ ] Maybe test with Django orm
- [ ] Publish the notebooks that build the charts from the collected data

