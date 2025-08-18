create or replace view irae__rx_belatacept as select * from (values
('http://www.nlm.nih.gov/research/umls/rxnorm', '1112973', 'Belatacept')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1112976', 'Belatacept 250 MG Injection')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1112977', 'Nulojix')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1112980', 'Nulojix 250 MG Injection')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1155316', 'Belatacept Injectable Product')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1178807', 'Nulojix Injectable Product')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1804970', 'Belatacept 250 MG')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1804971', 'Belatacept Injection')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1804973', 'Belatacept 250 MG [Nulojix]')
,('http://www.nlm.nih.gov/research/umls/rxnorm', '1804974', 'Belatacept Injection [Nulojix]')
) AS t (system, code, display) ;