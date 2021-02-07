
## DataStax Cassandra setup:

### Create id/number table for counters
` CREATE TABLE IF NOT EXISTS userdata.website ( id text PRIMARY KEY, number counter ); `

### Create user table
` CREATE TABLE IF NOT EXISTS userdata.users ( email text PRIMARY KEY, password text, firstname text, lastname text ); `

### Create item type
` CREATE TYPE IF NOT EXISTS restaurant.item ( name text, carbs float, fat float, protein float ); `

### Create restaurant table
```
CREATE TABLE IF NOT EXISTS restaurant.restaurants (
    name text PRIMARY KEY,
    website text,
    latitude float,
    longitude float,
    items list<frozen<restaurant.item>>
);
```


### Insert a user
```
insert into userdata.users (email, password, firstname, lastname) values (
    'cambones12@gmail.com', '12345', 'Cam', 'Bones'
);
```
    
