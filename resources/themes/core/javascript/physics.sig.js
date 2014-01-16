function physicsSig(s, w){
    var sig = s;
    var wg = w;
    if(sig === undefined){ 
	if(window.sig === undefined) throw "physics.sig.js requires sig.js";
	sig = window.sig; 
    }

    if(wg === undefined){ 
	if(window.wg === undefined) throw "physics.sig.js requires wg.sig.js";
	wg = window.wg; 
    }

    
    // simulation takes an object of initial parameters,
    //   a Signal of an object of external parameters,
    //   and runs simStep at each time step, passing it
    //   either initParams or its last output and
    //   the contents of externalParamSig. 
    //   Its output is used to generate input for the next time step. 
    function simulation(initParams, externalParamSig, simStep){
	var lastOutput = initParams; 
	function sim(externalParams){
	    var output = simStep(lastOutput, externalParams);
	    lastOutput = output;
	    return output; 
	}
	return externalParamSig.lift(sim);
    }
    
    function spring(paramSig){
	//We assume rest position is @ 0. 

	var restSpeedThreshhold = 0.005; 
	function simStep(t0, t1){
	    var dt = (t1.time - t0.time) / 400;
	    k = t1.k;
	    friction = t1.friction; 
	    endVal = t1.endVal; 

	    //Last timestep's acceleration = force / (mass = 1) = kx - fv
            a0 = (k * (endVal - t0.pos)) - friction * t0.velocity;
	    //Rate of change of (Position = dt*x0 + v0*dt^2) 
		// = x0 + v0*dt*(1/2)
            dxdt0 = t0.pos + t0.velocity * dt * 0.5;
	    //This timestep's Rate of change of (Velocity = v0 + a0 * dt^2) 
		// = v0 + a0 * dt * 0.5
            dvdt0 = t0.velocity + a0 * dt * 0.5;
            a1 = (k * (endVal - dxdt0)) - friction * dvdt0;
	    dxdt = t0.velocity + a0 * dt * dt; 
	    dvdt = a1; 
	    if(dt > 0.1 || Math.abs(t0.velocity + dvdt * dt) < restSpeedThreshhold){
		return {
		    pos: t0.pos,
		    velocity: t0.velocity,
		    time: t1.time
		} 
	    }
	    return {
		pos: t0.pos + dxdt * dt,
		velocity: t0.velocity + dvdt * dt,
		time: t1.time
	    }
	    return ret; 



            aAcceleration = (k * (endVal - t0.pos)) - friction * t0.velocity;
	    

            dxdt = t0.pos + t0.velocity * dt * 0.5;
	    
	    //Last timestep's Rate of change of (Velocity = v0 + v * dt^2) 
		// = pos_0 + v * dt * 0.5
            dvdt_0 = t0.velocity + aAcceleration * dt * 0.5;
	    
	    //This timestep's acceleration ( = dvdt_1)
            dvdt_1 = (k * (endVal - dxdt)) - friction * dvdt_0;
	    v1 = t0.velocity + dvdt_1 * dt;
	    x1 = t0.pos + dxdt * dt; 

	    if(dt > 0.1 || Math.abs(v1) < restSpeedThreshhold){
		return {
		    pos: t0.pos,
		    velocity: t0.velocity,
		    time: t1.time
		} 
	    }
	    return {
		pos: x1,
		velocity: v1,
		time: t1.time
	    }
	    return ret; 

	}
	var paramSig2 = paramSig.merge(sig.Util.milliseconds.lift(function(x){ return { time : x } }));
	var initParams = {
	    pos : 0,
	    velocity: 0,
	    time : (new Date()).valueOf()
	}
	return simulation(initParams, paramSig2, simStep);
    }
    
    function springify(friction, tension, endValSig){
	var springParams = sig.ojoin({
	    k : tension
	    , endVal : endValSig
	    , friction : friction
	    , force : 0
	});
	return spring(springParams).lift(function(x){ return x.pos; });
    }
    return {
	spring: spring,
	springify: springify
    }
}

window.physics = physicsSig();
