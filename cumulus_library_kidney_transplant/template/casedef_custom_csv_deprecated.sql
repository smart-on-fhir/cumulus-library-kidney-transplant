CREATE EXTERNAL TABLE irae__casedef_csv
(
    vocab	        string,
    code	        string,
    display         string,
    likely          string,
    preop           string,
    transplant      string,
    rejection       string,
    failure         string,
    outcome         string,
    lab             string,
    imaging         string,
    count_sum       string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar"     = "\"",
  "escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION 's3://cumulus-analytics/andy/irae/casedef/curated/'
TBLPROPERTIES ("skip.header.line.count"="1");

