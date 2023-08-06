Changelog
=========

0.4.1 (2019-09-20)
------------------

- Improve indexing on `request` table that avoid error with to large response
  [mpeeters]


0.4.0 (2019-09-11)
------------------

- Update request table schema
  [mpeeters]

- Add `session` parameter to use a specific session with mapper methods
  [mpeeters]

- Remove unicity constraint on url column for `router` table
  [mpeeters]


0.3.2 (2019-05-22)
------------------

- Add file type "Email entrant" in DB
  [ndemonte]

- Handle potentially optional type metadata
  [ndemonte]

0.3.1 (2018-12-06)
------------------

- Add `delete` method on mappers
  [mpeeters]


0.3.0 (2018-12-03)
------------------

- Add the mapper for the `router` table
  [mpeeters]

- Add the column to store the response in the database
  [mpeeters]


0.2.1 (2018-11-29)
------------------

- Add a function to return a session not bound to a transaction manager
  [mpeeters]


0.2 (2016-04-22)
----------------

- Update the file types for database generation script
  [mpeeters]

- Add the Request mapper
  [mpeeters]

- Removed accented chars in sql
  [sgeulette]

0.1 (2014-10-17)
----------------

- Initial release
  [mpeeters]
