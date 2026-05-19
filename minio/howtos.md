### Enter in the minio container:
 - `mc alias set local http://localhost:9000 minadmin minadmin`
### To see the buckets
 - `mc ls local`
### To add an event 
 - `mc event add ALIAS/BUCKETNAME arn:minio:sqs::primary:webhook --event EVENTS_LIST` 
### To list the events
  - `mc event list ALIAS/BUCKETNAME `
