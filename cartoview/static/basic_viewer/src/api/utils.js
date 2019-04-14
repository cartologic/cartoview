export function getCRSFToken() {
	let csrfToken, csrfMatch = document.cookie.match(/csrftoken=(\w+)/)
	if (csrfMatch && csrfMatch.length > 0) {
		csrfToken = csrfMatch[1]
	}
	return csrfToken
}