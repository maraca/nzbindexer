CREATE KEYSPACE news
    WITH REPLICATION = {'CLASS': 'SimpleStrategy',
                        'replication_factor': 1};

CREATE TABLE segments (
    bytes int,
    number int,
    title varchar,
    PRIMARY KEY (title, number)
 )
    WITH
    comment='Also knows as parts, segments represent a list of yEnc files that must be grouped in order to download a single file.';
