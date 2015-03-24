
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
    	},
	{#5, most interesting user
      "name": "Frank",
	    "salary": {
		"bad_low": 0,
		"bad_high": 30,
		"ok_low": 60,
		"ok_high": 70,
		"good_low": 100,
		"good_high": 130
	    },
	    "employees": {
		"small_low": 5,
		"small_high": 50,
		"med_low": 100,
		"med_high": 300,
		"large_low": 500,
		"large_high": 1000
	    },
	    "rep": {
		"low": 3.5,
		"high": 7.7
	    },
      "commute": {
        "close": 5,
        "medium": 30,
        "far": 60
      },
	    "expected":"myPod"
    	},
	{#6
      "name": "Sam",
	    "salary": {
		"bad_low": 10,
		"bad_high": 25,
		"ok_low": 50,
		"ok_high": 60,
		"good_low": 70,
		"good_high": 130
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 50,
		"med_low": 65,
		"med_high": 120,
		"large_low": 200,
		"large_high": 1000
	    },
	    "rep": {
		"low": 5,
		"high": 7.8
	    },
      "commute": {
        "close": 10,
        "medium": 40,
        "far": 90
      },
	    "expected":"Masterminds"
    	},
	{#8
      "name": "Garrett",
	    "salary": {
		"bad_low": 40,
		"bad_high": 50,
		"ok_low": 75,
		"ok_high": 90,
		"good_low": 100,
		"good_high": 200
	    },
	    "employees": {
		"small_low": 1,
		"small_high": 10,
		"med_low": 30,
		"med_high": 42,
		"large_low": 101,
		"large_high": 1000
	    },
	    "rep": {
		"low": 6,
		"high": 8
	    },
      "commute": {
        "close": 3,
        "medium": 25,
        "far": 60
      },
	    "expected":"myPod"
    	},
	{#9
      "name": "RandomGuy",
	    "salary": {
		"bad_low": 60,
		"bad_high": 70,
		"ok_low": 90,
		"ok_high": 120,
		"good_low": 160,
		"good_high": 200
	    },
	    "employees": {
		"small_low": 30,
		"small_high": 50,
		"med_low": 80,
		"med_high": 300,
		"large_low": 500,
		"large_high": 1000
	    },
	    "rep": {
		"low": 2,
		"high": 6
	    },
      "commute": {
        "close": 50,
        "medium": 90,
        "far": 120
      },
	    "expected":"Smith Consulting"
    	}]


def getEmployeeData():
    return users
