CREATE KEYSPACE news
    WITH REPLICATION = {'CLASS': 'SimpleStrategy',
                        'replication_factor': 1};

-- stores information about a file uploaded on usenet,
-- probably using yEnc and split across several "segments".
-- Each "segment" is represented as a map<xx/yy, message_id>
-- where xx/yy -> 001/100 and unique_id is this http://en.wikipedia.org/wiki/Message-ID
-- "subject" represents the name of the file, and "groups"
-- a set of groups where the file can be found.
CREATE TABLE files (
    subject varchar,
    segments map<varchar, varchar>,
    groups set<varchar>,
    PRIMARY KEY(subject) )
    WITH
    comment='Lists of segments associated with a file.';

