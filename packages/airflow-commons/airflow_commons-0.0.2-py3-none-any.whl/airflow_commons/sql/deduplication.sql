MERGE
    `{target_dataset}.{target_table}` T
USING
  (
  SELECT
    latest_row.*
  FROM (
    SELECT
      ARRAY_AGG(t
      ORDER BY
        {order_by_clause}
      LIMIT
        1)[
    OFFSET
      (0)] AS latest_row
    FROM (
      SELECT
        *
      FROM
        `{source_dataset}.{source_table}`
      WHERE
          {source_partition_field} BETWEEN '{start_date}'
        AND '{end_date}'
        AND {target_partition_field} >= '{oldest_target_partition}' ) AS t
    GROUP BY
        {group_by_clause} )) AS S
ON
  (T.{target_partition_field} >= '{oldest_target_partition}')
  AND {merge_keys}
  WHEN MATCHED THEN UPDATE SET {update_statements}
  WHEN NOT MATCHED
  THEN
INSERT
  ({columns})
VALUES
  ({columns});
