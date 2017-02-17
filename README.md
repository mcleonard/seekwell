
# SeekWell

SeekWell is a package for quickly and easily querying SQL databases in Python. It was made with data analysts in mind and plays well with Jupyter notebooks. This notebook is a little tutorial to get you started working with SQL databases in under 5 minutes.

SeekWell is a higher level library built on top of SQLAlchemy, an amazing library that does all the heavy lifting. SeekWell is designed to get our of your way and focus on retrieving the data you want from your database. 

Query results are retrieved in a lazy manner. That is, they aren't returned until you ask for them. Records are cached once you get them, so you only ever run the query once. SeekWell also provides methods for inspecting the tables and columns in your database.


```python
from seekwell import Database
```

## Connect to the database

SeekWell uses SQLAlchemy underneath to connect to literally any database you can throw at it. You just need the appropriate engines, for example, psychopg for PostGres. Make sure to check out [SQLAlchemy's documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html) for connecting to databases.

In SeekWell, you just need to import the `Database` class and create a new Database object. The path required is defined by SQLAlchemy (link to documentation here).

Here I'll load a database of European soccer matches, teams, and players available [from Kaggle Datasets](https://www.kaggle.com/hugomathien/soccer). 


```python
db = Database('sqlite:///database.sqlite')
```

I've found database introspection to be really useful, that is, listing out tables and columns. When connected to a `Database`, you can get a list of tables.


```python
db.table_names
```




    ['Country',
     'League',
     'country',
     'Match',
     'Player',
     'Team',
     'Player_Attributes',
     'Team_Attributes',
     'sqlite_sequence']



And you can get a table to inspect it.


```python
table = db['Team']
table
```




    Table(Team, Database('sqlite:///database.sqlite'))




```python
table.column_names
```




    ['id', 'team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name']



To check out the data in a table, use the `head` method to print out the first few rows.


```python
table.head()
```




<table style="font-size:10pt; white-space:nowrap;">
<tr><th>id</th> <th>team_api_id</th> <th>team_fifa_api_id</th> <th>team_long_name</th> <th>team_short_name</th></tr>
<tr><td>1</td> <td>9987</td> <td>673</td> <td>KRC Genk</td> <td>GEN</td></tr>
<tr><td>2</td> <td>9993</td> <td>675</td> <td>Beerschot AC</td> <td>BAC</td></tr>
<tr><td>3</td> <td>10000</td> <td>15005</td> <td>SV Zulte-Waregem</td> <td>ZUL</td></tr>
<tr><td>4</td> <td>9994</td> <td>2007</td> <td>Sporting Lokeren</td> <td>LOK</td></tr>
<tr><td>5</td> <td>9984</td> <td>1750</td> <td>KSV Cercle Brugge</td> <td>CEB</td></tr>
<tr><td>6</td> <td>8635</td> <td>229</td> <td>RSC Anderlecht</td> <td>AND</td></tr>
<tr><td>7</td> <td>9991</td> <td>674</td> <td>KAA Gent</td> <td>GEN</td></tr>
<tr><td>8</td> <td>9998</td> <td>1747</td> <td>RAEC Mons</td> <td>MON</td></tr>
<tr><td>9</td> <td>7947</td> <td>None</td> <td>FCV Dender EH</td> <td>DEN</td></tr>
<tr><td>10</td> <td>9985</td> <td>232</td> <td>Standard de Liège</td> <td>STL</td></tr>

</table>



In a notebook, rows are printed out in an HTML table for nice viewing. In the terminal, rows are printed out as an ASCII table.


```python
print(table.head())
```

     id | team_api_id | team_fifa_api_id | team_long_name    | team_short_name 
    ----+-------------+------------------+-------------------+-----------------
     1  | 9987        | 673              | KRC Genk          | GEN             
     2  | 9993        | 675              | Beerschot AC      | BAC             
     3  | 10000       | 15005            | SV Zulte-Waregem  | ZUL             
     4  | 9994        | 2007             | Sporting Lokeren  | LOK             
     5  | 9984        | 1750             | KSV Cercle Brugge | CEB             
     6  | 8635        | 229              | RSC Anderlecht    | AND             
     7  | 9991        | 674              | KAA Gent          | GEN             
     8  | 9998        | 1747             | RAEC Mons         | MON             
     9  | 7947        | None             | FCV Dender EH     | DEN             
     10 | 9985        | 232              | Standard de Liège | STL             


If you're using a database with schemas, you can get a list of the schema names with `db.schema_names`.


```python
db.schema_names
```




    ['main']



## Querying

There we go, now you're connected to the database and it's ready to be queried. Data analysts are all about getting data and workign with it. Queries are run through the Database object's `query` method. It accepts a SQL statement as a string and returns a `Records` object.


```python
records = db.query('SELECT * from Player limit 50')
```

The data isn't returned immediately, only when you request it.


```python
records
```




<table style="font-size:10pt; white-space:nowrap;">
<tr><th>id</th> <th>player_api_id</th> <th>player_name</th> <th>player_fifa_api_id</th> <th>birthday</th> <th>height</th> <th>weight</th></tr>


</table>



Use `fetch` to get the data. Calling `fetch` without any arguments will return all the rows. Passing in a number will return that many rows.


```python
records.fetch(10)
```




<table style="font-size:10pt; white-space:nowrap;">
<tr><th>id</th> <th>player_api_id</th> <th>player_name</th> <th>player_fifa_api_id</th> <th>birthday</th> <th>height</th> <th>weight</th></tr>
<tr><td>1</td> <td>505942</td> <td>Aaron Appindangoye</td> <td>218353</td> <td>1992-02-29 00:00:00</td> <td>182.88</td> <td>187</td></tr>
<tr><td>2</td> <td>155782</td> <td>Aaron Cresswell</td> <td>189615</td> <td>1989-12-15 00:00:00</td> <td>170.18</td> <td>146</td></tr>
<tr><td>3</td> <td>162549</td> <td>Aaron Doran</td> <td>186170</td> <td>1991-05-13 00:00:00</td> <td>170.18</td> <td>163</td></tr>
<tr><td>4</td> <td>30572</td> <td>Aaron Galindo</td> <td>140161</td> <td>1982-05-08 00:00:00</td> <td>182.88</td> <td>198</td></tr>
<tr><td>5</td> <td>23780</td> <td>Aaron Hughes</td> <td>17725</td> <td>1979-11-08 00:00:00</td> <td>182.88</td> <td>154</td></tr>
<tr><td>6</td> <td>27316</td> <td>Aaron Hunt</td> <td>158138</td> <td>1986-09-04 00:00:00</td> <td>182.88</td> <td>161</td></tr>
<tr><td>7</td> <td>564793</td> <td>Aaron Kuhl</td> <td>221280</td> <td>1996-01-30 00:00:00</td> <td>172.72</td> <td>146</td></tr>
<tr><td>8</td> <td>30895</td> <td>Aaron Lennon</td> <td>152747</td> <td>1987-04-16 00:00:00</td> <td>165.1</td> <td>139</td></tr>
<tr><td>9</td> <td>528212</td> <td>Aaron Lennox</td> <td>206592</td> <td>1993-02-19 00:00:00</td> <td>190.5</td> <td>181</td></tr>
<tr><td>10</td> <td>101042</td> <td>Aaron Meijers</td> <td>188621</td> <td>1987-10-28 00:00:00</td> <td>175.26</td> <td>170</td></tr>

</table>



The data is cached in `records.rows`


```python
records.rows
```




    [(1, 505942, 'Aaron Appindangoye', 218353, '1992-02-29 00:00:00', 182.88, 187),
     (2, 155782, 'Aaron Cresswell', 189615, '1989-12-15 00:00:00', 170.18, 146),
     (3, 162549, 'Aaron Doran', 186170, '1991-05-13 00:00:00', 170.18, 163),
     (4, 30572, 'Aaron Galindo', 140161, '1982-05-08 00:00:00', 182.88, 198),
     (5, 23780, 'Aaron Hughes', 17725, '1979-11-08 00:00:00', 182.88, 154),
     (6, 27316, 'Aaron Hunt', 158138, '1986-09-04 00:00:00', 182.88, 161),
     (7, 564793, 'Aaron Kuhl', 221280, '1996-01-30 00:00:00', 172.72, 146),
     (8, 30895, 'Aaron Lennon', 152747, '1987-04-16 00:00:00', 165.1, 139),
     (9, 528212, 'Aaron Lennox', 206592, '1993-02-19 00:00:00', 190.5, 181),
     (10, 101042, 'Aaron Meijers', 188621, '1987-10-28 00:00:00', 175.26, 170)]



You can get rows using slices too.


```python
records[5:15]
```




<table style="font-size:10pt; white-space:nowrap;">
<tr><th>id</th> <th>player_api_id</th> <th>player_name</th> <th>player_fifa_api_id</th> <th>birthday</th> <th>height</th> <th>weight</th></tr>
<tr><td>6</td> <td>27316</td> <td>Aaron Hunt</td> <td>158138</td> <td>1986-09-04 00:00:00</td> <td>182.88</td> <td>161</td></tr>
<tr><td>7</td> <td>564793</td> <td>Aaron Kuhl</td> <td>221280</td> <td>1996-01-30 00:00:00</td> <td>172.72</td> <td>146</td></tr>
<tr><td>8</td> <td>30895</td> <td>Aaron Lennon</td> <td>152747</td> <td>1987-04-16 00:00:00</td> <td>165.1</td> <td>139</td></tr>
<tr><td>9</td> <td>528212</td> <td>Aaron Lennox</td> <td>206592</td> <td>1993-02-19 00:00:00</td> <td>190.5</td> <td>181</td></tr>
<tr><td>10</td> <td>101042</td> <td>Aaron Meijers</td> <td>188621</td> <td>1987-10-28 00:00:00</td> <td>175.26</td> <td>170</td></tr>
<tr><td>11</td> <td>23889</td> <td>Aaron Mokoena</td> <td>47189</td> <td>1980-11-25 00:00:00</td> <td>182.88</td> <td>181</td></tr>
<tr><td>12</td> <td>231592</td> <td>Aaron Mooy</td> <td>194958</td> <td>1990-09-15 00:00:00</td> <td>175.26</td> <td>150</td></tr>
<tr><td>13</td> <td>163222</td> <td>Aaron Muirhead</td> <td>213568</td> <td>1990-08-30 00:00:00</td> <td>187.96</td> <td>168</td></tr>
<tr><td>14</td> <td>40719</td> <td>Aaron Niguez</td> <td>183853</td> <td>1989-04-26 00:00:00</td> <td>170.18</td> <td>143</td></tr>
<tr><td>15</td> <td>75489</td> <td>Aaron Ramsey</td> <td>186561</td> <td>1990-12-26 00:00:00</td> <td>177.8</td> <td>154</td></tr>

</table>




```python
records[-5:]
```




<table style="font-size:10pt; white-space:nowrap;">
<tr><th>id</th> <th>player_api_id</th> <th>player_name</th> <th>player_fifa_api_id</th> <th>birthday</th> <th>height</th> <th>weight</th></tr>
<tr><td>46</td> <td>409003</td> <td>Abdoulaye Keita</td> <td>212280</td> <td>1994-01-05 00:00:00</td> <td>175.26</td> <td>165</td></tr>
<tr><td>47</td> <td>37280</td> <td>Abdoulaye Meite</td> <td>41745</td> <td>1980-10-06 00:00:00</td> <td>185.42</td> <td>181</td></tr>
<tr><td>48</td> <td>439366</td> <td>Abdoulaye Toure</td> <td>210450</td> <td>1994-03-03 00:00:00</td> <td>187.96</td> <td>170</td></tr>
<tr><td>49</td> <td>148827</td> <td>Abdoulwahid Sissoko</td> <td>189568</td> <td>1990-03-20 00:00:00</td> <td>182.88</td> <td>165</td></tr>
<tr><td>50</td> <td>173011</td> <td>Abdourahman Dampha</td> <td>197901</td> <td>1991-12-27 00:00:00</td> <td>182.88</td> <td>168</td></tr>

</table>



Or get all the rows by calling `fetch` with no arguments...


```python
records.fetch()
```




<table style="font-size:10pt; white-space:nowrap;">
<tr><th>id</th> <th>player_api_id</th> <th>player_name</th> <th>player_fifa_api_id</th> <th>birthday</th> <th>height</th> <th>weight</th></tr>
<tr><td>1</td> <td>505942</td> <td>Aaron Appindangoye</td> <td>218353</td> <td>1992-02-29 00:00:00</td> <td>182.88</td> <td>187</td></tr>
<tr><td>2</td> <td>155782</td> <td>Aaron Cresswell</td> <td>189615</td> <td>1989-12-15 00:00:00</td> <td>170.18</td> <td>146</td></tr>
<tr><td>3</td> <td>162549</td> <td>Aaron Doran</td> <td>186170</td> <td>1991-05-13 00:00:00</td> <td>170.18</td> <td>163</td></tr>
<tr><td>4</td> <td>30572</td> <td>Aaron Galindo</td> <td>140161</td> <td>1982-05-08 00:00:00</td> <td>182.88</td> <td>198</td></tr>
<tr><td>5</td> <td>23780</td> <td>Aaron Hughes</td> <td>17725</td> <td>1979-11-08 00:00:00</td> <td>182.88</td> <td>154</td></tr>
<tr><td>6</td> <td>27316</td> <td>Aaron Hunt</td> <td>158138</td> <td>1986-09-04 00:00:00</td> <td>182.88</td> <td>161</td></tr>
<tr><td>7</td> <td>564793</td> <td>Aaron Kuhl</td> <td>221280</td> <td>1996-01-30 00:00:00</td> <td>172.72</td> <td>146</td></tr>
<tr><td>8</td> <td>30895</td> <td>Aaron Lennon</td> <td>152747</td> <td>1987-04-16 00:00:00</td> <td>165.1</td> <td>139</td></tr>
<tr><td>9</td> <td>528212</td> <td>Aaron Lennox</td> <td>206592</td> <td>1993-02-19 00:00:00</td> <td>190.5</td> <td>181</td></tr>
<tr><td>10</td> <td>101042</td> <td>Aaron Meijers</td> <td>188621</td> <td>1987-10-28 00:00:00</td> <td>175.26</td> <td>170</td></tr>
<tr><td>11</td> <td>23889</td> <td>Aaron Mokoena</td> <td>47189</td> <td>1980-11-25 00:00:00</td> <td>182.88</td> <td>181</td></tr>
<tr><td>12</td> <td>231592</td> <td>Aaron Mooy</td> <td>194958</td> <td>1990-09-15 00:00:00</td> <td>175.26</td> <td>150</td></tr>
<tr><td>13</td> <td>163222</td> <td>Aaron Muirhead</td> <td>213568</td> <td>1990-08-30 00:00:00</td> <td>187.96</td> <td>168</td></tr>
<tr><td>14</td> <td>40719</td> <td>Aaron Niguez</td> <td>183853</td> <td>1989-04-26 00:00:00</td> <td>170.18</td> <td>143</td></tr>
<tr><td>15</td> <td>75489</td> <td>Aaron Ramsey</td> <td>186561</td> <td>1990-12-26 00:00:00</td> <td>177.8</td> <td>154</td></tr>
<tr><td>16</td> <td>597948</td> <td>Aaron Splaine</td> <td>226014</td> <td>1996-10-13 00:00:00</td> <td>172.72</td> <td>163</td></tr>
<tr><td>17</td> <td>161644</td> <td>Aaron Taylor-Sinclair</td> <td>213569</td> <td>1991-04-08 00:00:00</td> <td>182.88</td> <td>176</td></tr>
<tr><td>18</td> <td>23499</td> <td>Aaron Wilbraham</td> <td>2335</td> <td>1979-10-21 00:00:00</td> <td>190.5</td> <td>159</td></tr>
<tr><td>19</td> <td>120919</td> <td>Aatif Chahechouhe</td> <td>187939</td> <td>1986-07-02 00:00:00</td> <td>175.26</td> <td>150</td></tr>
<tr><td>20</td> <td>46447</td> <td>Abasse Ba</td> <td>156626</td> <td>1976-07-12 00:00:00</td> <td>187.96</td> <td>185</td></tr>
<tr><td>21</td> <td>167027</td> <td>Abdelaziz Barrada</td> <td>192274</td> <td>1989-06-19 00:00:00</td> <td>177.8</td> <td>161</td></tr>
<tr><td>22</td> <td>245653</td> <td>Abdelfettah Boukhriss</td> <td>202425</td> <td>1986-10-22 00:00:00</td> <td>185.42</td> <td>161</td></tr>
<tr><td>23</td> <td>128456</td> <td>Abdelhamid El Kaoutari</td> <td>188145</td> <td>1990-03-17 00:00:00</td> <td>180.34</td> <td>161</td></tr>
<tr><td>24</td> <td>42664</td> <td>Abdelkader Ghezzal</td> <td>178063</td> <td>1984-12-05 00:00:00</td> <td>182.88</td> <td>172</td></tr>
<tr><td>25</td> <td>425950</td> <td>Abdellah Zoubir</td> <td>212934</td> <td>1991-12-05 00:00:00</td> <td>180.34</td> <td>161</td></tr>
<tr><td>26</td> <td>38423</td> <td>Abdelmajid Oulmers</td> <td>52782</td> <td>1978-09-12 00:00:00</td> <td>172.72</td> <td>143</td></tr>
<tr><td>27</td> <td>3264</td> <td>Abdelmalek Cherrad</td> <td>51868</td> <td>1981-01-14 00:00:00</td> <td>185.42</td> <td>165</td></tr>
<tr><td>28</td> <td>467485</td> <td>Abdelmalek El Hasnaoui</td> <td>209399</td> <td>1994-02-09 00:00:00</td> <td>180.34</td> <td>159</td></tr>
<tr><td>29</td> <td>306735</td> <td>Abdelouahed Chakhsi</td> <td>210504</td> <td>1986-10-01 00:00:00</td> <td>182.88</td> <td>170</td></tr>
<tr><td>30</td> <td>41659</td> <td>Abderrazak Jadid</td> <td>149241</td> <td>1983-06-01 00:00:00</td> <td>177.8</td> <td>157</td></tr>
<tr><td>31</td> <td>31684</td> <td>Abdeslam Ouaddou</td> <td>33022</td> <td>1978-11-01 00:00:00</td> <td>190.5</td> <td>181</td></tr>
<tr><td>32</td> <td>32637</td> <td>Abdessalam Benjelloun</td> <td>177295</td> <td>1985-01-28 00:00:00</td> <td>187.96</td> <td>179</td></tr>
<tr><td>33</td> <td>563215</td> <td>Abdou Diallo</td> <td>225711</td> <td>1996-05-04 00:00:00</td> <td>182.88</td> <td>159</td></tr>
<tr><td>34</td> <td>41093</td> <td>Abdou Traore</td> <td>187048</td> <td>1988-01-17 00:00:00</td> <td>180.34</td> <td>174</td></tr>
<tr><td>35</td> <td>564712</td> <td>Abdoul Ba</td> <td>225050</td> <td>1994-02-08 00:00:00</td> <td>200.66</td> <td>212</td></tr>
<tr><td>36</td> <td>67334</td> <td>Abdoul Karim Yoda</td> <td>188232</td> <td>1988-10-25 00:00:00</td> <td>182.88</td> <td>161</td></tr>
<tr><td>37</td> <td>173955</td> <td>Abdoul Razzagui Camara</td> <td>193953</td> <td>1990-02-20 00:00:00</td> <td>177.8</td> <td>157</td></tr>
<tr><td>38</td> <td>39562</td> <td>Abdoulay Konko</td> <td>161999</td> <td>1984-03-09 00:00:00</td> <td>182.88</td> <td>157</td></tr>
<tr><td>39</td> <td>191784</td> <td>Abdoulaye Ba</td> <td>204826</td> <td>1991-01-01 00:00:00</td> <td>198.12</td> <td>174</td></tr>
<tr><td>40</td> <td>210400</td> <td>Abdoulaye Bamba</td> <td>199313</td> <td>1990-04-25 00:00:00</td> <td>182.88</td> <td>150</td></tr>
<tr><td>41</td> <td>201915</td> <td>Abdoulaye Diaby</td> <td>202330</td> <td>1991-05-21 00:00:00</td> <td>172.72</td> <td>154</td></tr>
<tr><td>42</td> <td>194479</td> <td>Abdoulaye Diallo Sadio,22</td> <td>204171</td> <td>1990-12-28 00:00:00</td> <td>182.88</td> <td>168</td></tr>
<tr><td>43</td> <td>189181</td> <td>Abdoulaye Diallo</td> <td>197233</td> <td>1992-03-30 00:00:00</td> <td>187.96</td> <td>174</td></tr>
<tr><td>44</td> <td>352887</td> <td>Abdoulaye Doucoure</td> <td>208135</td> <td>1993-01-01 00:00:00</td> <td>182.88</td> <td>165</td></tr>
<tr><td>45</td> <td>40005</td> <td>Abdoulaye Faye</td> <td>100329</td> <td>1978-02-26 00:00:00</td> <td>187.96</td> <td>218</td></tr>
<tr><td>46</td> <td>409003</td> <td>Abdoulaye Keita</td> <td>212280</td> <td>1994-01-05 00:00:00</td> <td>175.26</td> <td>165</td></tr>
<tr><td>47</td> <td>37280</td> <td>Abdoulaye Meite</td> <td>41745</td> <td>1980-10-06 00:00:00</td> <td>185.42</td> <td>181</td></tr>
<tr><td>48</td> <td>439366</td> <td>Abdoulaye Toure</td> <td>210450</td> <td>1994-03-03 00:00:00</td> <td>187.96</td> <td>170</td></tr>
<tr><td>49</td> <td>148827</td> <td>Abdoulwahid Sissoko</td> <td>189568</td> <td>1990-03-20 00:00:00</td> <td>182.88</td> <td>165</td></tr>
<tr><td>50</td> <td>173011</td> <td>Abdourahman Dampha</td> <td>197901</td> <td>1991-12-27 00:00:00</td> <td>182.88</td> <td>168</td></tr>

</table>



Your statements can of course be as complex as you want. Using parameters in statements is possible using keyword arguments. This uses the SQLAlchemy `text` syntax, so [read up on it here](http://docs.sqlalchemy.org/en/rel_1_1/core/sqlelement.html?highlight=text#sqlalchemy.sql.expression.text). Below is an example using `:home_team` as a parameter to filter for the desired home team in the statement.


```python
statement = """
SELECT Match.date, 
       Match.home_team_goal, Match.away_team_goal,
       home_team.team_long_name AS home_team, 
       away_team.team_long_name AS away_team
FROM Match
JOIN Team AS home_team
  ON Match.home_team_api_id=home_team.team_api_id
JOIN Team AS away_team
  ON Match.away_team_api_id=away_team.team_api_id
WHERE home_team=:home_team
ORDER BY Match.date ASC
"""
records = db.query(statement, home_team='KRC Genk')
records.fetch()[:20]
```




<table style="font-size:10pt; white-space:nowrap;">
<tr><th>date</th> <th>home_team_goal</th> <th>away_team_goal</th> <th>home_team</th> <th>away_team</th></tr>
<tr><td>2008-08-17 00:00:00</td> <td>1</td> <td>1</td> <td>KRC Genk</td> <td>Beerschot AC</td></tr>
<tr><td>2008-08-30 00:00:00</td> <td>1</td> <td>0</td> <td>KRC Genk</td> <td>Sporting Lokeren</td></tr>
<tr><td>2008-09-21 00:00:00</td> <td>0</td> <td>1</td> <td>KRC Genk</td> <td>Club Brugge KV</td></tr>
<tr><td>2008-10-04 00:00:00</td> <td>2</td> <td>1</td> <td>KRC Genk</td> <td>KV Mechelen</td></tr>
<tr><td>2008-10-26 00:00:00</td> <td>0</td> <td>0</td> <td>KRC Genk</td> <td>Standard de Liège</td></tr>
<tr><td>2008-11-15 00:00:00</td> <td>1</td> <td>1</td> <td>KRC Genk</td> <td>KSV Roeselare</td></tr>
<tr><td>2008-11-29 00:00:00</td> <td>3</td> <td>2</td> <td>KRC Genk</td> <td>KSV Cercle Brugge</td></tr>
<tr><td>2008-12-13 00:00:00</td> <td>1</td> <td>0</td> <td>KRC Genk</td> <td>Sporting Charleroi</td></tr>
<tr><td>2009-01-24 00:00:00</td> <td>2</td> <td>0</td> <td>KRC Genk</td> <td>RAEC Mons</td></tr>
<tr><td>2009-02-07 00:00:00</td> <td>1</td> <td>2</td> <td>KRC Genk</td> <td>SV Zulte-Waregem</td></tr>
<tr><td>2009-02-20 00:00:00</td> <td>1</td> <td>1</td> <td>KRC Genk</td> <td>Royal Excel Mouscron</td></tr>
<tr><td>2009-03-07 00:00:00</td> <td>4</td> <td>3</td> <td>KRC Genk</td> <td>FCV Dender EH</td></tr>
<tr><td>2009-03-21 00:00:00</td> <td>3</td> <td>0</td> <td>KRC Genk</td> <td>Tubize</td></tr>
<tr><td>2009-04-04 00:00:00</td> <td>1</td> <td>4</td> <td>KRC Genk</td> <td>KVC Westerlo</td></tr>
<tr><td>2009-04-17 00:00:00</td> <td>2</td> <td>2</td> <td>KRC Genk</td> <td>KAA Gent</td></tr>
<tr><td>2009-05-03 00:00:00</td> <td>0</td> <td>1</td> <td>KRC Genk</td> <td>KV Kortrijk</td></tr>
<tr><td>2009-05-16 00:00:00</td> <td>0</td> <td>2</td> <td>KRC Genk</td> <td>RSC Anderlecht</td></tr>
<tr><td>2009-08-15 00:00:00</td> <td>1</td> <td>1</td> <td>KRC Genk</td> <td>KAA Gent</td></tr>
<tr><td>2009-08-30 00:00:00</td> <td>1</td> <td>1</td> <td>KRC Genk</td> <td>Beerschot AC</td></tr>
<tr><td>2009-09-18 00:00:00</td> <td>1</td> <td>2</td> <td>KRC Genk</td> <td>Sporting Charleroi</td></tr>

</table>



## Exporting

You can export your records as a CSV file or a Pandas DataFrame.


```python
records.to_csv('KRC_Genk_games.csv')
```


```python
df = records.to_pandas()
df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>home_team_goal</th>
      <th>away_team_goal</th>
      <th>home_team</th>
      <th>away_team</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2008-08-17 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Beerschot AC</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2008-08-30 00:00:00</td>
      <td>1</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Sporting Lokeren</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2008-09-21 00:00:00</td>
      <td>0</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Club Brugge KV</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2008-10-04 00:00:00</td>
      <td>2</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KV Mechelen</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2008-10-26 00:00:00</td>
      <td>0</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Standard de Liège</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2008-11-15 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KSV Roeselare</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2008-11-29 00:00:00</td>
      <td>3</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>KSV Cercle Brugge</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2008-12-13 00:00:00</td>
      <td>1</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Sporting Charleroi</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2009-01-24 00:00:00</td>
      <td>2</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>RAEC Mons</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2009-02-07 00:00:00</td>
      <td>1</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>SV Zulte-Waregem</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2009-02-20 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Royal Excel Mouscron</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2009-03-07 00:00:00</td>
      <td>4</td>
      <td>3</td>
      <td>KRC Genk</td>
      <td>FCV Dender EH</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2009-03-21 00:00:00</td>
      <td>3</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Tubize</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2009-04-04 00:00:00</td>
      <td>1</td>
      <td>4</td>
      <td>KRC Genk</td>
      <td>KVC Westerlo</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2009-04-17 00:00:00</td>
      <td>2</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>KAA Gent</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2009-05-03 00:00:00</td>
      <td>0</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KV Kortrijk</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2009-05-16 00:00:00</td>
      <td>0</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>RSC Anderlecht</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2009-08-15 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KAA Gent</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2009-08-30 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Beerschot AC</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2009-09-18 00:00:00</td>
      <td>1</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>Sporting Charleroi</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2009-09-26 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KSV Roeselare</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2009-10-18 00:00:00</td>
      <td>1</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>KV Mechelen</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2009-11-02 00:00:00</td>
      <td>2</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>KSV Cercle Brugge</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2009-11-08 00:00:00</td>
      <td>0</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>RSC Anderlecht</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2009-12-05 00:00:00</td>
      <td>0</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>KVC Westerlo</td>
    </tr>
    <tr>
      <th>25</th>
      <td>2009-12-19 00:00:00</td>
      <td>2</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>SV Zulte-Waregem</td>
    </tr>
    <tr>
      <th>26</th>
      <td>2009-12-29 00:00:00</td>
      <td>0</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Sint-Truidense VV</td>
    </tr>
    <tr>
      <th>27</th>
      <td>2010-01-24 00:00:00</td>
      <td>2</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Club Brugge KV</td>
    </tr>
    <tr>
      <th>28</th>
      <td>2010-02-07 00:00:00</td>
      <td>1</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Standard de Liège</td>
    </tr>
    <tr>
      <th>29</th>
      <td>2010-02-19 00:00:00</td>
      <td>3</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Sporting Lokeren</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>76</th>
      <td>2014-08-02 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KSV Cercle Brugge</td>
    </tr>
    <tr>
      <th>77</th>
      <td>2014-08-08 00:00:00</td>
      <td>0</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Sporting Lokeren</td>
    </tr>
    <tr>
      <th>78</th>
      <td>2014-08-22 00:00:00</td>
      <td>3</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>KAA Gent</td>
    </tr>
    <tr>
      <th>79</th>
      <td>2014-09-14 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Club Brugge KV</td>
    </tr>
    <tr>
      <th>80</th>
      <td>2014-09-27 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Sporting Charleroi</td>
    </tr>
    <tr>
      <th>81</th>
      <td>2014-10-19 00:00:00</td>
      <td>3</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KVC Westerlo</td>
    </tr>
    <tr>
      <th>82</th>
      <td>2014-10-28 00:00:00</td>
      <td>3</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Lierse SK</td>
    </tr>
    <tr>
      <th>83</th>
      <td>2014-11-09 00:00:00</td>
      <td>0</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>Standard de Liège</td>
    </tr>
    <tr>
      <th>84</th>
      <td>2014-11-23 00:00:00</td>
      <td>3</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>KV Mechelen</td>
    </tr>
    <tr>
      <th>85</th>
      <td>2014-12-13 00:00:00</td>
      <td>3</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>KV Kortrijk</td>
    </tr>
    <tr>
      <th>86</th>
      <td>2015-01-23 00:00:00</td>
      <td>2</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Royal Excel Mouscron</td>
    </tr>
    <tr>
      <th>87</th>
      <td>2015-02-03 00:00:00</td>
      <td>1</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KV Oostende</td>
    </tr>
    <tr>
      <th>88</th>
      <td>2015-02-08 00:00:00</td>
      <td>1</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Waasland-Beveren</td>
    </tr>
    <tr>
      <th>89</th>
      <td>2015-02-22 00:00:00</td>
      <td>0</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>RSC Anderlecht</td>
    </tr>
    <tr>
      <th>90</th>
      <td>2015-03-07 00:00:00</td>
      <td>3</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>SV Zulte-Waregem</td>
    </tr>
    <tr>
      <th>91</th>
      <td>2015-07-25 00:00:00</td>
      <td>3</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Oud-Heverlee Leuven</td>
    </tr>
    <tr>
      <th>92</th>
      <td>2015-08-15 00:00:00</td>
      <td>2</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KVC Westerlo</td>
    </tr>
    <tr>
      <th>93</th>
      <td>2015-08-28 00:00:00</td>
      <td>2</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Sporting Charleroi</td>
    </tr>
    <tr>
      <th>94</th>
      <td>2015-09-18 00:00:00</td>
      <td>3</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KV Mechelen</td>
    </tr>
    <tr>
      <th>95</th>
      <td>2015-10-04 00:00:00</td>
      <td>3</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Standard de Liège</td>
    </tr>
    <tr>
      <th>96</th>
      <td>2015-10-23 00:00:00</td>
      <td>0</td>
      <td>4</td>
      <td>KRC Genk</td>
      <td>Royal Excel Mouscron</td>
    </tr>
    <tr>
      <th>97</th>
      <td>2015-10-30 00:00:00</td>
      <td>0</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>Sporting Lokeren</td>
    </tr>
    <tr>
      <th>98</th>
      <td>2015-11-28 00:00:00</td>
      <td>0</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KAA Gent</td>
    </tr>
    <tr>
      <th>99</th>
      <td>2015-12-06 00:00:00</td>
      <td>0</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>RSC Anderlecht</td>
    </tr>
    <tr>
      <th>100</th>
      <td>2015-12-19 00:00:00</td>
      <td>3</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>Sint-Truidense VV</td>
    </tr>
    <tr>
      <th>101</th>
      <td>2016-01-15 00:00:00</td>
      <td>2</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>SV Zulte-Waregem</td>
    </tr>
    <tr>
      <th>102</th>
      <td>2016-01-30 00:00:00</td>
      <td>1</td>
      <td>0</td>
      <td>KRC Genk</td>
      <td>KV Kortrijk</td>
    </tr>
    <tr>
      <th>103</th>
      <td>2016-02-13 00:00:00</td>
      <td>6</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>Waasland-Beveren</td>
    </tr>
    <tr>
      <th>104</th>
      <td>2016-02-28 00:00:00</td>
      <td>3</td>
      <td>2</td>
      <td>KRC Genk</td>
      <td>Club Brugge KV</td>
    </tr>
    <tr>
      <th>105</th>
      <td>2016-03-13 00:00:00</td>
      <td>4</td>
      <td>1</td>
      <td>KRC Genk</td>
      <td>KV Oostende</td>
    </tr>
  </tbody>
</table>
<p>106 rows × 5 columns</p>
</div>




```python
df = df.assign(point_diff=(df['home_team_goal'] - df['away_team_goal']))
df.groupby('away_team')['point_diff'].agg({'wins': lambda x: sum(x>0),
                                           'losses': lambda x: sum(x<0),
                                           'ties': lambda x: sum(x==0)})
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>wins</th>
      <th>losses</th>
      <th>ties</th>
    </tr>
    <tr>
      <th>away_team</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Beerschot AC</th>
      <td>3</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Club Brugge KV</th>
      <td>5</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>FCV Dender EH</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>KAA Gent</th>
      <td>3</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>KAS Eupen</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>KSV Cercle Brugge</th>
      <td>4</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>KSV Roeselare</th>
      <td>0</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>KV Kortrijk</th>
      <td>4</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>KV Mechelen</th>
      <td>5</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>KV Oostende</th>
      <td>1</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>KVC Westerlo</th>
      <td>3</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Lierse SK</th>
      <td>4</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Oud-Heverlee Leuven</th>
      <td>2</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>RAEC Mons</th>
      <td>3</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>RSC Anderlecht</th>
      <td>0</td>
      <td>6</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Royal Excel Mouscron</th>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>SV Zulte-Waregem</th>
      <td>4</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Sint-Truidense VV</th>
      <td>2</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>Sporting Charleroi</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Sporting Lokeren</th>
      <td>4</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Standard de Liège</th>
      <td>4</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>Tubize</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Waasland-Beveren</th>
      <td>2</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>


