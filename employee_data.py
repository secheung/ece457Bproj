
users = [{#0
	    "salary": {
		"bad_low": 0,
		"bad_high": 10,
		"ok_low": 30,
		"ok_high": 50,
		"good_low": 90,
		"good_high": 100
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 20,
		"med_low": 35,
		"med_high": 40,
		"large_low": 50,
		"large_high": 100
	    },
	    "rep": {
		"low": 3,
		"high": 4
	    },
	    "expected":"Acme Inc"
    	},
	{#1
	    "salary": {
		"bad_low": 25,
		"bad_high": 35,
		"ok_low": 40,
		"ok_high": 50,
		"good_low": 75,
		"good_high": 100
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 20,
		"med_low": 50,
		"med_high": 100,
		"large_low": 200,
		"large_high": 500
	    },
	    "rep": {
		"low": 3,
		"high": 8
	    },
	    "expected":"Acme Inc"
    	},
	{#2
	    "salary": {
		"bad_low": 25,
		"bad_high": 35,
		"ok_low": 40,
		"ok_high": 50,
		"good_low": 75,
		"good_high": 100
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 20,
		"med_low": 50,
		"med_high": 100,
		"large_low": 200,
		"large_high": 500
	    },
	    "rep": {
		"low": 2,
		"high": 8
	    },
	    "expected":"Smith Consulting"
    	},
	{#3
	    "salary": {
		"bad_low": 30,
		"bad_high": 35,
		"ok_low": 55,
		"ok_high": 60,
		"good_low": 75,
		"good_high": 100
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 35,
		"med_low": 40,
		"med_high": 60,
		"large_low": 200,
		"large_high": 500
	    },
	    "rep": {
		"low": 5,
		"high": 7
	    },
	    "expected":"myPod"
    	},
	{#4
	    "salary": {
		"bad_low": 40,
		"bad_high": 50,
		"ok_low": 55,
		"ok_high": 65,
		"good_low": 80,
		"good_high": 120
	    },
	    "employees": {
		"small_low": 5,
		"small_high": 35,
		"med_low": 120,
		"med_high": 200,
		"large_low": 210,
		"large_high": 1000
	    },
	    "rep": {
		"low": 4.3,
		"high": 8.5
	    },
	    "expected":"myPod"
    	}]


def getEmployeeData():
    return users
