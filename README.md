# Sqlite write speed tests

Test Sqlite write speed with various sql abstraction tools in Go and Python

## Tested tools

### Go

- [Gorm](https://github.com/jinzhu/gorm) : an orm
- [Goqu](https://github.com/doug-martin/goqu): an sql query builder
- [Xorm](https://github.com/go-xorm/xorm): an orm

### Python

- [Django orm](https://www.djangoproject.com/): the Django object relationnal mapper
- [Dataset](https://github.com/pudo/dataset): an easy way to handle database operations
in Python (uses [SqlAlchemy](http://www.sqlalchemy.org/) under the hood)

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

**Goqu**: average of 195 ms. Best run: 152 ms. Worst run: 561 ms

**Xorm**: average of 214 ms. Best run: 188 ms. Worst run: 487 ms

**Gorm**: average of 239 ms. Best run: 177 ms. Worst run: 513 ms
   
**Django**: average of 314 ms. Best run: 259 ms. Worst run: 641 ms

**Dataset**: average of 741 ms. Best run: 684 ms. Worst run: 1,49 s

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/bar.png)

#### Go

Blue: Gorm, Yellow: Xorm, Green: Goqu

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/timeline_go.png)

#### Python

Orange: Django, Green: Dataset

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/timeline_python.png)


### Execution time

#### Gorm

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/gorm_timeline.png)

#### Goqu

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/goqu_timeline.png)

#### Xorm

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/xorm_timeline.png)

#### Django

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/django_timeline.png)

#### Dataset

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/dataset_timeline.png)

### Regularity

This uses normalized data with the extreme values removed to compare the most common cases.

#### Normalized execution speed comparison

##### Go

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/go_norm.png)

##### Python

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/django_norm.png)

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/dataset_norm.png)

#### Distribution of the values

#### Gorm

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/gorm_distrib.png)

#### Goqu

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/goqu_distrib.png)

#### Xorm

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/xorm_distrib.png)

#### Django

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/django_distrib.png)

#### Dataset

![Img](https://raw.githubusercontent.com/synw/sqlite-speed/master/docs/img/dataset_distrib.png)

Dataset seems to have a lot of spikes. Considering the histograms Gorm seems to be the most irregular regarding
to the distribution of the values. Django appears to be very regular.

### Summary

Note: this is a subjective estimation

Engine | Speed | Ease of use | Regularity
--- | --- | --- | ---
Gorm | ++++ | ++++ | +
Goqu | +++++ | +++ | +++
Xorm | ++++ | ++++ | ++++
Django | +++ | ++++ | +++++
Dataset | + | +++++ | ++

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

To run the analytics on the generated data 
some [notebooks](https://github.com/synw/sqlite-speed-notebooks) are available 

## Todo

- [x] Automate multiple runs and stats
- [ ] Test with Xorm
- [x] Test with Django orm
- [ ] Publish the notebooks that build the charts from the collected data

