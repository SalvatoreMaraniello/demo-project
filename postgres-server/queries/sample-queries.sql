-- reminder window functions
SELECT 
	p.*,
	row_number() over w_age as rno
FROM public.sample as p
WINDOW w_age AS (PARTITION BY p.name ORDER BY p.age DESC)
order by rno
limit 50;

-- percentiles and median
select 
	p.name, 
	percentile_cont(.5) within group (order by p.age asc) as perc50_age
from public.sample as p
group by p.name