//Automatically replaces forms on this page
// with sig.js forms


var inputTypes = {
    "select" : function(z){
	var ops = {};
	z.find('option').each(function(){
	    var v = jQuery(this).attr('value');
	    if(v.length) ops[v] = jQuery(this).html(); 
	});
	return wg.dropdownField(ops);
    }
    ,"input[type=text]" : function(z){
	return wg.inputField(z.val()); 
    }
    ,"input[type=hidden]" : function(z){
	return wg.hiddenField(z.val()); 
    }
    ,"textarea" : function(z){
	return wg.textareaField(z.val()); 
    }
    ,"input[type=password]" : function(z) {
	return wg.passwordField();
    }
}

function labelElem(contents, name){
    return wg.constGen("<label for="+name+">"+contents+"</label>");
}

var nForms = 0; 
function autoform(){
    jQuery('form').each(function(){
	var form = jQuery(this);
	var elems = [];
	var values = {};
	var submitValue = form.find(":submit").val() || "Submit"; //Might need custom message on submit button

	for(k in inputTypes){
		var key = k; 
	    form.find(k).each(function(){

		var name = jQuery(this).attr('name');
		var label = form.find("label[for="+jQuery(this).attr('id')+"]");
		if(label.length) elems.push( labelElem(label.html(), name) );
		var fun = inputTypes[key];
		var elem = inputTypes[key](jQuery(this));
		if(key === "select")
		    values[name] = elem.val().prop("k");
		else
		    values[name] = elem.val();
		elems.push(elem);
	    });
	}
	var button = wg.button(sig.constant(submitValue)); 	
	elems.push(button);
	var httpRes = sig.ojoin(values)
	    .onChange(button.clicked().toggle().throttle(50))
	    .throttle(1000).http(sig.constant(form.attr('action')));
	var loading = wg.statusIndicator(httpRes.prop("inProgress")
					 ,httpRes.prop("success"));
	elems.push(loading);
	var id = 'autoform_'+(nForms++);
	form.after("<div id='" + id + "'></div>");
	form.hide();
	wg.render(wg.elem(elems), sig.constant("#"+id));

    });
}




jQuery(document).ready(function(){
    autoform();
    sig.run();

});
