# BITSMITHS LIB #

This is the base/core Bitsmiths python library upon which all other products are built upon. This library contains the most
common base objects and patterns that we use for all our other projects.

This library contains both *normal* and *async* version of these common objects so that projects down the line can choose to
implement whichever version the need.


## Library Objects ##

These are the common objects in the library as well as a short description of their intended purpose.

### Transactionable ###

`Transactionable` is an interface class that allows derived objects to extend `begin`, `commit`, and `rollback`
methods. This object is intended to be used with database connections or any *transactionable* object. For example the
**Audit** Product extends this to do automatic record auditing on the `commit()` method.

Note there is also an `TransactionableAsync` object for *async* code.

### AutoTransaction ###

The `AutoTransaction` object is designed to be used with one or many `Transactionable` objects. After a piece of
*work* is complete, one would perform a `commit()` which would in turn `commit` all the *transactionable* objects that
were instantiated. If an error occurs, or if you do not do a `commit()`, this object will auto rollback all
the *transactionable* objects for you.

Note there is also an `AutoTransactionAsync` object for *async* code.

Below is an example of intended use:

```python

def save_bank_record(self, brec: tBank):
	with AutoTransaction(self.database_connection) as at:
		with BankManager(self.database_connection) as bm:
			bm.save(brec)
			at.commit()

```

### Pod ###

The intended purpose of the *Pod* is to contain the shared/common business objects in a given product. By our
design we always at least have the following public properities in a pod:

- dbcon : The active database connection that is ready for use
- cfg : A shared/common configuration dictionary
- log : The active logging logger object that is ready for use
- usr_id : The current business or systems user identifier string that is performing the current action/work

Think of a *Pod* as an object or dependency that you *inject* into all your business code down the line. The *Pod* contains
everything your business code needs to do its job. You are encouraged to extend the `Pod` object to have
any other common business properties your project requires.  Note also see the *Provider* for dynamically creating
core business objects.

You will notice that the `Pod` inherits from `Transactionable` and it also automatically `commits` and `rollbacks` the
database connection if it used with `AutoTransaction`.

Note there is also a `PodAsync` object for *async* code.

### Provider ###

The provider is designed to be an interface that you can override to create commonly used objects from sort
of factory.  It was originally a pattern we copied from C++, but it does have a place in Python frameworks if
one embraces the pattern.  We don't use it much, but there is nothing wrong with having it here.

### Query Builder ###

The `QueryBuilder` object is just a common piece of code use to string together dynamic SQL. Its is meant to be
relatively *SQL Injection* safe, but you it responsibly.

### Common ###

This is just a collection of commonly used functions that we use often in multiple different products.

### Sentinel ###

This is process/thread server management tool. More to explain here in the future.
