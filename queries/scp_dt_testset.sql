SELECT distinct d.doi,
	case 
			when 'Erratum' = any(scp_type) then 'editorial_discourse'
			when 'Letter' = any(scp_type) then 'editorial_discourse'
			when 'Note' = any(scp_type) then 'editorial_discourse'
			when 'Review' = any(scp_type) then 'research_discourse'
			when 'Article' = any(scp_type) then 'research_discourse'
            else 'not assigned'
           end as scptype
FROM unignhaupka.oal_doc_dataset d
join unignhaupka.oal_wos_scp_s2_pubmed_comparison_2012_22 owsspc 
on d.doi = owsspc.doi