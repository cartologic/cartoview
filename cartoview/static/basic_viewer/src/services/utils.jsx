export function resolveURL(url, base) {
	if ('string' !== typeof url || !url) {
		return null; // wrong or empty url
	}
	else if (url.match(/^[a-z]+\:\/\//i)) {
		return url; // url is absolute already 
	}
	else if (url.match(/^\/\//)) {
		return 'http:' + url; // url is absolute already 
	}
	else if (url.match(/^[a-z]+\:/i)) {
		return url; // data URI, mailto:, tel:, etc.
	}
	else if ('string' !== typeof base) {
		var a = document.createElement('a');
		a.href = url; // try to resolve url without base  
		if (!a.pathname) {
			return null; // url not valid 
		}
		return 'http://' + url;
	}
	else {
		base = resolve(base); // check base
		if (base === null) {
			return null; // wrong base
		}
	}
	var a = document.createElement('a');
	a.href = base;

	if (url[0] === '/') {
		base = []; // rooted path
	}
	else {
		base = a.pathname.split('/'); // relative path
		base.pop();
	}
	url = url.split('/');
	for (var i = 0; i < url.length; ++i) {
		if (url[i] === '.') { // current directory
			continue;
		}
		if (url[i] === '..') { // parent directory
			if ('undefined' === typeof base.pop() || base.length === 0) {
				return null; // wrong url accessing non-existing parent directories
			}
		}
		else { // child directory
			base.push(url[i]);
		}
	}
	return a.protocol + '//' + a.hostname + base.join('/');
}