# starframe
Extension of polars dataframe to stars schema

The project aims to handle one specific of https://en.wikipedia.org/wiki/Star_schema
based on Polars dataframes when working in star schema allows significant reduction
in memory/storage/network bandwidth used.

It is also my toy project for Polars and Rust - at least until someone else thinks
it is a good idea and joins me.

Initial assumptions:

* we do only eager dataframes at the beginning
* only star schema, not snowflake
