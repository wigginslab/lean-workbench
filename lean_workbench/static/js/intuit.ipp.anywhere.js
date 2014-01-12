--if (typeof intuit === 'undefined' || !intuit) {
	intuit = {}; // since intuit is in global scope and because of a bug in IE we don't do a 'var intuit'.
}

if (!intuit.ipp) {
	intuit.ipp = {};
}

if (!intuit.ipp.anywhere) {
	intuit.ipp.anywhere = {};
}

intuit.ipp.anywhere = {
	version : '1.2.1',
	tags	: ['connectToIntuit', 'blueDot', 'login'],
	tagPrefix : 'ipp',
	ready: false,
	developerGaTrackerInitiated: false,
	directAlreadyCalled: false,
	windowLoad	: function() {
		intuit.ipp.jQuery(document).ready(function () {
			intuit.ipp.jQuery('script').each(function (){
				// check if this script file is from our domain
				//if (!this.src) {
			//		return;
			//	}
			/*	var jsSrc = this.src;
				var jsSrcParts = jsSrc.replace(/http[s]?:\/\//, '').split('/');
				var qs = intuit.ipp.ourDomain.exec(jsSrcParts[0]);
				if(!qs) {
					qs = document.domain.match(intuit.ipp.ourDomain);
				}
				if (!qs || !jsSrcParts[jsSrcParts.length - 1].match('intuit.ipp.anywhere') || !jsSrc.match(/:\/\/(.[^/]+)/)) {
					return;
				} */
				// get ipp's domain
				intuit.ipp.anywhere.serviceHost = jsSrc.match(/:\/\/(.[^/]+)/)[1];
				intuit.ipp.jQuery('head').append("<link rel='stylesheet' href='https://" + intuit.ipp.anywhere.serviceHost + "/Content/IA/intuit.ipp.anywhere.css' type='text/css' media='all' />");
				intuit.ipp.jQuery('head').append("<!--[if IE 7]><style type='text/css'>.intuitPlatformConnectButton, .intuitPlatformReconnectButton, .intuitPlatformLoginButtonVertical, .intuitPlatformLoginButtonHorizontal, .intuitPlatformLoginButtonLogo { font-size:0; text-indent: 0; line-height: 0; overflow: hidden; }</style><![endif]-->");
				if(intuit.ipp.anywhere.serviceHost.match(/^([a-zA-Z]+\.)?appcenter.intuit.com$/) || intuit.ipp.anywhere.serviceHost.match(/workplace.intuit.com$/)) {
					intuit.ipp.anywhere.serviceHost = "appcenter.intuit.com";
				}
				intuit.ipp.anywhere.ready = true;
				if(intuit.ipp.anywhere.directAlreadyCalled) {
					intuit.ipp.anywhere.directConnectToIntuit();
				}
				intuit.ipp.anywhere.init(jsSrc);
				return false;
			});
		});
	},
	init	: function(srcFile) {
		// load the tiny scroll plugin
		(function($){$.tiny=$.tiny||{};$.tiny.scrollbar={options:{axis:'y',wheel:40,scroll:true,size:'auto',sizethumb:'auto'}};$.fn.tinyscrollbar=function(options){var options=$.extend({},$.tiny.scrollbar.options,options);this.each(function(){$(this).data('tsb',new Scrollbar($(this),options));});return this;};$.fn.tinyscrollbar_update=function(sScroll){return $(this).data('tsb').update(sScroll);};function Scrollbar(root,options){var oSelf=this;var oWrapper=root;var oViewport={obj:$('.intuitPlatformAppMenuDropdownAppsListScrollViewport',root)};var oContent={obj:$('.intuitPlatformAppMenuDropdownAppsListScrollOverview',root)};var oScrollbar={obj:$('.intuitPlatformAppMenuDropdownAppsListScrollbar',root)};var oTrack={obj:$('.intuitPlatformAppMenuDropdownAppsListScrollTrack',oScrollbar.obj)};var oThumb={obj:$('.intuitPlatformAppMenuDropdownAppsListScrollThumb',oScrollbar.obj)};var sAxis=options.axis=='x',sDirection=sAxis?'left':'top',sSize=sAxis?'Width':'Height';var iScroll,iPosition={start:0,now:0},iMouse={};function initialize(){oSelf.update();setEvents();return oSelf;}
this.update=function(sScroll){oViewport[options.axis]=oViewport.obj[0]['offset'+sSize];oContent[options.axis]=oContent.obj[0]['scroll'+sSize];oContent.ratio=oViewport[options.axis]/oContent[options.axis];oScrollbar.obj.toggleClass('intuitPlatformAppMenuDropdownAppsListScrollDisable',oContent.ratio>=1);oTrack[options.axis]=options.size=='auto'?oViewport[options.axis]:options.size;oThumb[options.axis]=Math.min(oTrack[options.axis],Math.max(0,(options.sizethumb=='auto'?(oTrack[options.axis]*oContent.ratio):options.sizethumb)));oScrollbar.ratio=options.sizethumb=='auto'?(oContent[options.axis]/oTrack[options.axis]):(oContent[options.axis]-oViewport[options.axis])/(oTrack[options.axis]-oThumb[options.axis]);iScroll=(sScroll=='relative'&&oContent.ratio<=1)?Math.min((oContent[options.axis]-oViewport[options.axis]),Math.max(0,iScroll)):0;iScroll=(sScroll=='bottom'&&oContent.ratio<=1)?(oContent[options.axis]-oViewport[options.axis]):isNaN(parseInt(sScroll))?iScroll:parseInt(sScroll);setSize();};function setSize(){oThumb.obj.css(sDirection,iScroll/oScrollbar.ratio);oContent.obj.css(sDirection,-iScroll);iMouse['start']=oThumb.obj.offset()[sDirection];var sCssSize=sSize.toLowerCase();oScrollbar.obj.css(sCssSize,oTrack[options.axis]);oTrack.obj.css(sCssSize,oTrack[options.axis]);oThumb.obj.css(sCssSize,oThumb[options.axis]);};function setEvents(){oThumb.obj.bind('mousedown',start);oThumb.obj[0].ontouchstart=function(oEvent){oEvent.preventDefault();oThumb.obj.unbind('mousedown');start(oEvent.touches[0]);return false;};oTrack.obj.bind('mouseup',drag);if(options.scroll&&this.addEventListener){oWrapper[0].addEventListener('DOMMouseScroll',wheel,false);oWrapper[0].addEventListener('mousewheel',wheel,false);}
else if(options.scroll){oWrapper[0].onmousewheel=wheel;}};function start(oEvent){iMouse.start=sAxis?oEvent.pageX:oEvent.pageY;var oThumbDir=parseInt(oThumb.obj.css(sDirection));iPosition.start=oThumbDir=='auto'?0:oThumbDir;$(document).bind('mousemove',drag);document.ontouchmove=function(oEvent){$(document).unbind('mousemove');drag(oEvent.touches[0]);};$(document).bind('mouseup',end);oThumb.obj.bind('mouseup',end);oThumb.obj[0].ontouchend=document.ontouchend=function(oEvent){$(document).unbind('mouseup');oThumb.obj.unbind('mouseup');end(oEvent.touches[0]);};return false;};function wheel(oEvent){if(!(oContent.ratio>=1)){oEvent=$.event.fix(oEvent||window.event);var iDelta=oEvent.wheelDelta?oEvent.wheelDelta/120:-oEvent.detail/3;iScroll-=iDelta*options.wheel;iScroll=Math.min((oContent[options.axis]-oViewport[options.axis]),Math.max(0,iScroll));oThumb.obj.css(sDirection,iScroll/oScrollbar.ratio);oContent.obj.css(sDirection,-iScroll);oEvent.preventDefault();};};function end(oEvent){$(document).unbind('mousemove',drag);$(document).unbind('mouseup',end);oThumb.obj.unbind('mouseup',end);document.ontouchmove=oThumb.obj[0].ontouchend=document.ontouchend=null;return false;};function drag(oEvent){if(!(oContent.ratio>=1)){iPosition.now=Math.min((oTrack[options.axis]-oThumb[options.axis]),Math.max(0,(iPosition.start+((sAxis?oEvent.pageX:oEvent.pageY)-iMouse.start))));iScroll=iPosition.now*oScrollbar.ratio;oContent.obj.css(sDirection,-iScroll);oThumb.obj.css(sDirection,iPosition.now);}
return false;};return initialize();};})(intuit.ipp.jQuery);
		// find all elements with the tag 'tagPrefix:tag'
		//alert(document.createElement("ipp:connectToIntuit"));
		intuit.ipp.jQuery.each(this.tags, function(index, value) {
			// for each tag of this type
			if (navigator.appVersion.indexOf("MSIE") != -1 && (parseFloat(navigator.appVersion.split("MSIE")[1]) <= 7 || document.documentMode <= 7)) {
				var tags = intuit.ipp.jQuery(value);
			} else {
				var tags = intuit.ipp.jQuery(intuit.ipp.anywhere.tagPrefix + '\\:' + value);
			}
			tags.each( function() {
				if (value == 'connectToIntuit') {
					intuit.ipp.anywhere.controller.connectToIntuit.execute(this);
				} else if (value == 'blueDot') {
					intuit.ipp.anywhere.controller.blueDot.execute(this);
				} else if (value == 'login') {
					intuit.ipp.anywhere.controller.login.execute(this);
				}
			});
		});
	},
	setup	: function(opts) {
		if(opts == null) {
			opts = {}
		}
		intuit.ipp.anywhere.menuProxy = opts.menuProxy;
		intuit.ipp.anywhere.developerGaTrackerId = opts.gaTrackerId;
		intuit.ipp.anywhere.grantUrl = opts.grantUrl;
	},
	directConnectToIntuit : function() {
		if(!intuit.ipp.anywhere.ready) {
			intuit.ipp.anywhere.directAlreadyCalled = true;
		} else {
			return intuit.ipp.anywhere.controller.directConnectToIntuit();
		}
	},
	
	logout: function (callback) {
	    intuit.ipp.jQuery.ajax({
					url: "https://" + intuit.ipp.anywhere.serviceHost + "/Account/LogoutJSONP?callback=?",
					dataType: "jsonp",
					complete: function () {
						callback();
						//intuit.ipp.anywhere.view.popup.hide();
					}
				});
		//intuit.ipp.anywhere.view.logout.render(callback);
		return false;
	},
	
	connected: function (opts) {
		intuit.ipp.anywhere.view.connected.render(opts);
		return false;
	}	
};

// CONTROLLER
intuit.ipp.anywhere.controller = {
	connectToIntuit : {
		name : 'connectToIntuit',
		execute : function(elem){
			var view = intuit.ipp.anywhere.view.connectToIntuit;
			var model = intuit.ipp.anywhere.model;
			view.render(elem);
		}
	},

	onConnectToIntuitClicked : function(elem){
		if(intuit.ipp.anywhere.grantUrl) {
			intuit.ipp.anywhere.tracking.trackEvent("ConnectButton", "Connect", "ConnectWithQuickbooks", "click");
			intuit.ipp.anywhere.service.openExternalPopupWindow({
				url: "https://"+intuit.ipp.anywhere.serviceHost+"/Connect/SessionStart?grantUrl="+encodeURIComponent(intuit.ipp.anywhere.grantUrl),
				centered: true
			});
		} else {
			if(console && console.log) {
				// console.log("Missing GrantURL parameter");
				console.log("Missing grantUrl in setup function");
			}
		}
	},
	
    onSignInWithIntuitClicked : function(elem){
        intuit.ipp.anywhere.tracking.trackEventSync("SignInWithIntuitButton", "SignIn", "SignInWithIntuit", "click");
    },

	directConnectToIntuit : function(){
		if(intuit.ipp.anywhere.grantUrl) {
			window.location = "https://"+intuit.ipp.anywhere.serviceHost+"/Connect/SessionStart?grantUrl="+encodeURIComponent(intuit.ipp.anywhere.grantUrl);
		} else {
			if(console && console.log) {
				// console.log("Missing GrantURL parameter");
				console.log("Missing grantUrl in setup function");
			}
		}
	},

	blueDot : {
		name : 'blueDot',
		execute : function(elem) {
			var view = intuit.ipp.anywhere.view.blueDot;
			var model = intuit.ipp.anywhere.model;
			
			view.render(elem);
			
			// find out if we need to show the intro message
			var showIntroMessage = true;
			// if the intuit.ipp.anywhere.introMessageShown cookie is present, don't need to show the intro message
			var cookiesArray = document.cookie.split(";");
			for (i = 0;i < cookiesArray.length;i++) {
				var x = cookiesArray[i].substr(0,cookiesArray[i].indexOf("="));
				var y =  cookiesArray[i].substr(cookiesArray[i].indexOf("=")+1);
				x = x.replace(/^\s+|\s+$/g,"");
				if (x == "intuit.ipp.anywhere.introMessageShown") {
					showIntroMessage = false;
				}
			}
			
			if (!showIntroMessage) {
				return;
			}
			
			intuit.ipp.jQuery.ajax({
				url: "https://" + intuit.ipp.anywhere.serviceHost + "/Connect/ShowIntroMessageJSONP?callback=?",
				dataType: "jsonp",
				success: function (response) {
					// create the intuit.ipp.anywhere.introMessageShown cookie with session expiry
					document.cookie = "intuit.ipp.anywhere.introMessageShown=true";
					 if (response.ErrorCode == '0'){ // means we should show the intro message
						intuit.ipp.anywhere.controller.introMessage.execute(elem, response.Value);
					 }
				}
			});
		}
	},
	
	introMessage : {
		name : 'introMessage',
		execute : function(elem, appName) {
			var view = intuit.ipp.anywhere.view.introMessage;
			var model = intuit.ipp.anywhere.model;
			
			view.render(elem, appName);
		}	
	},

	login : {
		name : 'login',
		execute : function(elem) {
			intuit.ipp.anywhere.view.login.render(elem);
		}
	}
};

intuit.ipp.anywhere.view = {
	connectToIntuit : {
		render : function(elem) {
			// build the html inside the elem
			intuit.ipp.jQuery(elem).html("<a href='javascript:void(0)' class='intuitPlatformConnectButton'>Connect with QuickBooks</a>");
			intuit.ipp.anywhere.tracking.trackEvent("ConnectButton", "Render", "ConnectWithQuickBooks", "load");
			// init the listeners
			intuit.ipp.jQuery(".intuitPlatformConnectButton").click(function() {
				intuit.ipp.anywhere.controller.onConnectToIntuitClicked(this);
			});
		}
	},
	blueDot : {
		render : function(elem) {
			var buildTools = function(data) {
				// var el = intuit.ipp.jQuery("<div id='intuitACNav' class='intuitACNav ipp'><a id='intuitACLogo' class='intuitACLogo ipp' href='javascript:void(0);' title='Intuit App Center'><span class='blueDot ipp'>&nbsp;</span></a><div id='intuitACTools' class='intuitACTools ipp'></div>");
				var el = intuit.ipp.jQuery('<div id="intuitPlatformAppMenu"><a id="intuitPlatformAppMenuLogo" href="javascript:void(0);" title="Intuit App Center"><span id="intuitPlatformAppMenuDot">&nbsp;</span></a><div id="intuitPlatformAppMenuDropdown" style="display: none;"><div id="intuitPlatformAppMenuDropdownTop"></div><div id="intuitPlatformAppMenuDropdownInner"></div></div></div>');
				return el;
			};

			var initListeners = function() {
				intuit.ipp.jQuery("#intuitPlatformAppMenuLogo").click(toggle);
			};

			var toggle = function(e) {
				intuit.ipp.jQuery('#intuitPlatformCallout').hide();
	
				intuit.ipp.jQuery("#intuitPlatformAppMenuDropdown").toggle();

				var isVisible = intuit.ipp.jQuery("#intuitPlatformAppMenuDropdown").is(":visible");
				intuit.ipp.jQuery("#intuitPlatformAppMenuLogo").toggleClass("opened", isVisible);

				// hide menu when user clicks outside of it
				// but only listen to body clicks if menu is visible
				// unbind when menu is not visible
				if (isVisible) {
					intuit.ipp.jQuery("body").bind("click", onBodyClicked);
				} else {
					intuit.ipp.jQuery("body").unbind("click", onBodyClicked);
				}

				intuit.ipp.anywhere.tracking.trackEvent("AppMenu", isVisible ? "Show" : "Hide", "", "click");
				intuit.ipp.anywhere.view.blueDot.setupScroll();
				e.preventDefault();
				return false;
			};

			var onBodyClicked = function(e) {
				if(!intuit.ipp.jQuery(e.target).parents().is("#intuitPlatformAppMenuDropdown")) {
					toggle(e);
				}
			};

			intuit.ipp.jQuery(elem).append(buildTools());

			initListeners();

			intuit.ipp.jQuery("#intuitPlatformAppMenuLogo").bind("click", intuit.ipp.anywhere.model.blueDot.loadWidget);
			intuit.ipp.anywhere.tracking.trackEvent("AppMenu", "Render", "", "load");
			// intuit.ipp.anywhere.controller.onBlueDotClicked(elem);

			/* handler called only once upon first click of logo */
		},

		setupScroll: function() {
			ht = intuit.ipp.jQuery(".intuitPlatformAppMenuDropdownAppsList").height();
			intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownAppsListScroll").hide();
			max = (intuit.ipp.jQuery(window).height() - (intuit.ipp.jQuery("#intuitPlatformAppMenuDropdown").height() + intuit.ipp.jQuery("#intuitPlatformAppMenuLogo").height()) - 50);
			max = (max < 40) ? 40 : max;
			if(max < ht) {
				intuit.ipp.jQuery(".intuitPlatformAppMenuDropdownAppsListScrollViewport").height(max);
			} else {
				intuit.ipp.jQuery(".intuitPlatformAppMenuDropdownAppsListScrollViewport").height(ht);
			}
			intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownAppsListScroll").show();
			intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownAppsListScroll").tinyscrollbar();
		}
	},
	
	introMessage: {
		render: function(elem, appName) {
			var html = "<div id='intuitPlatformCallout'><span class='intuitPlatformCalloutPointer'></span><div class='close' onclick='intuit.ipp.anywhere.tracking.trackEvent(\"IntroMsg\", \"Close\", \"IntroMsg\", \"close\"); intuit.ipp.jQuery(\"#intuitPlatformCallout\").hide();' title='Close dialog'>X</div><div class='intuit-bigText'>Congratulations!<br/>" + 
				appName + " & QuickBooks are now connected!</div></div>";
			intuit.ipp.anywhere.tracking.trackEvent("IntroMsg", "Render", "IntroMsg", "load");
            intuit.ipp.jQuery('#intuitPlatformAppMenu').prepend(html);
		}
	},

	login: {
		render : function(elem) {
			var type = intuit.ipp.jQuery(elem).attr('type') || 'horizontal';
			var href = intuit.ipp.jQuery(elem).attr('href') || "#";
			if(type != 'vertical' && type != 'horizontal' && type != 'logo') {
				type = 'horizontal';
			}
		    type=type.replace(/\b[a-z]/g, function() { return arguments[0].toUpperCase(); })
		    intuit.ipp.jQuery(elem).html('<a href="' + href + '" class="intuitPlatformLoginButton' + type + '">Sign in with Intuit</a>');
			intuit.ipp.anywhere.tracking.trackEvent("LoginButton" + type, "Render", "SignInWithIntuit", "load");
		    intuit.ipp.jQuery(".intuitPlatformLoginButton"+type).click(function() {
		        intuit.ipp.anywhere.controller.onSignInWithIntuitClicked(this);
			});
        }
	},
	
	logout: {
		render: function (callback) {
			intuit.ipp.anywhere.view.popup.render();
			html = intuit.ipp.jQuery('<div style="margin:10px 0;"></div>');
			html.append('<h2 style="color: #4C9E19; font: normal 21px Verdana; margin: 0;">Would you also like to log out of your Intuit account?</h2>');
			html.append('<br />');
			btn = intuit.ipp.jQuery('<button id="logoutConfirmDialogYesButton">Yes</button>');
			btn.click(function () {
				intuit.ipp.jQuery.ajax({
					url: "https://" + intuit.ipp.anywhere.serviceHost + "/Account/LogoutJSONP?callback=?",
					dataType: "jsonp",
					complete: function () {
						callback();
						intuit.ipp.anywhere.view.popup.hide();
					}
				});
			});
			html.append(intuit.ipp.jQuery('<span class="intuitPlatformLargeButton intuitPlatformButtonOrange"></span>').append(intuit.ipp.jQuery('<span class="intuitPlatformLargeButtonWrapper"></span>').append(btn)));
			html.append(' or ');
			btn = intuit.ipp.jQuery('<button id="logoutConfirmDialogNoButton">No</button>');
			btn.click(function () {
				callback();
				intuit.ipp.anywhere.view.popup.hide();
			});
			html.append(intuit.ipp.jQuery('<span class="intuitPlatformLargeButton"></span>').append(intuit.ipp.jQuery('<span class="intuitPlatformLargeButtonWrapper"></span>').append(btn)));
			html.append('<br /><br />');
			
			intuit.ipp.anywhere.view.popup.insert(html);
			intuit.ipp.anywhere.view.popup.show();
		}
	},
	
	connected: {
		render: function (opts) {
			if(opts["name"] === undefined || opts["name"] === "") return false;
			if(opts["appid"] === undefined || opts["appid"] === "") return false;
			if(opts["realmName"] === undefined || opts["realmName"] === "") return false;
			if(opts["data"] === undefined) opts["data"] = [];
			intuit.ipp.anywhere.view.popup.render();
			html = intuit.ipp.jQuery('<div style="margin:10px 0;"></div>');
			
			html.append('<h2 style="color: #4C9E19; font: normal 21px Verdana; margin: 0;">' + opts["name"] + ' and QuickBooks are now connected!</h2>');
			html.append('<br />');
			html.append('<div id="intuitPlatformSyncingGraphic"><div id="intuitPlatformSyncingGraphicQBIcon"><span>' + opts["realmName"] + '</span></div><div id="intuitPlatformSyncingGraphicAppIcon"><img src="https://' + intuit.ipp.anywhere.serviceHost + '/Content/images/apps/' + opts["appid"] + '/applogo.png" width="46" /><span>' + opts["name"] + '</span></div></div>');
			html.append('<br />');
			html.append('<div style="font: normal 14px Verdana; margin: 0;">QuickBooks is now sharing your company data with ' + opts["name"] + '...</div><br />');
			
			ul = intuit.ipp.jQuery('<ul class="intuitPlatformCheckmarkList"></ul>');
			for(i in opts["data"]) {
				ul.append('<li>' + opts["data"][i] + '</li>');
			}
			html.append(ul);
			
			//html.append('<br />');
			
			btn = intuit.ipp.jQuery('<button>Go to App</button>');
			btn.click(function () {
				intuit.ipp.anywhere.view.popup.hide();
			});
			html.append(intuit.ipp.jQuery('<span class="intuitPlatformLargeButton intuitPlatformButtonOrange"></span>').append(intuit.ipp.jQuery('<span class="intuitPlatformLargeButtonWrapper"></span>').append(btn)));
			
			html.append('<br /><br />');
			
			intuit.ipp.anywhere.view.popup.insert(html);
			intuit.ipp.anywhere.view.popup.show();
			if(typeof opts["callback"] === "function") intuit.ipp.anywhere.view.popup.hide_callback = opts["callback"];
		}
	},
	
	popup: {
		render: function () {
			if(intuit.ipp.jQuery("#intuitPlatformPopupWrap").length == 0) {
				intuit.ipp.jQuery("body").append('<div id="intuitPlatformPopupWrap"><div id="intuitPlatformPopup"><div id="intuitPlatformPopupContent"><div id="intuitPlatformPopupHeader"></div><div id="intuitPlatformPopupInnerContent"></div></div></div></div><div id="intuitPlatformPopupOverlay"></div>');
				intuit.ipp.jQuery("#intuitPlatformPopupOverlay").height(intuit.ipp.jQuery(window).height());
				intuit.ipp.jQuery(window).resize(function () {
					intuit.ipp.jQuery("#intuitPlatformPopupOverlay").height(intuit.ipp.jQuery(window).height());
					intuit.ipp.anywhere.view.popup.center();
				});
				intuit.ipp.jQuery("#intuitPlatformPopupOverlay").click(function () {
					intuit.ipp.anywhere.view.popup.hide();
				});
			}
		},
		
		insert: function (html) {
			intuit.ipp.jQuery("#intuitPlatformPopupInnerContent").html(html);
			intuit.ipp.anywhere.view.popup.center();
		},
		
		center: function () {
			intuit.ipp.jQuery("#intuitPlatformPopupWrap").css({
				left: (intuit.ipp.jQuery(window).width() - intuit.ipp.jQuery("#intuitPlatformPopupWrap").width())/2,
				top: (intuit.ipp.jQuery(window).height() > intuit.ipp.jQuery("#intuitPlatformPopupWrap").height() ? (intuit.ipp.jQuery(window).height() - intuit.ipp.jQuery("#intuitPlatformPopupWrap").height())/2 : 40)
			});
		},
		
		show: function () {
			intuit.ipp.jQuery("#intuitPlatformPopupOverlay").fadeIn(function () {
				intuit.ipp.jQuery("#intuitPlatformPopupWrap").fadeIn();
			});
		},
		
		hide: function () {
			intuit.ipp.jQuery("#intuitPlatformPopupWrap").fadeOut(function () {
				intuit.ipp.jQuery("#intuitPlatformPopupOverlay").fadeOut(function () {
					if(typeof intuit.ipp.anywhere.view.popup.hide_callback === "function") {
						intuit.ipp.anywhere.view.popup.hide_callback();
						intuit.ipp.anywhere.view.popup.hide_callback = undefined;
					}
				});
			});
		}
	}
};

intuit.ipp.anywhere.model = {
	blueDot : {
		loadWidget: function(event) {
			if(intuit.ipp.anywhere.menuProxy) {
				intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownInner").html('<span class="intuitPlatformAppMenuDropdownHeader">Please wait, loading menu...</span>');
				intuit.ipp.jQuery("#intuitPlatformAppMenuLogo").unbind("click", intuit.ipp.anywhere.model.blueDot.loadWidget);
				intuit.ipp.jQuery.ajax({
					url: intuit.ipp.anywhere.menuProxy + (intuit.ipp.anywhere.menuProxy.match(/(?:\?([^#]*))/g) ? "&" : "?") + (new Date()).valueOf(),
					success: function(data) {
						if(data.match(/ipp_unscheduled_maintenance/) || data.match(/ipp_scheduled_maintenance/) ) {
							intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownInner").html('<span class="intuitPlatformAppMenuDropdownHeader">We are sorry, but we cannot load the menu right now.</span>');
						} else {
							intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownInner").html(data);
						}
						intuit.ipp.jQuery("#intuitPlatformAppMenuDropdown").show();
						intuit.ipp.jQuery("#intuitPlatformAppMenuLogo").addClass("opened");
						intuit.ipp.anywhere.view.blueDot.setupScroll();
						intuit.ipp.jQuery(window).resize(intuit.ipp.anywhere.view.blueDot.setupScroll);
					},
					error: function(jqXHR, textStatus, errorThrown) {
						if(typeof console !== "undefined" && typeof console.log !== "undefined") {
							if(jqXHR.status == 404) {
								console.log("IPP: App Menu Proxy URL is incorrect");
							} else {
								console.log("IPP: App Menu Proxy returns " + jqXHR.status + " status code");
							}
						}
						intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownInner").html('<span class="intuitPlatformAppMenuDropdownHeader">We are sorry, but we cannot load the menu right now.</span>');
					}
				});
			} else {
				intuit.ipp.jQuery("#intuitPlatformAppMenuDropdownInner").html('<span class="intuitPlatformAppMenuDropdownHeader">We are sorry, but we cannot load the menu right now.</span>');
				if(typeof console !== "undefined" && typeof console.log !== "undefined") {
					console.log("IPP: Missing menu proxy");
				}
			}
			event.preventDefault();
			return false;
		}
	}
};

intuit.ipp.anywhere.service = {
	timeout : 5000,

	openPopupWindow : function(wind) {
		var url = "https://" + intuit.ipp.anywhere.serviceHost + wind.path;
		window.open(url, "ippPopupWindow", "location=1,width=400,height=300");
	},

	openExternalPopupWindow : function (wind) {
		parameters = "location=1";
		if(wind.height == null && wind.width == null) {
			wind.height = 630;
			wind.width = 703;
		}
		parameters += ",width=" + wind.width + ",height=" + wind.height;
		if(wind.centered) {
			parameters += ",left=" + (screen.width - wind.width)/2 + ",top=" + (screen.height - wind.height)/2;
		}
		window.open(wind.url, "ippPopupWindow", parameters);
	}
};

intuit.ipp.anywhere.tracking = {
	server: function () {
		return "https://" + intuit.ipp.anywhere.serviceHost + "/trackapi/TrackingActions"
	},

	getPageName: function () {
		return document.title;
	},

	trackEvent : function(elementName, action, elementText, eventType) {
		//Anonmous Product Improvement Feedback
		//Intuit Feedback System
		var eventData = { pn: intuit.ipp.anywhere.tracking.getPageName(), nm: "ia" + elementName, typ: action, txt: elementText, et: eventType, ref: document.referrer, url: document.URL, host: window.location.host };
		intuit.ipp.jQuery.getJSON(intuit.ipp.anywhere.tracking.server() + "?remote=true&" + intuit.ipp.anywhere.tracking.util.arrayToURL(eventData) + "&callback=?");
	},
	
    trackEventSync : function(elementName, action, elementText, eventType) {
		//Anonmous Product Improvement Feedback
		//Intuit Feedback System
		var eventData = { pn: intuit.ipp.anywhere.tracking.getPageName(), nm: "ia" + elementName, typ: action, txt: elementText, et: eventType, ref: document.referrer, url: document.URL, host: window.location.host };
		intuit.ipp.jQuery.ajax({
          url: intuit.ipp.anywhere.tracking.server() + "?remote=true",
          dataType: 'json',
          data: eventData,
          async: false
        });
        //intuit.ipp.jQuery.getJSON(intuit.ipp.anywhere.tracking.server() + "?remote=true&" + intuit.ipp.anywhere.tracking.util.arrayToURL(eventData) + "&callback=?");
	},

	util: {
		arrayToURL: function(array) {
			var pairs = [];
			for (var key in array) {
				if (array.hasOwnProperty(key)) {
					pairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(array[key]));
				}
			}
			return pairs.join('&');
		}
	}
};

// function that starts it all. timeout is 0
(function() {
	// these are the domains whose js files we're going to look at
	// intuit.ipp.ourDomain = /(.intuit.com).*?#(.*)/;
	intuit.ipp.ourDomain = /intuit.com$/;
	if(window.jQuery === undefined || window.jQuery.fn.jquery < "1.4.2") {
		// minimum version 1.4.2
		var script_tag = document.createElement('script');
		script_tag.setAttribute("type","text/javascript");
		script_tag.setAttribute("src", "https://ajax.googleapis.com/ajax/libs/jquery/1.6/jquery.min.js");
		script_tag.onload = function () {
		    //IPP-1811 Internet Explorer 9 and above and intuit.ipp.anywhere.js bugs. in IE9 and higher, onload gets called twice
		    // once by window.onload and once by the onreadystatechange.
		    if (intuit.ipp.anywhere.onloadCalled) {
		        return false;
		    }
		    intuit.ipp.anywhere.onloadCalled = true;
			if(window.jQuery) {
				intuit.ipp.jQuery = window.jQuery.noConflict(true);
				intuit.ipp.anywhere.windowLoad();
			}
		};
		script_tag.onreadystatechange = function () { // Same thing but for IE
			if (this.readyState == 'complete' || this.readyState == 'loaded') {
				script_tag.onload();
			}
		};

		// Try to find the head, otherwise default to the documentElement
		(document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);

	} else {
		// we do have jquery
		intuit.ipp.jQuery = window.jQuery;
		intuit.ipp.anywhere.windowLoad();
	}
})();