-- the user-user graph based on crate dependency and crate ownership
COPY (SELECT distinct u2.gh_login as gh_source, u1.gh_login as gh_target from crates c1
INNER JOIN crate_owners co1 ON co1.crate_id = c1.id
INNER JOIN users u1 ON (u1.id=co1.owner_id AND co1.owner_kind=0)
INNER JOIN dependencies d ON d.crate_id=c1.id
INNER JOIN versions ON d.version_id=versions.id
INNER JOIN crates c2 ON versions.crate_id=c2.id
INNER JOIN crate_owners co2 ON co2.crate_id=c2.id
INNER JOIN users u2 ON (u2.id=co2.owner_id AND co2.owner_kind=0))
TO '/tmp/user-graph.csv' (format csv, delimiter ',');

-- the user-user graph based on crate dependency and crate ownership
COPY (SELECT distinct u2.gh_login as gh_source, u1.gh_login as gh_target from crates c1
INNER JOIN crate_owners co1 ON co1.crate_id = c1.id
INNER JOIN users u1 ON (u1.id=co1.owner_id AND co1.owner_kind=0)
INNER JOIN dependencies d ON d.crate_id=c1.id
INNER JOIN versions ON d.version_id=versions.id
INNER JOIN crates c2 ON versions.crate_id=c2.id
INNER JOIN crate_owners co2 ON co2.crate_id=c2.id
INNER JOIN users u2 ON (u2.id=co2.owner_id AND co2.owner_kind=0)
WHERE c1.repository not like 'https://github.com/rust-lang/%')
TO '/tmp/user-graph-not-rust-lang.csv' (format csv, delimiter ',');


-- the module-module graph based on crate dependency
COPY (SELECT distinct c2.name as source_crate, c1.name as target_crate from crates c1
INNER JOIN dependencies d ON d.crate_id=c1.id
INNER JOIN versions ON d.version_id=versions.id
INNER JOIN crates c2 ON versions.crate_id=c2.id)
TO '/tmp/crate-graph.csv' (format csv, delimiter ',');

-- user-module ownership
COPY (SELECT users.gh_login,crates.name as crate_name FROM users
INNER JOIN crate_owners co ON (co.owner_id=users.id AND co.owner_kind=0)
INNER JOIN crates ON crates.id=co.crate_id)
TO '/tmp/user-crates.csv' (format csv, delimiter ',');

-- user data for presentation
COPY (SELECT gh_login, name, gh_avatar FROM users) TO '/tmp/users.csv' (format csv, delimiter ',');
