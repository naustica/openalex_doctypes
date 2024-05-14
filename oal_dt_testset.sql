SELECT distinct d.doi,
	case 
           	when oal_type in ('article', 'journal-article') then 'research_discourse'
           	when oal_type in ('erratum', 'editorial', 'letter', 'paratext') then 'editorial_discourse'
            else 'not assigned'
           end as oaltype
FROM unignhaupka.oal_doc_dataset d
join unignhaupka.oal_wos_scp_s2_pubmed_comparison_2012_22 owsspc 
on d.doi = owsspc.doi
