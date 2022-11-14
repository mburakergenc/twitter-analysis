# Part I

1. The sql query below retreives the current user information

   ```
   SELECT t1.user_id, t1.name, t1.email

   from user_changes AS t1

   LEFT  OUTER  JOIN user_changes AS t2

   ON t1.user_id = t2.user_id

   AND(t1.created < t2.created

   OR (t1.created = t2.created AND t1.user_id < t2.user_id))

   WHERE t2.email is  NULL
   ```

2. Find the median time between the second and third profile edit.

   ```
   with edit_diff as
   (
     select timestampdiff(hour, min(created), max(created)) difference
     from
     (
       select *,
         row_number() over (partition by user_id order by created) rn
       from users_changes
     ) T
     where rn in(2,3)
     group by user_id
   )

   select round(avg(difference), 2) median
   from
   (
     select difference,
            row_number() over (order by difference) diffOrder,
           count(*) over () cn
     from edit_diff
   ) T
   where diffOrder between floor((cn + 1) / 2) and ceil((cn + 1) / 2);
   ```

# Part II

## How to run the application

- Have Docker installed on your system
- If you don't have docker installed, you can run the src/assignment/handler.py file after filling the src/assignment/credentials.py file with your credentials.
- Run the command below to pull the docker image;
  - `docker pull mburakergenc/kahootassignment`
- Run the command below to run the container;
  - `docker run -ti mburakergenc/kahootassignment`
- Enter a search term when requested by the application such as "Donald"
- Please try to select a high volume keyword to see all the details analysis. You'll get warnings printed when the keyword doesn't have any tweets within the last 1, 5, 60 minutes.
- Results are limited to **500 tweets** for performance reasons. It should take a few seconds for 500 tweets to be loaded from Twitter.

## How to run the tests

- cd into the project directory
  - `cd twitter-analysis`
- `py.test`
