// import * as mapActions from '../actions/map'

import { fetchServerLayers, fetchServers } from '../api'

import AddIcon from '@material-ui/icons/Add'
import ArrowBackSharpIcon from '@material-ui/icons/ArrowBackSharp'
import { BasicViewerContext } from '../context'
import DeleteIcon from '@material-ui/icons/Delete'
import FormControl from '@material-ui/core/FormControl'
import IconButton from '@material-ui/core/IconButton'
import InputLabel from '@material-ui/core/InputLabel'
import LegendService from '../services/Legend'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction'
import ListItemText from '@material-ui/core/ListItemText'
import MapConfigService from '../services/MapLoadService'
import MenuItem from '@material-ui/core/MenuItem'
import Pagination from "material-ui-flat-pagination"
import PropTypes from 'prop-types'
import React from 'react'
import Select from '@material-ui/core/Select'
import { connect } from 'react-redux'
import { withStyles } from '@material-ui/core/styles'

const styles = theme => ({
	divFlex: {
		display: 'flex',
		margin: '0px 10px'
	},
	controlFlex: {
		display: 'flex',
		margin: '0px 10px',
		'flex': '1',
		'flex-direction': 'column'
	},
	customPagination: {
		alignItems: 'center',
		display: 'flex',
		justifyContent: 'center'
	}
})
class AddLayers extends React.PureComponent {
	constructor(props) {
		super(props)
		this.state = {
			servers: [],
			layers: [],
			layersLoading: false,
			selectedServerId: -1,
			offset: 0,
			count: 0,
			limit: 25
		}
	}
	handleOffsetChange = (offset) => {
		this.setState({ offset }, () => this.getLayers())
	}
	addLayer = (layerJson) => {
		const { map, setStateKey, mapLayers } = this.context
		const service = new MapConfigService(map, {})
		const layer = service.generateLayerFromConfig(layerJson)
		if (layer) {
			map.addLayer(layer)
			setStateKey('mapLayers', [layer, ...mapLayers])
			Promise.all(LegendService.getLegends(map)).then(result => setStateKey('legends', result))
		}
	}
	deleteLayer = (layerJson) => {
		const { map, mapLayers, setStateKey } = this.context
		const { id } = layerJson
		map.getLayers().getArray().map(lyr => {
			const metadata = lyr.get('metadata')
			if (metadata && metadata.identifier === id) {
				map.removeLayer(lyr)
				setStateKey('mapLayers', mapLayers.filter(lyr => {
					const metadata = lyr.get('metadata')
					return metadata && metadata.name !== name
				}))
			}
		})
	}
	getLayers = () => {
		const me = this
		const { selectedServerId, limit, offset } = me.state
		if (selectedServerId > -1) {
			me.setState({ layersLoading: true }, () => {
				fetchServerLayers(selectedServerId, limit, offset).
					then(data => me.setState({
						layers: data.results,
						count: data.count,
						layersLoading: false
					})).
					catch(err => {
						me.setState({ count: 0, layers: [], layersLoading: false })
						console.error(err)
					})
			})

		}
	}
	handleChange = event => {
		let me = this
		me.setState({ [event.target.name]: event.target.value },
			() => this.getLayers())
	}
	layerMapExist = (id) => {
		const { map } = this.context
		const found = map.getLayers().getArray().filter(layer => {
			const metadata = layer.get('metadata')
			if (metadata && metadata.identifier === id) {
				return true
			}
			return false
		})
		if (found.length > 0) {
			return true
		}
		return false

	}
	componentDidMount() {
		fetchServers().then(servers => this.setState({ servers }))
	}
	handleDetailsExpand = () => {
		this.setState({ expanded: !this.state.expanded })
	}
	render() {
		const { classes, setComponent } = this.props
		const { servers, selectedServerId, layers, count, offset, limit } = this.state
		return (
			<div>
				<div className={classes.controlFlex}>
					<IconButton onClick={() => setComponent(null)}>
						<ArrowBackSharpIcon />
					</IconButton>
					<FormControl className={classes.divFlex}>
						<InputLabel htmlFor="server-select">Server</InputLabel>
						<Select
							value={selectedServerId}
							onChange={this.handleChange}
							inputProps={{
								name: 'selectedServerId',
								id: 'server-select',
							}}
						>
							<MenuItem value={-1}>
								<em>{"------"}</em>
							</MenuItem>
							{servers.length > 0 && servers.map(server => {
								return <MenuItem key={server.id} value={server.id}>{server.title}</MenuItem>
							})}
						</Select>
					</FormControl>
				</div>
				<List>
					{layers.map(layer => <ListItem key={layer.id}>
						<ListItemText primary={layer.title} secondary={layer.layer_type} />
						<ListItemSecondaryAction>
							{!this.layerMapExist(layer.id) && <IconButton onClick={() => this.addLayer(layer)} aria-label="Add">
								<AddIcon />
							</IconButton>}
							{this.layerMapExist(layer.id) && <IconButton onClick={() => this.deleteLayer(layer)} aria-label="Add">
								<DeleteIcon />
							</IconButton>}
						</ListItemSecondaryAction>
					</ListItem>)}
				</List>
				<Pagination
					classes={{ 'root': classes.customPagination }}
					limit={limit}
					offset={offset}
					total={count}
					onClick={(e, offset) => this.handleOffsetChange(offset)}
				/>
			</div >
		)
	}
}
AddLayers.propTypes = {
	classes: PropTypes.object.isRequired,
	reduxMap: PropTypes.object.isRequired,
	setComponent: PropTypes.func.isRequired,
}
AddLayers.contextType = BasicViewerContext
const mapStateToProps = (state) => {
	return {
		reduxMap: state.map,
	}
}

const App = connect(mapStateToProps, null)(AddLayers)
export default withStyles(styles)(App)