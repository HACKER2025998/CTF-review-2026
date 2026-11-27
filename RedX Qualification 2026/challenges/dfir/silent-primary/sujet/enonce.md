# Silent Primary

- **Category:** DFIR
- **Author:** Viscanturtle
- **Difficulty:** —
- **Points:** 100 (dynamic, initial 500)
- **Solves:** 88
- **Instance:** none

## Statement

During end-of-day reconciliation on our fintech database cluster, automated checks flagged a balance discrepancy between the primary server and its read replica. Replication health shows zero errors, and the on-call DBA suspects routine replica drift.

You have been given offline copies of both servers MySQL data directories and my.cnf configuration files. Determine which server holds the tampered balance, recover the legitimate balance, and identify the exact GTID sequence number of the last logged transaction committed immediately before the divergence occurred.

Flag Format: `RxR{<accountid><legitimatebalance><last_gtid_seq_before_divergence>}`

Flag Example: `RxR{1_2_3}`
