function jsSig(){
    var asyncInputBuffer = [];
    var networkChanged = true;
    var sortedNetwork = [];
    var sigNet = [];
    var freq = 0;
    var sigCount = 0;
    
    function nchange(n){
	var nc = true;
	if(n.backward !== undefined){
	    n.backward.forEach(function(z){
		nc = nc && z.nochange;
	    });
	}
	return nc;
    }


    var Nothing = { Nothing: true }
    function Just(x) { 
	return { Just: x } 
    }
    function fromJust(x){
	if(isNothing(x)) 
	    throw "fromJust: Object is Nothing."
	return x.Just;
    }
    function isNothing(obj){
	if(obj.Nothing === true) return true;
	return false; 
    }

    var NoChange = { NoChange: true }    
    function isNoChange(obj){
	if(obj.NoChange === true) return true;
	return false;
    }

    var nsteps = 0;
    function step(sorted){
	nsteps++;
	for(var i = 0; i < asyncInputBuffer.length; i++){
	    var o = asyncInputBuffer[i];
	    o.node.newAsyncValue = o.value;
	}
	asyncInputBuffer = [];

	sorted.forEach(function(n){
	    var nc = nchange(n);
	    n.nochange = true;
	    if(n.category === 'input'){
		n.nochange = false;
		var z = n.stepSample(n);
		if(!isNoChange(z)){ 
		    n.nochange = false; n.value = Just(z); }
		else n.nochange = true;	    
	    }
	    if(n.category === 'asyncinput'){
		var z = n.stepSample(n);
		if(n.newAsyncValue === undefined) { n.nochange = true; }
		else { 
		    n.value = Just(n.newAsyncValue); 
		    delete n.newAsyncValue;
		    n.nochange = false; 
		}
	    }
	    if(n.category === "const"){
		if(n.emitted === undefined){ 
		    n.emitted = true; n.nochange = false;}
		else n.nochange = true;
	    }
	    if(n.category === "foldp"){
		//foldp SFN's initial .value is set to undefined
		if(n.value === undefined) {
		    if(n.skipInitial === true) n.value = Nothing;
		    else n.value = Just(n.init);
		}
		if(n.newAsyncValue === undefined) n.newAsyncValue = n.init; 
		if(n.newAsyncValue === undefined){ n.nochange = true; }
		else {
		    var oldValue;
		    var first = false; 
		    if(isNothing(n.value)) {
			first = true; 
			oldValue = n.newAsyncValue;
		    }
		    else oldValue = fromJust(n.value);
		    var z = n.stepSample(n.newAsyncValue, oldValue);
		    delete n.newAsyncValue;
		    if(oldValue === z && !first ){ n.nochange = true; }
		    n.value = Just(z); 
		    n.nochange = false; 
		}
	    }
	    if(!nc){
		n.nochange = false;
		if(n.category === "aggregator"){
		    var out = [];
		    var outputNothing = false; 
		    for(var i = 0; i < n.backward.length; i++){
			
			if(!isNothing(n.backward[i].value)){
			    out.push(fromJust(n.backward[i].value));
			}
			else if(n.filterNothings === false){
			    outputNothing = true;
			    break;
			}
		    }
		    if(outputNothing) n.value = Nothing;
		    else n.value = Just(out); 
		}
		if(n.category === 'builtin'){ 
		    var z = n.stepSample(n);
		    if(!isNoChange(z)){ n.nochange = false; n.value = Just(z); }
		    else n.nochange = true;	    
		}
		if(n.category === 'SF') { 
		    if(isNothing(n.backward[0].value))
			n.value = Nothing;
		    else n.value = Just(n.stepSample( 
			fromJust(n.backward[0].value) ));
		}		
		//Lifts propagate Nothing values - akin to 
		// fmap'ing over a Nothing. 
		if(n.category === 'lift' || n.category === 'output'){ 
		    var inputsJust = true;
		    var vals = n.backward.map(function(sfn){ 
			if(isNothing(sfn.value)) {
			    inputsJust = false;
			    return undefined; // empty array elem
			}
			else return fromJust(sfn.value)
		    });
		    if(!inputsJust) n.value = Nothing;
		    else n.value = Just(n.stepSample.apply(n, vals));
		}
	    }
	});
    }

    //DFS Topo Sort
    // Temporary, inefficient solution - 
    // in the future we can explore at each step rather than sorting. 
    function topoSort(sigNet){
	var nodes = [];
	var L = [];
	function discoverNode(i){
	    nodes.push(i);
	    i.tmarked = false; //track for cycles
	    i.pmarked = false;
	    if(i.forward === undefined){ return; }
	    i.forward.forEach(function(n){
		discoverNode(n);
	    });
	}
	sigNet.forEach(discoverNode); 
	
	function visit(n){
	    if(n.tmarked) return false; //cycle
	    if(!n.pmarked){
		n.tmarked = true;
		n.pmarked = true;
		L.push(n);
		if(n.backward !== undefined)
		    n.backward.forEach(function(dep){ visit(dep); });
	    }
	}
	while(nodes.length){ visit(nodes.pop()); }
	//Cleanup
	L.forEach(function(n){
	    n.tmarked = undefined;
	    n.pmarked = undefined;
	});
	return L.reverse();
    } 

    /* Linking signal nodes */
    function connect(n1, n2){
	networkChanged = true;
	n2.backward.push( n1 ); 
	n2.incoming[n1.guid] = true;
	n1.forward.push( n2 );
	return n2;
    }

    //Reconnect sets the sole input for n1 to be n2
    function reconnect(n1, n2){
	n2.backward = [];
	n2.incoming = {}; 
	return connect(n1, n2);
    }

    function disconnect(n1, n2){
	networkChanged = true;
	n1.forward = n1.forward.filter(function(e){ return e !== n2; });
	n2.backward = n2.backward.filter(function(e){ return e !== n1; });
	n2.incoming[n1.guid] = false;
    }

    function asyncInput(node, value){
	asyncInputBuffer.push({node: node, value: value});
	node.nochange = false;
    }

    /* Signal Function Node -- representation of a Signal
       A node in the network connecting signal functions together.
    */
    function SFN(i) {
	if(i === undefined){ i = { category: null, stepSample: null }}
	this.value = Nothing;
	this.forward = Array();
	this.backward = Array();
	this.category = i.category;
	this.stepSample = i.stepSample;
	this.guid = sigCount++;
	this.incoming = {};
    }

    function removeSFN(SFN){
	SFN.forward.forEach(function(n){ disconnect(SFN, n); });
	SFN.backward.forEach(function(n){ disconnect(n, SFN); });
    }
    
    /* Private Signal Function utilities */
    function sfnCopy(s){
	var cpy = new SFN();
	cpy.category = s.category;
	cpy.stepSample = s.stepSample;
	cpy.init = s.init;
	return cpy;
    }

    /* Signal function creation & composition */

    /* Compose connects two signal function nodes in a 
     * referentially transparent way by copying the second node.
     *
     * It functions both as application and composition
     * Since it can take the form of either:
     *   - SF a b -> SF b c -> SF a c
     *   - Signal b -> SF b c -> Signal c
     */
    function compose(s1, s2){
	return connect(s1, sfnCopy(s2));
    }
    SFN.prototype.compose = function(s2){ return compose(this, s2); }

    function compose2(s1, s2, s3){
	var z = sfnCopy(s3);
	connect(s1, z);
	connect(s2, z);
	return z;
    }

    function compose3(s1, s2, s3, s4){
	var z = sfnCopy(s4);
	connect(s1, z);
	connect(s2, z);
	connect(s3, z);
	return z;
    }

    // Lift a function to a signal function
    function lift(f){
	var sig = new SFN();
	sig.category = "lift";
	sig.stepSample = f;
	return sig;
    }
    SFN.prototype.lift = function(f){ return connect(this, lift(f)); }

    //def sets a default value if the incoming signal is a Nothing
    function def(d){
	var sig = new SFN();
	sig.lastValue = undefined; 
	sig.category = "input";
	sig.stepSample = function(n){
	    var out; 
	    if(n.backward[0] === undefined ||
	       isNothing(n.backward[0].value)) out = d;
	    else out = fromJust(n.backward[0].value);
	    if(out === n.lastValue) return NoChange;
	    n.lastValue = out; 
	    return out; 
	};
	return sig;
    }
    SFN.prototype.def = function(d){ return connect(this, def(d)); }

    //Constant Signal
    function constant(c){
	var sig = new SFN();
	sig.category = "const";
	sig.value = Just(c);
	return sig;
    }

    //Past-dependent signal
    function foldp(sig, f, init, skipInitial){
	/* In order to prevent infinite loops we can't form 
	   any cycles in our SFN DAG. To prevent this, 
	   foldpEmit node transmits the incoming signal 
	   with one time step delay to foldpRecv
	 */
	var foldpRecv = new SFN();
	foldpRecv.category="foldp";
	foldpRecv.stepSample = f;
	foldpRecv.init = init;
	foldpRecv.skipInitial = skipInitial;
	foldpRecv.value = undefined; //initial
	addSFN(foldpRecv);

	var foldpEmit = new SFN();
	foldpEmit.category="SF";
	foldpEmit.stepSample = function(v){
	    asyncInput(foldpRecv, v);
	    return undefined; 
	}
	
	connect(sig, foldpEmit);
	return foldpRecv;
    }
    SFN.prototype.foldp = function(f, init, si){ return foldp(this, f, init, si); }
    
    function copy(x){
	if(typeof(x) !== "object") return x; 
	var isArray = x[0] !== undefined; 
	var y = {};
	if(isArray) y = [];
	for(k in x){
	    y[k] = copy(x[k]);
	}
	return y; 
    }

    function loop(sig){
	return sig.foldp(function(a, b){ return copy(a) }, undefined, true);
    }
    SFN.prototype.loop = function(){ return loop(this); }

    function selfLoop(start, end, def){
	var dummy = new SFN({category: "input", stepSample: function(){ return nsteps; }});
	var fp = end.foldp(function(a, b){ return a }, def);
	connect(fp, start); 
	connect(dummy, fp);
	return end; 
    }

    function receiver(d){
	if(d === undefined)
	    throw "Receivers must be given a default value.";
	var z = def(d);
	z.receiver = { bound : false }
	return z; 
    }
    
    SFN.prototype.transmitter = function(recv){ 
	if(recv.receiver.bound !== false) {
	    console.log(recv);
	    throw "Receivers can only be bound to once."
	}
	recv.receiver.bound = true; 
	connect(this.loop(), recv);
    }

    /* Signal generation & aggregation */
    
    // Aggregator a : Signal [a]
    // + Signals can be dynamically attached to an Aggregator via
    //   `aggregate`. The aggregator forms a list of the values of these
    //   signals and outputs that as a Signal. 
    // + if filterNothings === true then nothings will be filtered from the list
    // + otherwise the Aggregator will output Nothing until all incoming
    //   signals are Just's. 
    function Aggregator(filterNothings){
	if(filterNothings === undefined) filterNothings = true; 
	var sig = new SFN();	
	sig.category = "aggregator";
	sig.filterNothings = filterNothings; 
	sig.value = Just([]);
	return sig;
    }

    // aggregate : Signal a -> Aggregator a -> SignalM (Signal a)
    // Returns the original signal given, unmodified. 
    function aggregate(sig, agg){
	if(agg.category != "aggregator") 
	    throw "Second argument to aggregate must be an aggregator.";
	/*if(agg.incoming[sig.guid] === true){
	    return sig; 
	}*/
	agg.incoming[sig.guid] = true;
	connect(sig, agg);
	return sig; 
    }
    SFN.prototype.aggregate = function(sig){ return aggregate(sig, this); }
    
    //aggregateOn aggregates a new copy of (this) into agg
    // every time sig changes. 
    SFN.prototype.aggregateOn = function(sig, agg){
	if(agg.category != "aggregator") 
	    throw "Second argument to aggregateOn must be an aggregator.";
	var last = undefined;
	function fun(sigVal, changeVal){
	    console.log("AggregateOn", sigVal, changeVal);
	    if(changeVal === last) return;
	    last = changeVal;
	    aggregate(constant(sigVal), agg);
	}
	return compose2(this, sig, lift(fun));
    }

    SFN.prototype.onChange = function(changeSig){
	var sig = new SFN();

	sig.category = 'builtin';
	var last = undefined; 
	sig.stepSample = function(n){
	    if(isNothing(n.backward[0].value)
	       || isNothing(n.backward[1].value)) return NoChange;
	       
	    var value = fromJust(n.backward[0].value);
	    var changeVal = fromJust(n.backward[1].value);
	    if(last === undefined){ last = changeVal; return NoChange; }
	    if(objEq(changeVal, last)) return NoChange;
	    last = changeVal;
	    return value;
	}

	connect(this, sig);
	connect(changeSig, sig);
	return sig; 
    }

    function mostRecent(sigs){
	var sig = new SFN();
	sig.category = 'builtin';
	sig.stepSample = function(n){
	    var lastValue = NoChange;
	    for(idx in n.backward){
		var b = n.backward[idx];
		if(!isNothing(b.value)
		   && (b.nochange === false
		       || lastValue === NoChange)){
		    lastValue = fromJust(b.value)
		}
	    }
	    return lastValue; 
	}
	for(idx in sigs){
	    connect(sigs[idx], sig); 
	}
	return sig; 
    }
    // combine : [Signal a] -> Signal [a]
    function combine(sigs, filterNothings){
	filterNothings = filterNothings || false; 
	var agg = Aggregator(filterNothings);	
	for(var i = 0; i < sigs.length; i++) aggregate(sigs[i], agg);
	agg.label = "combine";
	return agg; 
    }
    // Signal.combine : Signal [Signal a] -> Signal [a]
    
    // join : Signal (Signal a) -> Signal a
    function join(s){
	var sig = new SFN();
	sig.category = 'builtin';
	sig.stepSample = function(n){
	    if(isNothing(n.backward[0].value)) return NoChange;
	    var sfn = fromJust(n.backward[0].value);
	    if(n.backward.length === 1){
		if(sfn.value !== undefined){
		    connect(sfn, n);
		}
		else {
		    console.log(n.backward[0]);
		    throw "Value of signal given to join is not a signal.";
		}
	    }
	    else if(n.backward.length === 2){
		if(sfn.guid != n.backward[1].guid){
		    disconnect(sfn, n);
		    connect(sfn, n);
		    n.backward = [n.backward[0], sfn];
		    return NoChange; 
		}
		if(isNothing(n.backward[1].value)) return NoChange;
		else return fromJust(n.backward[1].value);
	    }
	    return NoChange; 
	}
	connect(s, sig);
	return sig; 
    }
    SFN.prototype.join = function(){ return join(this); }

    function isSFN(sfn){
	return sfn.backward !== undefined; //TODO
    }
    function ojoin(obj){
	var sig = new SFN();
	sig.category = 'builtin';
	var sigKeys = [];
	var base = {};
	for(k in obj){
	    if(isSFN(obj[k])){
		sigKeys.push(k);
		connect(obj[k], sig);
	    }
	    else base[k] = obj[k];
	}
	sig.stepSample = function(n){
	    var base2 = {};
	    for(k in base){ base2[k] = base[k]; }
	    for(i = 0; i < n.backward.length; i++){
		if(isNothing(n.backward[i].value)) return NoChange; 
		base2[sigKeys[i]] = fromJust(n.backward[i].value);
	    }
	    return base2; 
	}
	return sig; 
    }
    SFN.prototype.ojoin = function(){ return sig.lift(ojoin).join(); }

    //Filter a signal based on a predicate
    // filter : Signal a -> (a -> Bool) -> Signal a
    function filter(pred){
	var sig = new SFN();
	sig.category = "SF";
	sig.stepSample = function(n){
	    if(nchange(n)) return NoChange;
	    if(!pred(n.backward[0].value)) return NoChange;
	    return n.backward[0].value;
	}
	return sig;
    }
    SFN.prototype.filter = function(pred){ return connect(this, filter(pred)); }

    function objEq(o1, o2){
	if(typeof(o1) !== 'object'
	   || typeof(o2) !== 'object') return o1 === o2;
	for(k in o1){
	    if(o2[k] === undefined && o1[k] !== undefined) return false; 
	    if(!objEq(o1[k], o2[k])) return false; 
	}
	return true; 
    }
    function filterRepeats(){
	var sig = new SFN();
	sig.category = "builtin";
	sig.lastValue = undefined;
	sig.stepSample = function(n){
	    if(isNothing(n.backward[0].value)) return NoChange;
	    if(nchange(n)) return NoChange;
	    if(objEq(fromJust(n.backward[0].value), sig.lastValue)) {
		console.log("Filtering value", n.backward[0].value);
		return NoChange;
	    }
	    console.log("Not filtering value", fromJust(n.backward[0].value), sig.lastValue);
	    sig.lastValue = fromJust(n.backward[0].value);
	    return fromJust(n.backward[0].value);
	}
	return sig;	
    }
    SFN.prototype.filterRepeats = function(){ return connect(this, filterRepeats()); }

    /** Additional signal functions **/
    
    //Internal function that serves as a pattern for creating
    // async input signals
    function asyncInputSig(f, def){
	var init = true;
	var sig = new SFN();
	sig.category = "asyncinput"
	sig.stepSample = function(n){ 
	    if(!init && nchange(n)) { n.nochange = true; return undefined; }
	    else {
		init = false;
		jQuery(document).ready(function(){ f(n) });
		return true;
	    }
	}
	if(def !== undefined) sig.value = Just(def); 
	return sig;
    }

    var Internal = {
	steps : new SFN({category: "input", stepSample: function(){ return nsteps; }}),
	sigNetSize : new SFN({category: "input", stepSample: function(){ return sigNet.length; }})
    };
    
    var Util = {
	date : new SFN({category: "input", stepSample: function(){ return new Date(); }})
	,milliseconds : new SFN({category: "input", stepSample: function(){ return (new Date()).valueOf(); }})
    }	

    var Window = {
     	scrollTop: asyncInputSig(function(n){
	    asyncInput(n, 0);
	    jQuery(window).scroll(
		function(e){ asyncInput(n, jQuery(window).scrollTop()); }
	    );
	}),
	width: asyncInputSig(function(n){
	    asyncInput(n, jQuery(window).width());
	    jQuery(window).resize(
		function(e){ asyncInput(n, jQuery(window).width()); }
	    );
	})

	
    }
    var Mouse = 
	{
	    position: 
     	      asyncInputSig(function(n){
		  asyncInput(n, []);
		  jQuery(document).mousemove(
		      function(e){ asyncInput(n, [e.pageX, e.pageY]); }
		  );
	      })
	    ,clicked:
 	      asyncInputSig(function(n){
		  asyncInput(n, "false");
		  jQuery(document).mousedown(
		      function(e){ asyncInput(n, "true"); }
		  );
		  jQuery(document).mouseup(
		      function(e){ asyncInput(n, "false"); }
		  );
	      })
	}

    SFN.prototype.throttle = function(t){
	var sig = new SFN();
	sig.category = 'builtin';
	var lastValue = undefined; 
	var lastTime = 0;
	sig.stepSample = function(n){
	    var time = (new Date()).valueOf();
	    var val = n.backward[0].value; 
	    if(time - lastTime > t){
		if(isNothing(val)) return NoChange;
		lastValue = val; 
		lastTime = time; 
		return fromJust(val); 
	    }
	    else return NoChange; 

	}
	return connect(this, sig);
    }

    SFN.prototype.decay = function(t){
	var sig = new SFN();
	sig.category = 'input';
	var lastValue = undefined; 
	var lastTime = 0;
	var r = undefined; 
	var lastIn = undefined; 
	sig.stepSample = function(n){
	    var time = (new Date()).valueOf();
	    var val = n.backward[0].value; 
	    if(isNothing(val)) return NoChange;
	    if(n.backward[0].nochange === false) lastTime = time; 
	    if(time - lastTime > t) r = { decayed : true, value: fromJust(val) };
	    else r = { decayed : false, value: fromJust(val) };
	    if(JSON.stringify(r) === JSON.stringify(lastValue)) return NoChange;
	    lastValue = r; 
	    return r; 
	}
	return connect(this, sig);
    }
    
    //Toggles between true and false every time the incoming
    // signal changes from def to !def. 
    function toggle(d){
	if(d === undefined) d = false; 
	var def = d; 
	var last = def; 
	var toggle = def; 
	function cmp(x){
	    var n; 
	    if(last === def && x === !def) toggle = !toggle;
	    n = toggle; 
	    last = x; 
	    return n; 
	}
	return lift(cmp);
    }
    SFN.prototype.toggle = function(def){ return connect(this, toggle(def)); }
    
    //bSwitch will output sig1 when switchSig === true and 
    // sig2 when switchSig === false
    function caseSwitch(switchSig, obj){
	function sw(s, o){
	    console.log("Switching!", s, o);
	    if(o[s] === undefined) 
		throw "caseSwitch: no case for property "+s;
	    return o[s];
	}
	var s = lift(sw);
	connect(switchSig, s);
	connect(ojoin(obj), s);
	return s; 
    }

    function valSig(){
	return asyncInputSig(function(n){
		    asyncInput(n, jQuery(n.backward[0].value).val());
		    jQuery(n.backward[0].value).change(
			function(){ asyncInput(n, jQuery(n.backward[0].value).val()); }
		    );
	});
    }
    SFN.prototype.valSig = function(){ return connect(this, valSig()); }


    SFN.prototype.prop = function(k){ 
	var A = k.split(".");	
	return connect(this, sig.lift(function(o){ 
	    var tmp = o;
	    for(var i = 0; i < A.length; i++){
		var prop = A[i];
		tmp = tmp[prop];
	    }
	    return tmp;
	}));
    }

    function or(s1, s2){
	return compose2(s1, s2, lift(function(a, b){ return a || b }));
    }

    function and(s1, s2){
	return compose2(s1, s2, lift(function(a, b){ return a && b }));
    }

    SFN.prototype.not = function(s){
	return this.lift(function(b){ return !b; });
    }

    function setContents(sel){
	var sig = new SFN();
	sig.category = "output";
	sig.stepSample = function(val){
	    jQuery(sel).html(val);
	}
	return sig;
    }
    SFN.prototype.setContents = function(sel){
	return connect(this, setContents(sel));
    }

    SFN.prototype.http = function(urlSig){
	var sig = new SFN()
	sig.category = 'asyncinput';
	sig.stepSample = function(n){
	    if(nchange(n)){ return NoChange; }
	    if(isNothing(n.backward[0].value)
	      || isNothing(n.backward[1].value)) return NoChange; 
	    var url = fromJust(n.backward[1].value);
	    var data = fromJust(n.backward[0].value);
	    var lastData = undefined; 
	    var time = (new Date()).valueOf();	    
	    asyncInput(n, {
		inProgress: true
		,time: time
		,data: lastData
		,success: true
	    });

	    jQuery.ajax({url: url, cache: false, data: data
			 , method: 'POST'
			 ,complete: function(response){
			     var time = (new Date()).valueOf();
			     var data = {}
			     var success = true;
			     var error = undefined; 
			     try {  data = eval(response.responseText); }
			     catch(e){ success = false; error = e; }
			     lastData = data; 
			     asyncInput(n, {
				 inProgress: false
				 ,time: time
				 ,data: data
				 ,error: error
				 ,success: success
			     });
			 }});
	}
	connect(this, sig); 
	connect(urlSig, sig); 
	return sig;
    }

    SFN.prototype.httpSim = function(sim, delay){
	var delay = delay || 1000; 
	var sig = new SFN();
	sig.label = 'httpSim';
	sig.category = 'input';
	sig.value = Nothing; 
	var lastValue = undefined; 
	var lastTime = 0;
	var lastStepData = false; 
	var inProgress = true; 
	sig.stepSample = function(n){
	    var time = (new Date()).valueOf();
	    var val = n.backward[0].value; 
	    if(inProgress && time - lastTime > delay){
		inProgress = false; 
		if(isNothing(val)) return NoChange;
		lastTime = time; 
		var r = {
		    inProgress: false,
		    time: time, 
		    data: sim(fromJust(val))
		}; 
		if(JSON.stringify(r) === JSON.stringify(lastValue)) return NoChange;
		lastValue = r; 
		return r;
	    }
	    else if(n.backward[0].nochange === false){
		lastTime = time; 
		inProgress = true; 
	    }
	    if(lastValue === undefined){ return NoChange; }
	    var r = { inProgress: inProgress
		     , time: lastValue.time
		     , data: lastValue.data
		   };

	    if(JSON.stringify(r) === JSON.stringify(lastValue)) return NoChange;
	    lastValue = r; 
	    return r; 

	}
	return connect(this, sig);
    }    

    /* Signal network operations */
    function addSFN(SFN){
	if(SFN.added) return; 
	SFN.added = true;
	sigNet.push(SFN);
	networkChanged = true;
	return SFN;
    }

    var stop = false; 
    function runSFs(f){
	if(stop) { console.log("STOPPING"); delete this; return; }
	if(f !== undefined){ freq = f; }
	if(sortedNetwork === undefined
	   || networkChanged){
	    sortedNetwork = topoSort(sigNet);
	    networkChanged = false;
	}
	step(sortedNetwork);
	setTimeout(runSFs, freq);
    }
    
    function stopSFs(){
	stop = true; 
    }

    //Ensures that we know about every signal created
    // by the user. 
    // TODO: This needs to be much more efficient. (discover new roots on connections etc).
    function extCreate(f){
	return function(a, b, c){ 
	    if(a !== undefined && b !== undefined && c !== undefined)
		return addSFN(f(a, b, c));
	    else if(a !== undefined && b !== undefined) 
		return addSFN(f(a, b));
	    else if(a !== undefined) return addSFN(f(a));
	    else return addSFN(f());
	}
    }

    /** Add builtin signals to network **/
    for(k in Mouse) addSFN(Mouse[k]);
    for(k in Internal) addSFN(Internal[k]);
    for(k in Util) addSFN(Util[k]);
    for(k in Window) addSFN(Window[k]);

    return {
	run : runSFs,
	stop: stopSFs,
	len : function(){ return sigNet.length },
	steps : function(){ return nsteps },
	lift: extCreate(lift),
	filter: extCreate(filter),
	filterRepeats: filterRepeats,
	Aggregator: extCreate(Aggregator),
	aggregate: aggregate,
	loop : loop,
	receiver: receiver,
	selfLoop : selfLoop,
	join : join,
	ojoin : ojoin,
	combine: extCreate(combine),
	compose: compose,
	compose2: compose2,
	compose3: compose3,
	foldp: extCreate(foldp), 
	or: or,
	and: and,
	constant: extCreate(constant),
	mostRecent: mostRecent, 
	caseSwitch: caseSwitch,
	Mouse: Mouse,
	Util: Util,
	Internal: Internal,
	Window: Window,
	__: {
	    SFN : SFN
	    , copy: copy
	    , connect: connect
	    , reconnect: reconnect
	    , asyncInputSig : asyncInputSig
	    , asyncInput : asyncInput
	    , addSFN : addSFN
	}
    }
};

window.sig = jsSig();
