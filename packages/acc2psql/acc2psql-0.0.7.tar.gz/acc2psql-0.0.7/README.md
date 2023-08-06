# acc2psql
## Convert Microsoft Access *.accdb or *.mdb into *.sql PostgreSQL format
I believe in MS Access regarding its fast prototyping of relational database. You probably are not going to use MS Access in production environment due to its file based and single user restriction. But in a prototyping phase, MS Acces is one tool that is hard to beat!

Quick and easily prototype your database using MS Access, once satisfied, use this tool to convert said database into PostgreSQL DDL. You can either save it to *.sql file, dump it to console or directly execute it to PostgreSQL instance

```
pip install acc2sql
python -m acc2sql --src someawesomedatabase.accdb --dump
python -m acc2sql --src someawesomedatabase.accdb --out saveto.sql
python -m acc2sql --src someawesomedatabase.accdb --host localhost --username user --password password --db db
```
This package is still in early development, I may add more database source / target along the way.
You can also use this to any tool necessary: for example, I am thinking to use this as PyCharm Extension.. that will be awesome!
>Eko - Founder and CEO 
> 
>[Remote Worker Indonesia](https://remoteworker.id) / [LinkedIn](https://www.linkedin.com/organization-guest/company/remote-worker-id) / [Facebook](https://www.facebook.com/remoteworkerid) / [Instagram](https://www.instagram.com/remoteworker.id/) / [Twitter](https://twitter.com/remoteworkerid) 
> 
>[Youtube: Everybody can code!](https://www.youtube.com/watch?v=h2naH3WawpU)
> 
>[Spotify: Everybody can code!](https://open.spotify.com/episode/2MeFoHkbvsyMZiplw01yYv?si=EQFpnYZoTzyp_JngpuIzEQ)
>
> swdev.balI@gmail.com


