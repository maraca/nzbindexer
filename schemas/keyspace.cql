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


-- stores information about the status of data retrieval for a newsgroup
-- "name" represents the name of the group eg: alt.binaries.tv
-- "server" represents a usenet provider   eg: news.giganews.com
-- "first" represents the first article_number in the queue that has been parsed
-- "last" represents the latest article_number that has been parsed
-- we assume all items between first and last have been parsed.
CREATE TABLE newsgroups (
    name varchar,
    server varchar,
    first int,
    last int,
    PRIMARY KEY (name, server))
    WITH
    comment='Newsgroup the user has chose to index, associated with a usenet server';
