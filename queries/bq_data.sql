EXPORT DATA
  OPTIONS (
    uri='gs://bigschol/document_type_snapshot/*.jsonl.gz',
    compression='GZIP',
    format='json')
AS (
    SELECT DISTINCT
            oal.doi,
            CASE 
              WHEN cr.abstract IS NOT NULL THEN 1 
              ELSE 0
            END has_abstract,
            cr.title,
            cr.page as page,
            ARRAY_LENGTH(cr.author) as author_count,
            CASE
                WHEN ARRAY_LENGTH(cr.license) > 0 THEN 1
                ELSE 0
            END has_license,
            cr.is_referenced_by_count,
            cr.references_count,
            CASE
                WHEN ARRAY_LENGTH(cr.funder) > 0 THEN 1
                ELSE 0
            END has_funder,
            CASE
                WHEN oal.institutions_distinct_count > 0 THEN oal.institutions_distinct_count
                ELSE 1
            END as inst_count,
            CASE
                WHEN oal.open_access.oa_url IS NOT NULL THEN 1
                ELSE 0
            END has_oa_url
    FROM `subugoe-wag-closed.oal_doctypes.cr_snapshot` AS cr
    JOIN `subugoe-collaborative.openalex.works` AS oal
        ON LOWER(cr.doi) = LOWER(oal.doi)
)