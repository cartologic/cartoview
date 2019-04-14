import 'react-input-range/lib/css/index.css'

import { SortableContainer, SortableElement, SortableHandle } from 'react-sortable-hoc'

import { BasicViewerContext } from '../context'
import Checkbox from '@material-ui/core/Checkbox'
import DragHandleIcon from '@material-ui/icons/DragHandle'
import DropDown from './DropDown'
import InputRange from 'react-input-range'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListSubheader from '@material-ui/core/ListSubheader'
import MenuItem from '@material-ui/core/MenuItem'
import { Message } from './CommonComponents'
import Paper from '@material-ui/core/Paper'
import PropTypes from 'prop-types'
import React from 'react'
import { arrayMove } from 'react-sortable-hoc'
import { withStyles } from '@material-ui/core/styles'

const DragHandle = SortableHandle(() => <DragHandleIcon />)
const styles = theme => ({
	legendsPaper: {
		padding: theme.spacing.unit * 2,
	}
})
const LayerItem = SortableElement(({ layer, layerIndex, handleLayerVisibilty, zoomToLayerData, handleLayerOpacity }) => {
	const metadata = layer.get('metadata')
	const layerTitle = metadata['title']
	const bbox = metadata['bbox'].map(coord => parseFloat(coord))
	const projection = metadata['projection']
	return (
		<ListItem disableGutters={true} className="layer-switcher-item dense">
			<DragHandle />
			<Checkbox
				checked={layer.getVisible()}
				tabIndex={-1}
				onChange={handleLayerVisibilty(layerIndex)}
				disableRipple
			/>
			<div className="element-flex element-column title-noWrap">
				<Message message={layerTitle} noWrap={true} align="left" type="body1" />
				<InputRange
					minValue={0}
					maxValue={1}
					step={.1}
					value={layer.getOpacity()}
					onChange={handleLayerOpacity(layerIndex)}
				/>
			</div>
			<DropDown>
				<MenuItem onClick={() => zoomToLayerData(bbox, projection)}>
					{"Zoom To Layer Data"}
				</MenuItem>
			</DropDown>
		</ListItem >
	)
})
const LayerList = SortableContainer(({ layers, handleLayerVisibilty, zoomToLayerData, handleLayerOpacity }) => {
	return (
		<List
			disablePadding={true}
			subheader={<ListSubheader disableSticky={true}>{"Drag & Drop To Order the Layers"}</ListSubheader>}>
			{layers.map((layer, index) => {
				return <LayerItem
					handleLayerVisibilty={handleLayerVisibilty}
					zoomToLayerData={zoomToLayerData}
					handleLayerOpacity={handleLayerOpacity}
					key={`item-${index}`}
					index={index}
					layerIndex={index}
					layer={layer} />
			})}
		</List>
	)
})
class CartoviewLayerSwitcher extends React.PureComponent {
	handleLayerVisibilty = layerIndex => (event, checked) => {
		let { mapLayers, setStateKey } = this.context
		let layer = mapLayers[layerIndex]
		layer.setVisible(checked)
		setStateKey('mapLayers', mapLayers)
	}
	changeLayerOrder = ({ oldIndex, newIndex }) => {
		const { mapLayers, setStateKey } = this.context
		const newMapLayers = arrayMove(mapLayers, oldIndex, newIndex)
		newMapLayers.map((layer, index) => {
			layer.setZIndex(mapLayers.length - index)
		})
		setStateKey('mapLayers', newMapLayers)
	}
	handleLayerOpacity = layerIndex => value => {
		let { mapLayers, setStateKey } = this.context
		const layer = mapLayers[layerIndex]
		layer.setOpacity(value)
		setStateKey('mapLayers', mapLayers)
	}
	render() {
		const {
			classes
		} = this.props
		const { mapLayers, mapLoading, zoomToExtent } = this.context
		return (
			<Paper className={classes.legendsPaper} elevation={0}>
				{mapLayers.length > 0 && !mapLoading && <LayerList
					layers={mapLayers}
					useDragHandle={true}
					handleLayerVisibilty={this.handleLayerVisibilty}
					zoomToLayerData={zoomToExtent}
					handleLayerOpacity={this.handleLayerOpacity}
					helperClass="sortable-container"
					onSortEnd={this.changeLayerOrder} />}
				{mapLayers.length == 0 && <Message
					message="No Layers"
					align="center"
					type="body1" />}
			</Paper>
		)
	}
}
CartoviewLayerSwitcher.contextType = BasicViewerContext
CartoviewLayerSwitcher.propTypes = {
	classes: PropTypes.object.isRequired,
}
export default withStyles(styles)(CartoviewLayerSwitcher)