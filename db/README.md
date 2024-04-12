# Adding tasks to the database using python

1. Include SQL
   
```
import sqlite3
```

2. Connent to database and create a cursor
   
```
connection = sqlite3.connect('./db/database.db')
with open('./db/schema.sql') as f:
      connection.executescript(f.read())

cur = connection.cursor()
```

3. Use cursor to execute SQL INSERT command
    - Replace 'Task Name' with the name of the task you wish to add
    - For status, 0 is incomplete and 1 is complete, always add new tasks with the status 0
    - Add date in the format 'year-month-day' or None

   ### Task  with a specific date:
```
cur.execute("INSERT INTO tasks (name, status, due_date) VALUES (?, ?, ?)",
         ('Task Name', 0, '2024-4-10')
         )
```

   ### Task without specific date:
```
cur.execute("INSERT INTO tasks (name, status, due_date) VALUES (?, ?, ?)",
         ('Task Name', 0, 'None')
         )
```
   
5. Close the database when done

```
connection.commit()
connection.close()
```


# Blank Task Template for implementation

```
import sqlite3

connection = sqlite3.connect('./db/database.db')
with open('./db/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO tasks (name, status, due_date) VALUES (?, ?, ?)",
            ('', 0, '')
            )

connection.commit()
connection.close()
```
