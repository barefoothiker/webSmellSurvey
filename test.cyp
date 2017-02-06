CREATE (Comobidity:subphenotype {name:'Comobidity'})
CREATE (name:subclass {name:'Co-morbidity_name'})
CREATE (status:subclass {name:'condition_status'})
CREATE (treatment:subclass {name:'on_treatment'})

CREATE (asthma:name {name:'asthma'})
CREATE (cancer:name {name:'cancer'})
CREATE (Cystic_fibrosis:name {name:'Cystic_fibrosis'})
CREATE (Sjorgren:name {name:'Sjorgren_syndrome'})

CREATE (remission:status {name:'in_remission'})
CREATE (uncontrolled:status {name:'uncontrolled'})
CREATE (controlled:status {name:'well_controlled'})

CREATE (yes:boolen {name:'yes'})
CREATE (no:boolen {name: 'no'})

CREATE
  (status)-[:IS_SUBCLASS]->(Comobidity),
  (treatment)-[:IS_SUBCLASS]->(Comobidity),
  (name)-[:IS_SUBCLASS]->(Comobidity),
  (yes)-[:IS_VALUE]->(treatment),
  (no)-[:IS_VALUE]->(treatment),
  (remission)-[:IS_VALUE]->(status),
  (uncontrolled)-[:IS_VALUE]->(status),
  (controlled)-[:IS_VALUE]->(status),
  
  (asthma)-[:IS_VALUE]-> (name),
  (cancer)-[:IS_VALUE]-> (name),
  (Cystic_fibrosis) -[:IS_VALUE]->(name),
  (Sjorgren)-[:IS_VALUE]-> (name)