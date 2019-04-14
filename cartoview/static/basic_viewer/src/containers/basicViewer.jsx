import "@babel/polyfill/noConflict"
import '../css/base.css'
import 'ol/ol.css'
import '../css/popup.css'

import { createMap, fetchMapById, mapJsonSerializer, saveMap, saveMapThumbnail } from '../api'

import BasicViewerHelper from 'cartoview-sdk/helpers/BasicViewerHelper'
import { BasicViewerProvider } from '../context'
import ContentGrid from '../components/ContentGrid'
import FeatureIdentify from '../services/Identify'
import FeaturesHelper from 'cartoview-sdk/helpers/FeaturesHelper'
import LegendService from '../services/Legend'
import MapConfigService from '../services/MapLoadService'
import Overlay from 'ol/overlay'
import { Provider } from 'react-redux'
import React from 'react'
import ReactDOM from 'react-dom'
import proj from 'ol/proj'
import proj4 from 'proj4'
import store from '../store'

proj.setProj4(proj4)

class BasicViewer extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            map: BasicViewerHelper.getMap(),
            drawerOpen: false,
            featureIdentifyLoading: false,
            featureIdentifyResult: [],
            showPopup: false,
            activeFeature: 0,
            legends: [],
            mapSaving: false,
            mapLayers: [],
            mouseCoordinates: [0, 0],
            mapLoading: false,
            currentMap: {
                title: "No Title Provided",
                description: "No Description Provided"
            },
        }
    }
    setStateKey = (key, value, callback = () => { }) => {
        this.setState({ [key]: value }, () => { callback() })
    }
    changeShowPopup = () => {
        const { showPopup } = this.state
        this.setState({ showPopup: !showPopup })
    }
    nextFeature = () => {
        const { activeFeature } = this.state
        const nextIndex = activeFeature + 1
        this.setState({ activeFeature: nextIndex })
    }
    previousFeature = () => {
        const { activeFeature } = this.state
        const previuosIndex = activeFeature - 1
        this.setState({ activeFeature: previuosIndex })
    }
    getMapThumbnail = () => {
        let imagePromise = new Promise((resolve, reject) => {
            const { map } = this.state
            map.once('postcompose', function (event) {
                var canvas = event.context.canvas;
                canvas.toBlob(function (blob) {
                    var file = new File([blob], 'map.png', { type: 'image/png', lastModified: Date.now() })
                    resolve(file)
                })
            });
            map.renderSync();
        })
        return imagePromise
    }
    toggleDrawer = () => {
        const { drawerOpen } = this.state
        this.setState({ drawerOpen: !drawerOpen })
    }
    save = () => {
        const { currentMap, map } = this.state
        const view = map.getView()
        const projection = view.getProjection().getCode()
        const zoom = view.getZoom()
        const rotation = view.getRotation()
        const center = view.getCenter()
        let layers = []
        let mapLayers = [...map.getLayers().getArray()]
        mapLayers = mapLayers.reverse()
        for (let index = 0; index < mapLayers.length; index++) {
            const layer = mapLayers[index];
            const metadata = layer.get('metadata')
            if (metadata) {
                layers.push(metadata.identifier)
            }
        }
        let savePromises = []
        let data = {
            title: currentMap.title,
            description: currentMap.description,
            projection,
            zoom,
            rotation,
            center,
            layers
        }
        if (currentMap.id) {
            savePromises.push(saveMap(currentMap.id, JSON.stringify(data)))
            this.getMapThumbnail().then(thumb => {
                let formdata = new FormData()
                formdata.append('thumbnail', thumb)
                savePromises.push(saveMapThumbnail(currentMap.id, formdata))
            })
            Promise.all(savePromises).then(results => this.setState({ mapSaving: false }))
        } else {
            createMap(JSON.stringify(data)).then(resp => {
                if (resp.status < 400) {
                    this.setState({ currentMap: resp.data })
                    this.getMapThumbnail().then(thumb => {
                        let formdata = new FormData()
                        formdata.append('thumbnail', thumb)
                        savePromises.push(saveMapThumbnail(resp.data.id, formdata))
                    })
                }
            })
        }
    }
    saveMap = () => {
        this.setState({ mapSaving: true }, this.save)
    }
    loadMap = (mapJson) => {
        const { map } = this.state
        let service = new MapConfigService(map, mapJson)
        service.load(() => {
            let layers = map.getLayers().getArray()
            layers = [...layers].reverse().filter(layer => {
                const metadata = layer.get('metadata')
                if (metadata && metadata['name'] !== undefined) {
                    return true
                }
                return false
            })
            this.setState({ mapLayers: layers })
            Promise.all(LegendService.getLegends(map)).then(result => this.setState({ legends: result }))
        })
    }
    componentDidMount() {
        const { map } = this.state
        if (window.mapId) {
            fetchMapById(window.mapId).then(response => {
                let data = response.data
                const transformedData = mapJsonSerializer(data)
                this.setState({ currentMap: data }, () => {
                    this.loadMap(transformedData)
                })
            })
        }
        this.overlay = new Overlay({
            autoPan: true,
            autoPanAnimation: {
                duration: 250
            },
            positioning: 'center-center'
        })
        map.addOverlay(this.overlay)
        map.on('singleclick', (evt) => {
            if (this.overlay) {
                this.overlay.setElement(undefined)
            }
            this.setState({
                featureIdentifyLoading: true,
                activeFeature: 0,
                featureIdentifyResult: [],
                showPopup: false,
                mouseCoordinates: evt.coordinate,
            }, () => this.identify(evt))
        })
    }
    zoomToExtent = (extent, projection = 'EPSG:4326') => {
        let { map } = this.state
        FeaturesHelper.getCRS(projection.split(":").pop()).then(newCRS => {
            const transformedExtent = BasicViewerHelper.reprojectExtent(extent, map, projection)
            BasicViewerHelper.fitExtent(transformedExtent, map)
        })
    }
    addOverlay = (node) => {
        const { activeFeature, featureIdentifyResult, mouseCoordinates } =
            this.state
        let position = mouseCoordinates
        if (featureIdentifyResult && featureIdentifyResult.length > 0) {
            const currentFeature = featureIdentifyResult[activeFeature]
            const geometry = currentFeature.getGeometry()
            position = FeaturesHelper.getGeometryCenter(geometry)
        }
        this.overlay.setElement(node)
        this.overlay.setPosition(position)
    }
    getContextValue = () => {
        return {
            ...this.state,
            toggleDrawer: this.toggleDrawer,
            nextFeature: this.nextFeature,
            previousFeature: this.previousFeature,
            changeShowPopup: this.changeShowPopup,
            addOverlay: this.addOverlay,
            setStateKey: this.setStateKey,
            zoomToExtent: this.zoomToExtent,
            saveMap: this.saveMap
        }
    }
    identify = (evt) => {
        const { map } = this.state
        Promise.all(FeatureIdentify.identify(map, evt)).then(featureGroups => {
            let features = []
            for (let g = 0, gg = featureGroups.length; g < gg; g++) {
                const layers = Object.keys(featureGroups[g])
                for (let l = 0, ll = layers.length; l < ll; l++) {
                    const layer = layers[l]
                    let newFeatures = featureGroups[g][layer].map(f => {
                        f.set('layerName', layer)
                        return f
                    })
                    features = [...features, ...newFeatures]
                }
            }
            this.setState({
                featureIdentifyLoading: false,
                activeFeature: 0,
                featureIdentifyResult: features,
                showPopup: true,
            })
        })
    }
    render() {
        return (
            <Provider store={store}>
                <React.Fragment>
                    <BasicViewerProvider value={this.getContextValue()}>
                        <ContentGrid />
                    </BasicViewerProvider>
                </React.Fragment>
            </Provider>
        )
    }
}
var elem = document.getElementById("basicviewer-app")
if (!elem) {
    elem = document.createElement('div', { "id": "basicviewer-app" })
    document.body.prepend(elem)
}
ReactDOM.render(<BasicViewer />, elem)
if (module.hot) {
    module.hot.accept()
}