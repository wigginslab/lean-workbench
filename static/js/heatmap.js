
	// standard gmaps init
		var myLatlng = new google.maps.LatLng(48.3333, 16.35);
		// define map properties
		var myOptions = {
			zoom: 3,
		  center: myLatlng,
		  mapTypeId: google.maps.MapTypeId.ROADMAP,
		  disableDefaultUI: false,
		  scrollwheel: true,
		  draggable: true,
		  navigationControl: true,
		  mapTypeControl: false,
		  scaleControl: true,
		  disableDoubleClickZoom: false
		};

		var map = new google.maps.Map($("#heatmapArea")[0], myOptions);

		var heatmap = new HeatmapOverlay(map, {
			"radius":20,
			"visible": true,
			"opacity":60
		});

		//dataset
		
		var testData = {
			max: 46,
			data: [{lat: 33.5363, lng:-117.044, count: 1},{lat: 33.5608, lng:-117.24, count: 1},{lat: 38, lng:-97, count: 1},{lat: 38.9358, lng:-77.1621, count: 1}]
		};

		// set the data
		google.maps.event.addListenerOnce(map, "idle", function(){
			heatmap.setDataSet(testData);
		});
