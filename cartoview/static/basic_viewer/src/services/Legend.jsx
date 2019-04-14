import Group from 'ol/layer/group'
import mergeImages from 'merge-images';
import { resolveURL } from './utils'
import { sourceMapping } from '../services/MapLoadService'
class LegendService {
	getOGCWMSLegend(metadata, url) {
		let serverProxy = metadata['server_proxy']
		let wmsURL = url
		let query = {
			'REQUEST': 'GetLegendGraphic',
			'VERSION': '1.0.0',
			'FORMAT': 'image/png',
			"LAYER": metadata['name']
		}
		wmsURL = new URL('', wmsURL)
		const keys = Object.keys(query)
		for (let index = 0; index < keys.length; index++) {
			const key = keys[index]
			const value = query[key]
			wmsURL.searchParams.append(key, value)

		}
		wmsURL = wmsURL.href
		if (serverProxy) {
			wmsURL = `${serverProxy}${encodeURIComponent(wmsURL)}`
		}
		return wmsURL
	}
	getForMerge(src) {
		var promiseObj = new Promise((resolve, reject) => {
			var i = new Image();
			i.onload = function () {
				resolve({ src, x: 0, y: i.height })
			}
			i.src = src
		})
		return promiseObj

	}
	getArgisLegend(legendJson) {
		var promiseObj = new Promise((resolve, reject) => {
			var canvas = document.createElement('canvas')
			var context = canvas.getContext("2d")
			// const height = legendJson.height || 50
			// const width = legendJson.height || 100
			// canvas.height = height
			// canvas.width = width
			var image = new Image()
			function getbase64() {
				canvas.toBlob(function (blob) {
					var reader = new FileReader()
					reader.readAsDataURL(blob)
					reader.onloadend = function () {
						const base64data = reader.result
						resolve(base64data)
					}
					canvas.parentNode.removeChild(canvas)
				}, 'image/png')
			}
			image.onload = function () {
				context.drawImage(this, 0, 0)
				context.fillStyle = "black"
				context.textBaseline = 'middle'
				context.font = "15px 'sans-serif'"
				const textHeight = image.height / 2
				const textWidth = image.width + 5
				context.fillText(legendJson.label, textWidth, textHeight)
				getbase64()
			}
			// set src last (recommend to use relative paths where possible)
			image.src = `data:${legendJson.contentType};base64,${legendJson.imageData}`
			document.body.appendChild(canvas)
		})
		return promiseObj

	}
	getLegendURL(layer) {
		const metadata = layer.get('metadata')
		let serverProxy = null
		if (metadata) {
			serverProxy = metadata['server_proxy']
		}
		var promiseObj = new Promise((resolve, reject) => {
			const source = layer.getSource()
			let url = this.getLayerURL(layer)
			if (source instanceof sourceMapping['TileWMS'] || source instanceof sourceMapping['TileWMS']) {
				resolve(this.getOGCWMSLegend(metadata, url))
			} else if (source instanceof sourceMapping['TileArcGISRest'] || source instanceof sourceMapping['ImageArcGISRest']) {
				url = url.endsWith("/") ? `${url}legend?f=json` : `${url}/legend?f=json`
				url = `${serverProxy}${encodeURIComponent(url)}`
				var imagesPromises = []
				var images = []
				fetch(url).then(resp => resp.json()).then(data => {
					data.layers.map(lyr => {
						lyr.legend.map(leg => {
							imagesPromises.push(this.getArgisLegend(leg))
						})
					})
					Promise.all(imagesPromises).then(values => {
						for (let index = 0; index < values.length; index++) {
							const element = values[index]
							images.push({ src: element, x: 0, y: 0 })
						}
						let current = 0
						for (let index = 0; index < images.length; index++) {
							const element = images[index]
							element.y = current + 25
							current = element.y
						}
						mergeImages(images, {
							height: (25 * images.length) + 50,
							width: 200
						}).then(b64 => {
							resolve(b64)
						})
					})
				})
			}
		});

		return promiseObj
	}
	getLayerURL(layer) {
		const source = layer.getSource()
		let layerURL = null
		try {
			layerURL = source.getUrls()[0]
		} catch (err) {
			layerURL = source.getUrl()
		}
		let url = resolveURL(layerURL)
		return url
	}
	getLayers(mapLayers) {
		let children = []
		mapLayers.forEach((layer) => {
			if (layer instanceof Group) {
				children = children.concat(this.getLayers(layer.getLayers()))
			} else if (layer.getVisible()) {
				children.push(layer)
			}
		})
		return children
	}
	getLegendObj(layer) {
		const metadata = layer.get('metadata')
		let promiseObj = new Promise((resolve, reject) => {
			this.getLegendURL(layer).then(url => {
				let legend = {
					layer: metadata['name'],
					url
				}
				resolve(legend)
			})
		})
		return promiseObj
	}
	getLegends(map) {
		const layers = this.getLayers(map.getLayers().getArray()).reverse()
		let legendsPromises = []
		for (let index = 0; index < layers.length; index++) {
			const lyr = layers[index]
			const source = lyr.getSource()
			if (source instanceof sourceMapping['TileArcGISRest'] || source instanceof sourceMapping['ImageArcGISRest'] || source instanceof sourceMapping['TileWMS'] || source instanceof sourceMapping['TileWMS']) {
				legendsPromises.push(this.getLegendObj(lyr))
			}
		}
		return legendsPromises
	}
}
export default new LegendService()
