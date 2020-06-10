# Gym Scheduler <br>

Python paackage which uses scrapy to access gym website and book classes on behalf of user. <br>

Current setup works by specifying the classes user wants from timetable as an option in the code. The package user form request from scrappy to login to the user account and access the available classes. <br>

The gym only allows booking 72 hours in advance so a CRON job can then be run at this time to ensure the classes are booked well in advance.<br>


