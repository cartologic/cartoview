import ArrowLeft from '@material-ui/icons/KeyboardArrowLeft'
import ArrowRight from '@material-ui/icons/KeyboardArrowRight'
import { BasicViewerContext } from '../context'
import Button from '@material-ui/core/Button'
import CloseIcon from '@material-ui/icons/Close'
import IconButton from '@material-ui/core/IconButton'
import { Message } from './CommonComponents'
import Paper from '@material-ui/core/Paper'
import PropTypes from 'prop-types'
import React from 'react'
import Table from '@material-ui/core/Table'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableRow from '@material-ui/core/TableRow'
import Tooltip from '@material-ui/core/Tooltip'
import Typography from '@material-ui/core/Typography'
import ZoomIcon from '@material-ui/icons/ZoomIn'
import classnames from 'classnames'
import { withStyles } from '@material-ui/core/styles'

const styles = theme => ({
	root: {
		width: '100%',
		maxWidth: 360,
		backgroundColor: theme.palette.background.paper,
		position: 'relative',
		overflow: 'auto',
		maxHeight: 300,
	},
	button: {
		height: 'auto'
	},
	titlePanel: {
		backgroundColor: theme.palette.primary.light,
		borderColor: '#777777',
		alignItems: 'center'
	},
	content: {
		backgroundColor: theme.palette.background.paper
	},
	table: {
		display: 'block',
		width: '100%',
		overflowX: 'auto'
	},
	tableRow: {
		display: 'flex',
		width: '100%',
		flexGrow: "1",
		height: 'auto !important',
		flexBasis: "0",
		'&:nth-of-type(odd)': {
			backgroundColor: theme.palette.background.default,
		},
	},
	tableCell: {
		flex: ".5",
		alignItems: "center",
		padding: `${theme.spacing.unit}px !important`,
		whiteSpace: 'nowrap',
		overflow: 'hidden',
		textOverflow: 'ellipsis'
	}
})
const FeatureAttributesTable = withStyles(styles)((props) => {
	const { currentFeature, classes } = props
	return (
		<Table className={classes.table}>
			<TableBody className={classes.table}>
				{Object.keys(currentFeature.getProperties()).map((key, index) => {
					if (key && key != "geometry" && key != 'layerName') {
						let attibuteLabel = key
						return (
							<TableRow classes={{ root: classes.tableRow }} key={index}>
								<TableCell classes={{ body: classes.tableCell }}>{`${attibuteLabel}`}</TableCell>

								<TableCell classes={{ body: classes.tableCell }}>
									<Tooltip id="tooltip-top" title={`${currentFeature.getProperties()[key]}`} placement="top">
										<span>{`${currentFeature.getProperties()[key]}`}</span>
									</Tooltip>
								</TableCell>

							</TableRow>
						)
					}
				})}
			</TableBody>
		</Table>
	)
})
FeatureAttributesTable.propTypes = {
	currentFeature: PropTypes.object.isRequired
}
class CartoviewPopup extends React.PureComponent {
	state = {
		currentFeature: null
	}
	ensureEvents = () => {
		const {
			// resetFeatureCollection,
			changeShowPopup,
			nextFeature,
			previousFeature,
			// zoomToFeature
		} = this.context
		let self = this
		var closer = self.popupCloser
		var nextB = self.nextButton
		var prevB = self.prevButton
		// var zoomToB = self.zoomToButton
		if (closer.onclick === null) {
			closer.onclick = () => {
				// resetFeatureCollection()
				changeShowPopup()
				return false
			}
		}
		if (nextB.onclick === null) {
			nextB.onclick = () => {
				nextFeature()
			}
		}
		if (prevB.onclick === null) {
			prevB.onclick = () => {
				previousFeature()
			}
		}
		// if (zoomToB.onclick === null) {
		// 	zoomToB.onclick = () => {
		// 		let { currentFeature } = this.state
		// 		// zoomToFeature(currentFeature)
		// 	}
		// }
	}
	componentDidUpdate() {
		const { addOverlay, featureIdentifyResult, activeFeature, showPopup } = this.context
		if (showPopup) {
			this.node.style.display = 'block'
			let currentFeature = featureIdentifyResult && featureIdentifyResult.length > 0 ?
				featureIdentifyResult[activeFeature] : null
			this.setState({ currentFeature }, () => addOverlay(this.node))
			this.ensureEvents()
		} else {
			this.node.style.display = 'none'
		}
	}
	render() {
		const {
			classes
		} = this.props
		const {
			featureIdentifyResult,
			featureIdentifyLoading,
			activeFeature,
		} = this.context
		const nextButtonVisible = (featureIdentifyResult.length > 0 &&
			activeFeature != featureIdentifyResult.length - 1)
		const currentFeature = featureIdentifyResult[activeFeature]
		return (
			<div ref={node => this.node = node} id="popup" className="ol-popup-cartoview">
				<Paper elevation={2}>
					<div className={classnames("title-panel", { [classes.titlePanel]: true })}>
						{featureIdentifyResult.length != 0 &&
							<Typography
								type="body1"
								align="left"
								noWrap={true}
								color="default"
								className="element-flex title-text">
								{`Layer : ${currentFeature.get('layerName')}`}
							</Typography>}
						<IconButton
							color="default"
							className={classnames({
								'hidden': activeFeature === 0,
								'visible': activeFeature != 0,
								'popup-buttons': true, [classes.button]: true
							})} buttonRef={(node) => this.prevButton = node}
							aria-label="Delete">
							<ArrowLeft />
						</IconButton>
						<IconButton color="default"
							className={classnames({
								'hidden': !nextButtonVisible,
								'visible': nextButtonVisible,
								'popup-buttons': true,
								[classes.button]: true
							})}
							buttonRef={(node) => this.nextButton = node} aria-label="Delete">
							<ArrowRight />
						</IconButton>
						<IconButton color="default"
							buttonRef={(node) => this.popupCloser = node}
							className={classnames({
								'popup-buttons': true,
								[classes.button]: true
							})}
							aria-label="Delete">
							<CloseIcon />
						</IconButton>
					</div>
					<div className={classnames("cartoview-popup-content", { [classes.content]: true })}>{featureIdentifyResult.length > 0 && <div>
						<FeatureAttributesTable currentFeature={currentFeature} />
					</div>}
						{featureIdentifyResult.length == 0 && !featureIdentifyLoading && <Message message={"No Features at this Point"} type={"subheading"} />}
					</div>
					{/* <div className="cartoview-popup-actions center">
						<div ref={(input) => { this.zoomToButton = input }} >
							{(featureIdentifyResult.length != 0 && !featureIdentifyLoading) && <Button color="default" className={classes.button} dense={"true"}>
								<ZoomIcon />
								<Typography type="caption" align="left" noWrap={false} color="inherit">{`Zoom To Feature`}</Typography>
							</Button>}
						</div>
					</div> */}
				</Paper>
			</div>
		)
	}
}
CartoviewPopup.contextType = BasicViewerContext
CartoviewPopup.propTypes = {
	classes: PropTypes.object.isRequired
}
export default withStyles(styles)(CartoviewPopup)