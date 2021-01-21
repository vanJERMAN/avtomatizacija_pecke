import sched

TIME = [('24.12.2020', '10:54:44', 'abc.php?xxx'),
    ('24.12.2020', '10:55:31', 'abc.php?yyy'),
    ('24.12.2020', '10:56:04', 'abc.php?zzz'),
    ('24.12.2020', '10:57:23', 'abc.php?www')]

def job():
    global TIME
    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    date = rtc.datetime()
    pravilen_cas = "{}.{}.{} {}:{}:{}".format(date[2], date[1], date[0], date[4], date[5], date[6])
    for i in TIME:
        runTime = i[0] + " " + i[1]
        if i and date == str(runTime):
            request.get(str(i[2]))

sched.every(0.01).minutes.do(job)

while True:
    sched.run_pending()
    time.sleep(1)