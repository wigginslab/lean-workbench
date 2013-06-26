

	//instantiate leanTracker as object
	var LeanTracker = Object();

	// ajax POST requests
	LeanTracker.send = function(){
		xmlhttp.open("POST","http://localhost:8000/leantracker",true);
		xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		xmlhttp.send("arguments="+arguments);
	}

	LeanTracker.emitEvent = function(){
		// get function arguments
		console.log(arguments);

	}
