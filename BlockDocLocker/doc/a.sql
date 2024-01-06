with cte as accountid,  weights from account_items a,  items i where a.itemid = i.itemid,
select accountids, sum(weights) from cte inner join cte using(accoundids) group by accountids