1.
Any time you use an aggregate function (SUM, COUNT) alongside a non-aggregated column (a.name), you need GROUP BY a.name (or a.id)
SELECT a.name, SUM(t.amount)
FROM accounts a
INNER JOIN transactions t ON a.id = b.id
GROUP BY a.name
HAVING COUNT(t.id) > 5

2.
Inner join (only keep match) vs left join (keep everything frmo the left - make it null for right if not match but still include stuff from left) 

3. 

4. Aggregate is used wrong because if you use aggreegate you must have GROUP BY
SELECT a.name, a.balance 
FROM accounts a
JOIN transactions t ON a.id = t.account_id
GROUP BY a.name, a.balance
HAVING COUNT(t.id) > 5;

// GROUP BY
// no group by
transactions:
id | account_id | amount
1  | 42         | 100
2  | 42         | 200
3  | 55         | 300
4  | 55         | 50

SELECT SUM(amount) FROM transactions;
=> Whole table in 1 which is 650

// Add group By you can split it into unique stuff

SELECT account_id, SUM(amount) 
FROM transactions
GROUP BY account_id; => In this case unique account id not each row = 1 thing anymore

// Now the rows get bucketed by account_id first, then summed within each bucket:
account_id | SUM(amount)
42         | 300
55         | 350

// Every column in your SELECT list must either be: IMPORTANTTTTTTTTTTTTT
1. In the GROUP BY clause, or
2. Wrapped in an aggregate function (SUM, COUNT, etc.)

// You also CANNOT use Agreegation in WHERE becuase it run before any grouping/aggregating happens

-- WRONG — name isn't grouped, and isn't aggregated
SELECT a.name, a.balance, SUM(t.amount)
FROM accounts a JOIN transactions t ON a.id = t.account_id
GROUP BY a.name; <- need to add a.balance to this for it to work!!!
=> MUST group by everything in SELECT except the thing in the agreegation function
because without it it doesnt know how to show the balance


SELECT account_id, SUM(amount) AS total
FROM transactions
WHERE amount > 0                -- filters individual ROWS, before grouping
GROUP BY account_id
HAVING SUM(amount) > 100;       -- filters GROUPS, after aggregating

// Quiz //

SELECT a.name, AVG(t.amount) AS avg_t
FROM accounts a INNER JOIN transactions t ON a.id = t.id
WHERE t.amount > 0
GROUP BY a.name
HAVING AVG(t.amount) > 100

///// Subqueries — a SELECT inside another SELECT
Sometimes you need the result of one query before you can even write the query you actually want. A subquery is just wrapping a SELECT in parentheses and using it as if it were a single value or a table.
subquery as a single value, used in WHERE

SELECT name, balance
FROM accounts
WHERE balance > (SELECT AVG(balance) FROM accounts);

// the innermost parentheses run first, produce a result, and that result gets substituted into the outer query

// Subquery in WHERE with a list — using IN:
SELECT name FROM accounts
WHERE id IN (SELECT account_id FROM transactions WHERE amount > 1000);

so just the the id in the accounts table that have a transaction with an amount greater than 1000

// Also WHERE can also used with IN 
SELECT name FROM accounts WHERE id IN (42, 55, 61);

// Subquery in FROM — treating a query's' result as if it were a table:
SELECT account_id, total
FROM (
  SELECT account_id, SUM(amount) AS total
  FROM transactions
  GROUP BY account_id
) AS account_totals
WHERE total > 500;

// The actual locations a subquery can live:
1. In WHERE (or HAVING) — used to filter rows, comparing against either a single value or a list
2. In FROM — used to treat a query's' result as if it were a table you can select/filter/join from


///////// WINDOW functions => OVER ()
GROUP BY collapses many rows into one row per group — you lose the individual rows, 
only the aggregated result survives. 

Window functions do a similar calculation, but keep every original row intact
they just add an extra calculated column alongside each row.

GROUP BY: many rows in → fewer rows out (one per group)
Window function: many rows in → same number of rows out (just an extra column added)

Example:
transactions:
id | account_id | amount
1  | 42         | 100
2  | 42         | 300
3  | 55         | 200
4  | 55         | 50

SELECT id, account_id, amount, 
       SUM(amount) OVER () AS total_all_transactions
FROM transactions;

1. 
OVER () is what makes this a window function instead of a normal aggregate. 
Result:
id | account_id | amount | total_all_transactions
1  | 42         | 100    | 650
2  | 42         | 300    | 650
3  | 55         | 200    | 650
4  | 55         | 50     | 650

// PARTITION BY — the part that makes it actually useful
PARTITION BY says "don't calculate across the whole table — reset the calculation separately for each group, but still keep every row."

SELECT id, account_id, amount, 
       SUM(amount) OVER (PARTITION BY account_id) AS total_for_this_account
FROM transactions;

kinda like the group by of WINDOW

id | account_id | amount | total_for_this_account
1  | 42         | 100    | 400
2  | 42         | 300    | 400
3  | 55         | 200    | 250
4  | 55         | 50     | 250

2. RANK() — ordering within each partition
SELECT id, account_id, amount,
       RANK() OVER (PARTITION BY account_id ORDER BY amount DESC) AS rank_in_account
FROM transactions;

// The realistic use case — "most recent transaction per account"
SELECT * FROM (
  SELECT id, account_id, amount, transaction_date,
         RANK() OVER (PARTITION BY account_id ORDER BY transaction_date DESC) AS rn
  FROM transactions
) ranked
WHERE rn = 1;

Rank each account's' transactions by date, most recent = rank 1, 
then wrap it in a subquery (theres your subquery skill applying immediately) 
and filter down to just rank 1 — giving you exactly one row per account, their latest transaction.