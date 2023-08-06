SELECT MIN({target_partition_field}) as oldest_value
FROM `{dataset_id}.{table_id}`
WHERE `{source_partition_field}` BETWEEN '{start_date}' and '{end_date}';
