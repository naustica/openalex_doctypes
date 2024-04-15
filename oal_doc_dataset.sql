create table unignhaupka.oal_doc_dataset as (
	select distinct 
	       owsspc.doi, 
		   owsspc.pm_grouptype, 
		   case 
           	when pm_type in ('Cochrane Systematic Review', 'Systematic Review', 'Meta-Analysis', 'Review', 'Case Reports', 'Randomized Controlled Trial', 'Clinical Trial', 
                               'Clinical Trial, Phase II', 'Clinical Trial, Phase III', 'Clinical Trial, Phase I', 
                               'Clinical Trial, Phase IV', 'Controlled Clinical Trial', 'Pragmatic Clinical Trial', 'Journal Article', 'Comparative Study', 'Multicenter Study', 
                               'Observational Study', 'Evaluation Study', 'Historical Article', 'Validation Study', 'Clinical Study', 'Randomized Controlled Trial, Veterinary',
                               'Twin Study', 'Clinical Trial, Veterinary', 'Classical Article', 'Observational Study, Veterinary', 'Corrected and Republished Article', 
                               'Adaptive Clinical Trial', 'Evaluation Studies', 'Validation Studies') then 'research_discourse'
            when pm_grouptype = 'funding_info' then 'research_discourse'
           	when pm_type in ('Published Erratum', 'Retraction of Publication', 'Retracted Publication', 'Editorial', 'News', 'Letter', 'Comment',
                                'Introductory Journal Article', 'Newspaper Article') then 'editorial_discourse'
            else 'not assigned'
           end as type,
		   co.abstract, 
		   co.title, 
		   co.page as page, 
		   json_array_length(co.author) as author_count,
		   case 
		   	when json_array_length(co.license) > 0 then 1
		   	else 0
		   end has_license,
		   co.is_referenced_by_count,
		   co.references_count,
		   case 
		   	when json_array_length(co.funder) > 0 then 1
		   	else 0
		   end has_funder
	from unignhaupka.oal_wos_scp_s2_pubmed_comparison_2012_22 owsspc 
	join open_add_ons.cr_oct2023 co 
		on lower(owsspc.doi) = lower(co.doi)	
)