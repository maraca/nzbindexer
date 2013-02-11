CREATE KEYSPACE news
    WITH REPLICATION = {'CLASS': 'SimpleStrategy',
                        'replication_factor': 1};

CREATE TABLE segments (
    bytes int,
    number int,
    title varchar,
    PRIMARY KEY (title, number)
 );
