
application requirements
1)it is assumed that python and pip is installed in the system. Else pl install it.
2)the entire aplication code is in one script [wamp.py] which will be part of the deliverable.
3)There are some packages that the application depends. pandas,matplotlib and sqlite3.
4)We have tested this application in windows only. 
---------------------------------------------------------------------
instructions to run the application.

1)unzip the contents in the folder into any directory.
2)move the sqlite folder [from inside the deliverables folder] into directly under C Drive.
  After this you should see a folder structure c:/sqlite/databases
3)run the below pip statements:

pip install pandas
pip install matplotlib
pip install sqlite3


4)run wamp.py script.

optional:
if you want to query the database, suggest download sqlitestudio.exe from https://sqlitestudio.pl/index.rvt?act=download .
To use sqlite in command line, edit environment path variable and add C:\sqlite.


note: expand the screen to max to get best results.

below are the queries used.
chart1 query:::
select fyear as Year,round(SUM(income_amount) + SUM(refund_amount),1) as NetAmount from transactions group by fyear

chart2 query:::
SELECT fyear, perf_code, SUM(income_amount) + SUM(refund_amount) AS NetAmount FROM transactions  GROUP BY fyear, perf_code

chart3 query:::
SELECT fyear, price_category, round(SUM(income_amount) + SUM(refund_amount),0) AS Net_Income FROM transactions GROUP BY fyear, price_category

chart4 query:::
SELECT fyear, price_type, round(SUM(income_amount) + SUM(refund_amount),0) AS Net_Income FROM transactions GROUP BY fyear, price_type having round(SUM(income_amount) + SUM(refund_amount),0) > 50000
