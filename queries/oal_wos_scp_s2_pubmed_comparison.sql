create table unignhaupka.oal_wos_scp_s2_pubmed_comparison_2012_22 as (	
	with 
		oal as (
			select lower(trim('https://doi.org/' from oal_works.doi)) as doi, oal_works.type as oal_type, 
				oal_sources.display_name as journal_title
			from fiz_openalex_rep_20230819_openbib.works oal_works
			left join fiz_openalex_rep_20230819_openbib.works_primary_locations oal_primary
               on oal_works.id = oal_primary.work_id
            left join fiz_openalex_rep_20230819_openbib.sources as oal_sources
                on oal_primary.source_id = oal_sources.id
            where oal_sources.type = 'journal' and oal_works.publication_year between 2012 and 2022 
		),
		scp as (
			select lower(doi) as doi, item_type as scp_type
			from scp_b_202307.items
			where source_type = 'Journal' and pubyear between 2012 and 2022
		),
		wos as (
			select lower(doi) as doi, item_type as wos_type
			from wos_b_202307.v_items 
			where source_type = 'Journal' and pubyear between 2012 and 2022
		),
		s2 as (
			select lower(externalids->>'DOI') as doi, publicationtypes as s2_type
            from open_add_ons.s2_2023_09_26_papers as s2_items
            left join open_add_ons.s2_2023_09_26_venues as s2_venues
            	on s2_items.publicationvenueid = s2_venues.id
            where s2_venues.type = 'journal' and year between 2012 and 2022
		),
		pm as (
			select lower(doi) as doi, ptype as pm_type, ptype_group as pm_grouptype 
			from dzhwaschniedermann.ac24_import_fromlocal as pm_items
			inner join dzhwaschniedermann.ac24_ptype_hierarchy as pm_type
				on pm_items.ptyperank = pm_type.grouprank
			where pubmed_date >= to_date('2012', 'yyyy') and pubmed_date < to_date('2023', 'yyyy')
		)
	select
		oal.doi,
		journal_title,
		oal_type,
		scp_type,
		wos_type,
		s2_type,
		pm_type,
		pm_grouptype
	from oal
	inner join scp
		on oal.doi = scp.doi
	inner join wos
		on oal.doi = wos.doi
	inner join s2
		on oal.doi = s2.doi
	inner join pm
		on oal.doi = pm.doi
)
