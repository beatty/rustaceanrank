Generates PageRank over the universe of Rust crates and the Rustaceans who own them.

Lastest generated rankings maintained at https://www.johndbeatty.com/rustaceanrank.html

Note: this is throwaway code. I'm purely making it available for transparency in how the rankings were generated. The code is not meant to be portable, maintainable, etc.

This is just a fun little way to explore Rustaceans and crates. I'm personally just using it to find very good Rustaceans to work on a new project.

How to run:
1. Download the crates database archive at https://crates.io/data-access.
1. Run "psql crates < crates.sql"
1. Install dependencies. e.g. pip3 install -r requirements.txt
1. Run python rustaceanrank.py

Limitations
* Only the crate owners are considered, which excludes very many significant contributors to crates that are not owners. Ideally contribution level from git would be used. I think this would be 10x the work. If someone knows of a very quick way to get this from github, drop me a note or a PR.
