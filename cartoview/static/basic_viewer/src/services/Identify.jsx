import FeaturesHelper from 'cartoview-sdk/helpers/FeaturesHelper'
import GeoJSON from 'ol/format/geojson'
import LayersHelper from 'cartoview-sdk/helpers/LayersHelper'
import axios from 'axios'
const geojsonFormat = new GeoJSON()
class FeatureIdentify {
	identify(map, evt) {
		const view = map.getView()
		const mapResolution = view.getResolution()
		const mapProjection = view.getProjection()
		const wmsLayers = LayersHelper.getLayers(map.getLayers().getArray()).reverse()
		const wfsPromise = new Promise((resolve) => {
			const layerFeatures = {}

			map.forEachFeatureAtPixel(evt.pixel, (feature, layer) => {
				const metadata = layer.get('metadata')
				const layer_name = metadata['name']
				if (layerFeatures[layer_name] === undefined) {
					layerFeatures[layer_name] = []
				}
				layerFeatures[layer_name].push(feature)
			})
			resolve(layerFeatures)
		})
		let identifyPromises = wmsLayers.map(
			(layer) => {
				const metadata = layer.get('metadata')
				const layerName = metadata["name"]
				const serverProxy = metadata["server_proxy"]
				let identifyPromiseHandler = new Promise((resolve, reject) => {
					const source = layer.getSource()
					const url = source.getGetFeatureInfoUrl(
						evt.coordinate, mapResolution, mapProjection, {
							"INFO_FORMAT": 'application/json',
							"FEATURE_COUNT": 10
						},
					)
					axios.get(`${serverProxy}${encodeURIComponent(url)}`).then(response => {
						const data = response.data
						if (data.features && data.features.length > 0) {
							const crs = data.features.length > 0 ?
								data.crs.properties.name.split(":").pop() : null
							FeaturesHelper.getCRS(crs).then(newCRS => {
								const features = geojsonFormat.readFeatures(data)
								resolve({ [layerName]: features })
							}, (error) => {
								reject(error)
							})
						} else {
							resolve({ [layerName]: [] })
						}
					}).catch(err => {
						console.error(`Layer ${layerName} => Feature Identify Error:`, err)
						resolve({ [layerName]: [] })
					})
				})
				return identifyPromiseHandler
			})
		return [wfsPromise, ...identifyPromises]
	}
}
export default new FeatureIdentify()