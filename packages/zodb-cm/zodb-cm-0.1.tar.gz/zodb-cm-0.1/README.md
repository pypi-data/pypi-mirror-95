# ZODB context manager

## Installation

`pip install zodb-cm`


### ZConnection()

- Provides a ZODB connection with auto-abort (default).
- Provides a tuple of connection and root object:

```
      with ZConnection(db) as cx, root:
          root.one = "ok"
```
- ZConnection implements a connection context manager.
- Transaction context managers in contrast do auto-commit:
  1. with db.transaction() as connection, or
  1. with cx.transaction_manager as transaction, or
  1. with transaction.manager as transaction  (for the thread-local transaction manager)
- See also http://www.zodb.org/en/latest/guide/transactions-and-threading.html
    
    
### ZDatabase()

- Provides a ZODB database context manager.
    