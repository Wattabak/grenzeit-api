# Some notes on the data model of the Grenzeit graph database


## Key points

1. Show how the borders of our countries changed over the history of humanity
2. For every point in existance of a certain country, allow to show data related to this country, for example population and composition of that population across the country
3. Provide a simple way of sourcing the information represented on grenzeit. For example the population data of certain countries, where does that information come from, what is the source (approximation or not, author of the dataset, basis etc.)

Basic model of each country show probably only include basic things, like date of foundation, dissolution, 


```
create (russianEmpire:Country {founded: DATE('1721-11-02'), dissolved: DATE('1917-03-15'), dissolution_reason: 'Abdication of Tsar Nicholas 2', name_RU: 'Российская империя', name_ZEIT: '', name_EN: 'Russian Empire', id: 1})
create (sovietUnion:Country {founded: DATE('1922-12-30'), dissolved: DATE('1991-01-01'), dissolution_reason: 'Revolution', name_RU: 'СССР', id: 2, name_EN: 'USSR', name_ZEIT: 'Союз Советских Социалистических республик'})
create (russianEmpirePop:Population {date_census: DATETIME('1897'), total: 125640021, by_language: [{lang: 'Russian', val: 55667469, percent: '	44.31'}], by_religion:[], by_political_affiliation: [], by_gender: [], by_})
create (russianEmpirePopSource:Source {name: 'wikipedia', permalink: 'https://archive.org/wikipedia.org/some_url', link: 'wikipedia.org/some_source_url', source_type: 'internet resource/wikipedia'})
```