window.wg_instances = 0; 
function wgSig(s){
    var sig = s;
    var instance = wg_instances++;
    if(sig === undefined){ 
	if(window.sig === undefined) throw "wgSig requires jsSig";
	sig = window.sig;
    }

    /** Bindings are signals that depend on the output of elements.
      * ex) elemSig.clicked(), elemSig.visible(), etc
      * Since elements are often rerendered and rebound, we keep 
      *  track of connected signals so we can reconnect them to the new
      *  input signals.
     **/ 
    var bindings = {};

    var defBindings = 
	{ clicked : false, mouseover: false, val : undefined, focus: false }

    function _registerBinding(guid, name, def){ 
	var d = defBindings[name];
	if(def !== undefined) d = def; 
	if(bindings[guid] === undefined) bindings[guid] = {};
	if(bindings[guid][name] === undefined){
	    var r = sig.lift(function(x){ return x; }).def(d);
	    sig.__.addSFN(r);
	    bindings[guid][name] = r;
	    return r; 
	}
	else return bindings[guid][name];
    }

    // The default WidgetSpec
    function defaultWS(){
	return {
	    type : "WidgetSpec",
	    css: {},
	    visible: true,
	    gen: function(){ return "<div></div>"; }
	}
    }

   
    function sel(elem, prefix){ 
	if(prefix === undefined) prefix = "#";
	return prefix+"wgElem_"+elem.guid; 
    }

    function elemChanged(z){ return true; } // TODO
    
    function _updateChildren(elem, force){
	//Do one pass on the old data to get a hashtable of all 
	// old elements present.
	var oldIdxs = {};
	if(elem.oldChildren !== undefined){
	    for(var i = 0; i < elem.oldChildren.length; i++){
		if(elem.oldChildren[i] !== undefined){
		    oldIdxs[elem.oldChildren[i].guid] = i;
		}
	    }
	}
	//Iterate over new children, updating old ones as necessary.
	for(var i = 0; i < elem.children.length; i++){
	    var ch = elem.children[i];
	    if(ch === undefined) continue; //TODO
	    //Possibly update element
	    if(oldIdxs[ch.guid] !== undefined && force === false){
		if(elem.oldChildren === undefined
		   || elemChanged(ch, elem.oldChildren[oldIdxs[ch.guid]]) 
		   ){
		    _render(ch, sel(elem), null, sel(elem), true);
		}
		delete oldIdxs[ch.guid]; //will use this for deletion later
	    }
	    //Append a new element
	    else if(oldIdxs[ch.guid] === undefined){
		console.log("No old child with this ID", force);
		_render(ch, sel(elem), null, null, false);
	    }
	    else {
		_render(ch, sel(elem), null, null, false);
	    }
	}
	//Remove any old elements we didn't encounter in the new list.
	for(idx in oldIdxs){
	    jQuery(sel(elem)).remove(sel(elem.oldChildren[oldIdxs[idx]]));
	}
    }

    //_changeCSS : Element -> Element -> m ()
    function _changeCSS(elem, oldElem){
	if(elem.spec.css === {} && oldElem.spec.css === {}) return; 
	var jq = jQuery(sel(elem));
	if(!oldElem){
	    for(k in elem.spec.css){ 
		jq.css(k, elem.spec.css[k]); 
	    }
	}
	else {
	    for(k in elem.spec.css){
		if(oldElem.spec.css[k] !== elem.spec.css[k]){
		    jq.css(k, elem.spec.css[k]);
		}
	    }
	}
    }

    //_bind : Signal Element -> m ()
    // TODO: rebind elem output signals that only became 
    //   depended upon after the most recent _bind. 
    function _bind(elem){
	for(binding in bindings[elem.guid]){
	    if(elem.bind[binding] === undefined) throw "Binding "+binding+" is not provided for element "+elem.guid; 
	    //sig.__.addSFN(elem.bind[binding]);
	    sig.__.reconnect(elem.bind[binding](sel(elem)), bindings[elem.guid][binding]);
	}
	console.log("Rebinding", elem);
    }

    var elemStore = {};
    //_render : Element -> Selector ->
    //          Element -> Selector ->
    //          Bool -> Bool -> m ()
    function _render(elem, selector, oldElem, oldSel, replace, firstRender){
	if(selector != oldSel) jQuery(sel(elem)).remove();

	oldElem = elemStore[elem.guid];
	elemStore[elem.guid] = sig.__.copy(elem); 

	if(oldElem) elem.oldChildren = oldElem.children; 
	
	elem.genChanged = true; 
	elem.cssChanged = true;

	if(oldElem) {
	    elem.genChanged = 
		elem.spec.gen !== oldElem.spec.gen &&
		elem.spec.gen(elem.spec) !== oldElem.spec.gen(elem.spec);
	    if(elem.spec.css !== undefined && oldElem.spec.css !== undefined){
		//Surprisingly the fastest way to compare objects for equality
		cssChanged = JSON.stringify(elem.spec.css) !== 
		    JSON.stringify(oldElem.spec.css) 
	    }
	}

	if(elem.genChanged === true || selector != oldSel || firstRender){
	    var g = generate(elem);
	    var updated = false; 
	    if(!replace || selector != oldSel || firstRender){
		jQuery(g).attr('id', sel(elem, "")).addClass("wg_widget").appendTo(jQuery(selector));
		_bind(elem);
		_updateChildren(elem, true);
		updated = true; 
	    }
	    else {
		var gp = jQuery(g).html(); //extract inner contents
		var se = jQuery(sel(elem));
		var children = se.children(".wg_widget").remove();
		se.html(gp); 
		se.append(children);
	    }
	    
	    if(!updated) _updateChildren(elem, false);
	    _changeCSS(elem, oldElem);
	}
	else {
	    _updateChildren(elem, false);
	    if(elem.cssChanged) _changeCSS(elem, oldElem);
	}
	if(!oldElem || elem.spec.visible !== oldElem.spec.visible){
	    if(elem.spec.visible) jQuery(sel(elem)).show();
	    else jQuery(sel(elem)).hide();
	}
	if(!oldElem || elem.spec.visible !== oldElem.spec.visible){
	    if(elem.spec.focus) jQuery(sel(elem)).focus();
	    else jQuery(sel(elem)).blur();
/*	    if(bindings[elem.guid] && bindings[elem.guid].focus){
		sig.__.asyncInput(bindings[elem.guid].focus.backward[0]
				  , elem.spec.focus);
	    }*/
	}
    }

    //render : Signal Element -> Signal Selector -> m ()
    function render(elem, sel){
	var rendered = false; //may want to use FRP construct rather than closure
	                      // use this to force a re-render the first time.
	function wrap(orig, loop){
	    var z = _render(orig[0], orig[1], loop[0], loop[1], true, !rendered);
	    rendered = true;
	}
	var orig = sig.combine([elem, sel]).lift(function(x){ return x; });
	var r = sig.compose2(orig, orig.loop(), sig.lift(wrap));
	return r; 
    }
    
    //generate : Element -> HTML
    function generate(elem){
	return elem.spec.gen();
    }

    function defaultBindings(guid){
	return {
	    "clicked" : function(sel){
		return sig.__.asyncInputSig(function(n){
		    sig.__.asyncInput(n, false);
		    var clicked = false; 
		    jQuery(sel).mousedown(function(e){
			clicked = true; 
			sig.__.asyncInput(n, true);
		    });
		    jQuery(document).mouseup(function(e){ 
			if(clicked === true)
			    sig.__.asyncInput(n, false);
			clicked = false;
		    });
		});
	    }
	    ,"mouseover" : function(sel){
		return sig.__.asyncInputSig(function(n){
		    sig.__.asyncInput(n, false);
		    jQuery(sel).mouseover(function(e){
			sig.__.asyncInput(n, true);
		    });
		    jQuery(sel).mouseleave(function(e){ 
			sig.__.asyncInput(n, false);
		    });
		});
	    }
	    ,"focus" : function(sel){
		return sig.__.asyncInputSig(function(n){
		    sig.__.asyncInput(n, false);
		    jQuery(sel).focus(function(e){
			sig.__.asyncInput(n, true);
		    });
		    jQuery(sel).blur(function(e){ 
			sig.__.asyncInput(n, false);
		    });
		});
	    }

	    ,"val" : function(sel, def){
		return sig.__.asyncInputSig(function(n){
		    sig.__.asyncInput(n, jQuery(sel).val());
		    jQuery(sel).bind('keyup change', (function(e){
			sig.__.asyncInput(n, jQuery(sel).val());
		    }));
		}, def);
	    }
	}
    }

    function typeAssert(type, obj, caller){
	caller = caller || "Unknown function";
	if(typeof(obj) !== type && obj.type !== type)
	    throw caller + "requires an argument of type "+type;
	return true; 
    }

    function elemGuid(sig){
	return instance + "_" + sig.guid; 
    }

    function elemChildren(chld){
	var sChildren; 
	if(chld === undefined) sChildren = sig.constant([]);
	else if(chld[0] !== undefined){
	    sChildren = sig.combine(chld, true);
	}
	else { sChildren = chld; }
	return sChildren;
    }

    function elem(chld){
	function _elem(ch){
	    return {
		type : 'Element',
		guid : elemGuid(this),
		children : ch,
		spec : defaultWS(),
		bind : defaultBindings()
	    }	
	}
	return elemChildren(chld).lift(_elem); 
    }

    sig.__.SFN.prototype.children = function(chld){ 
	function children(elem, chlds){
	    typeAssert("Element", elem, "wg.children");
	    elem.children = chlds;
	    return elem; 
	}
	var e = elemChildren(chld);
	return sig.compose2(this, e, sig.lift(children));
    }; 


    sig.__.SFN.prototype.bind = function(name, s){ 
	function rebind(elem){
	    elem.bind[name] = function(__){ return s }; 
	    return elem; 
	}
	return this.lift(rebind); 
    }; 

    //clicked : Signal Element -> Signal Bool
    //mouseover : Signal Element -> Signal Bool
    var simpleOutputs = ["clicked", "mouseover", "val", "focus"];
    simpleOutputs.forEach(function(name){
	sig.__.SFN.prototype[name] = function(def){
	    return this.lift(function(e){ 
		return _registerBinding(e.guid, name, def); }).join(); 
	}
    });
    
    sig.__.SFN.prototype.clickToggle = function(){
	return this.clicked().toggle()
    };

    sig.__.SFN.prototype.isVisible = function(){
	return this.lift(function(e){
	    typeAssert("Element", e, "wg.isVisible");
	    return e.spec.visible; 
	});
    };
    

    //mappend for defaults
    // merge : {} -> {} -> {}
    function merge(o1, o2){
	if(o1 === undefined){ o1 = {}; }
	if(typeof(o1) !== "object" || typeof(o2) !== "object") 
	    throw "mplus must be passed two objects";
	var res = {};
	for(k in o1){ res[k] = o1[k];}
	for(k in o2){
	    if(typeof(o2[k]) === "object") res[k] = mplus(o1[k], o2[k]);
	    else res[k] = o2[k];
	}
	return res;
    }
    sig.__.SFN.prototype.merge = function(objsig){ 
	return sig.compose2(this, objsig, sig.lift(merge));
    };

/*    function spec(){
	return sig.constant(defaultWS()); 
    }*/

    sig.__.SFN.prototype.css = function(objSig){ 
	function cssMerge(ws, newCSS){
	    typeAssert("Element", ws, "wg.css");
	    typeAssert("object", newCSS, "wg.css");
	    ws.spec.css = merge(ws.spec.css, newCSS);
	    return ws; 
	}
	return sig.compose2(this, objSig, sig.lift(cssMerge));
    };

    sig.__.SFN.prototype.hideOn = function(hideSig){ 
	function hide(elem, hidden){
	    typeAssert("Element", elem, "wg.hideOn");
	    if(hidden === true){ elem.spec.visible = false; }
	    else { elem.spec.visible = true; }
	    return elem; 
	}
	return sig.compose2(this, hideSig, sig.lift(hide));
    }; 

    sig.__.SFN.prototype.focusOn = function(focusSig){ 
	function focus(elem, focus){
	    typeAssert("Element", elem, "wg.focusOn");
	    if(focus === true){ elem.spec.focus = true; }
	    else { elem.spec.focus = false; }
	    return elem; 
	}
	return sig.compose2(this, focusSig, sig.lift(focus));
    }; 


    sig.__.SFN.prototype.dynGen = function(genSig){ 
	function genMerge(elem, newGen){
	    typeAssert("Element", elem, "wg.gen");
	    typeAssert("function", newGen, "wg.gen");
	    elem.spec.gen = newGen;
	    return elem; 
	}
	return sig.compose2(this, genSig, sig.lift(genMerge));
    }; 

    sig.__.SFN.prototype.gen = function(genSig){ 
	var g = genSig.lift(function(c){ return function(x){ return c } });
	return this.dynGen(g); 
    }; 

    sig.__.SFN.prototype.constGen = function(genString){ 
	var g = sig.constant(function(x){ return genString });
	return this.dynGen(g); 
    }; 
    function constGen(str){
	return elem().constGen(str); 
    }

    
    sig.__.SFN.prototype.cloneElem = function(){ 
	function clone(elem){
	    typeAssert("Element", elem, "wg.cloneElem");
	    var e2 = elem.copy();
	    e2.guid = elemGuid(this);
	    return e2; 
	}
	return this.lift(clone);
    }; 



    function toggleField(){
	/** Slider Object **/
	var slider = elem();
	var sliderBar = constGen("<div class='slideBar secondary'></div>");
	var sliderEndValSig = sliderBar.clicked().toggle().lift(function(z){ 
	    if(z === true) return 1.0;
	    return 0; 
	});
	var spring = physics.springify(8, 80, sliderEndValSig);
	function sliderGen(clicked){
	    return "<div class='slider primary'>"+(clicked ? "On" : "Off")+"</div>";
	};
	function slidCSS(springpos){
	    return { 'margin-left' : 66 * springpos + "%" };
	}
	var state = sliderBar.clicked().toggle();
	slider = slider.gen(state.lift(sliderGen))
	    .css(spring.lift(slidCSS))
	return sliderBar.children([slider]).bind("val", state); 
    }


    function inlineField(value){
	var input = elem().constGen(
	    "<input class='inlineEdit fieldInput formField' value='"+value+"' />")
	var displayGen = input.val().def("Value").lift(function(v){ 
	    return "<div class='inlineEdit'>"+v+"</div>"; });
	var displayElem = elem().gen(displayGen);
	var inputVisible =  sig.or(
	    input.focus().throttle(50)
	    ,displayElem.clicked().throttle(50)
	);
	var display = displayElem.hideOn( inputVisible );
	input = input
	    .focusOn( inputVisible ).hideOn( inputVisible.not() )
	return elem([input, display]).bind("val", input.val());
    }

    function inputField(value){
	var input = elem().constGen(
	    "<input type='text' class='inlineEdit fieldInput formField' value='"+value+"' />")
	return input;
    }

    function hiddenField(value){
	var input = elem().constGen(
	    "<input type='hidden' value='"+value+"' />")
	return input;
    }

    function passwordField() {
	var input = elem().constGen(
	    "<input type='password' class='fieldInput'/>");
	return input;
    }

    function textareaField(value){
	var input = elem().constGen(
	    "<textarea class='fieldInput formField' placeholder='"+value+"'></textarea>");
	    return input;
    }

    
    function dropdownField(ops, def){
	var selectDropdown = constGen("<div class='selectDropdown formField'></div>");
	var options = constGen("<ul class='options'></ul>");
	var optionDisplays = sig.Aggregator();
	var outputSigs = [];

	for(k in ops){
	    (function(){ // Creating a closure for _k and _v
		var optionDisplay = constGen("<li class='option fieldInput secondary'>"+ops[k]+"</li>");
		var _k = k;
		var _v = ops[k];
		var output = optionDisplay.clicked().toggle().lift(
		    function(clicked){
			return { clicked: clicked, k:_k, v:_v }
		    });
		optionDisplays.aggregate(optionDisplay);
		outputSigs.push(output);
	    })();
	}
	var chosen = sig.mostRecent(outputSigs);
	var chosenContent = chosen.lift(
	    function(x){ return "<div class='chosen primary fieldInput'>"+x.v+"</div>"; });
/*	var chosenContent2 = sig.mostRecent(outputSigs).lift(
	    function(x){ console.log("ChosenConten2t", x); return "<div class='chosen primary fieldInput'>"+x.v+"</div>"; });*/
	
	var chosenDrop = constGen("<i class='fa dropdown-icon fa-chevron-down'></i>");
	var chosenDisplay = elem([chosenDrop]).gen(chosenContent); 
	options = options.hideOn(
	    sig.mostRecent([chosenDisplay.clicked()
			    ,options.clicked()]
			  ).toggle().not()
	);

	return selectDropdown
	    .children([chosenDisplay, options.children(optionDisplays)])
	    .bind("val", chosen)
	    .bind("clicked", chosenDisplay.clicked());
    }

    function statusIndicator(loading, success){
	function status(load, succ){
	    if(load){
		displaying = false;
		return "<div style='display:inline-block;'><div class='fa fa-spinner fa-spin'></div></div>";
	    }
	    else if(succ.decayed && succ.value === true){
		return "<div style='display: inline-block;'></div>";
	    }
	    else {
		if(succ.value === true)
		    return "<div style='display:inline-block;'><div class='fa fa-check'></div></div>";
		else
		    return "<div style='display:inline-block;'><div class='fa fa-minus-circle'></div></div>";
	    }
	}
	var gen = sig.compose2(loading, success.decay(500), sig.lift(status)); 
	return elem().gen( gen );
    }

    function button(valueSig){
	var gen = valueSig.lift(function(v){ 
	    return "<button class='formField primary'>"+v+"</button>"; });
	return elem().gen(gen);
    }

    function buttonGroup(ops, def){
	
    }

    return {
	defaultWS : defaultWS,
	elem : elem,
	render : render,
	constGen : constGen,
	merge : merge,
	button : button,
	statusIndicator : statusIndicator,
	buttonGroup : buttonGroup,
	inlineField : inlineField,
	inputField : inputField,
	textareaField : textareaField,
	passwordField: passwordField,
	hiddenField : hiddenField,
	toggleField : toggleField,
	dropdownField : dropdownField,
    }

}

window.wg = wgSig();
