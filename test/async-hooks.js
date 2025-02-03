'use strict';

const { AsyncResource } = require('async_hooks');
const Fiber = require('fibers');

class TestResource extends AsyncResource {
	constructor() {
		super('TestResource');
	}

	run(cb) {
		this.runInAsyncScope(cb);
	}
}

let tmp = Fiber(function() {
	let resource = new TestResource;
	resource.run(function() {
		Fiber.yield();
	});
});
tmp.run();
setTimeout(function() {
	tmp.run();
	console.log('pass');
}, 5);
