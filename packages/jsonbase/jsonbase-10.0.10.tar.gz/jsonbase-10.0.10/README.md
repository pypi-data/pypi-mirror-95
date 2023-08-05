# **JSONBASE**
## Description:
### jsonbase is a simple database module
### you can use it to store a small amount of data
### but that doesn't mean that you can store a big amount of data

#
![Preview](https://i.ibb.co/tXQkprn/image.png)
#
## `Why use jsonbase?`
### jsonbase is simple and easy to use

## `Will my data safe?`
### We have used json for over 1 month
### and yes, your data will safe
#
## Usage
```py
import jsonbase

database = jsonbase.database('my_database')
database.create()
```
```py
data = database.get()

data['Variable'] = 'value'
data['List'] = ['element','item']
data['Dict'] = {'key':'value'}
database.save(data)
```
#
## Quick Link
### [Docs](https://hackmd.io/@WinXpDev/BJ52SUeJu)